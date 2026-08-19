import os
import logging
from datetime import datetime

import pandas as pd

# ============================================================
# CONFIGURAÇÃO DA PIPELINE
# ============================================================

PREFIXO_ARQUIVO = "vendas_"
EXTENSAO_ARQUIVO = ".csv"

# contrato das colunas
COLUNAS_OBRIGATORIAS = [
    "venda_id",
    "cliente_id",
    "produto_id",
    "quantidade",
    "valor_unitario",
    "data_venda",
]


# ============================================================
# LOGGING
# ============================================================

class FiltroConsole(logging.Filter):
    """Só deixa passar para o console as mensagens marcadas com console=True."""

    def filter(self, record):
        return getattr(record, "mostrar_console", False)


def configurar_logger(pasta_logs):
    """Cria um logger que grava tudo em arquivo, mas só exibe no console
    as mensagens explicitamente marcadas (ver função `log`)."""
    os.makedirs(pasta_logs, exist_ok=True)
    caminho_log = os.path.join(pasta_logs, "pipeline_execucao.txt")

    logger = logging.getLogger("pipeline_vendas")
    logger.setLevel(logging.INFO)
    logger.handlers.clear()  # evita duplicar handlers em reexecuções

    formato = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")

    # arquivo: registra tudo, sem exceção
    handler_arquivo = logging.FileHandler(caminho_log, encoding="utf-8")
    handler_arquivo.setFormatter(formato)
    logger.addHandler(handler_arquivo)

    # console: registra só o que for marcado como visível
    handler_console = logging.StreamHandler()
    handler_console.setFormatter(formato)
    handler_console.addFilter(FiltroConsole())
    logger.addHandler(handler_console)

    return logger


def log(logger, mensagem, console=False, nivel=logging.INFO):
    """Registra uma mensagem sempre no arquivo; no console, só se console=True."""
    logger.log(nivel, mensagem, extra={"mostrar_console": console})


# ============================================================
# EXTRACT - LOCALIZAÇÃO
# ============================================================

def localizar_arquivos(caminho_raw):
    """Localiza na pasta raw todos os arquivos que seguem o padrão vendas_*.csv"""
    arquivos_encontrados = []

    for arquivo in os.listdir(caminho_raw):
        if arquivo.startswith(PREFIXO_ARQUIVO) and arquivo.endswith(EXTENSAO_ARQUIVO):
            arquivos_encontrados.append(arquivo)

    arquivos_encontrados.sort()

    return arquivos_encontrados


# ============================================================
# EXTRACT - INVENTÁRIO DA CAMADA RAW
# ============================================================

def gerar_inventario_raw(pasta_raw, arquivos_encontrados, pasta_logs):
    """Gera um arquivo de log com o inventário dos arquivos encontrados em raw."""
    os.makedirs(pasta_logs, exist_ok=True)
    caminho_log = os.path.join(pasta_logs, "inventario_raw.txt")

    with open(caminho_log, "w", encoding="utf-8") as f:
        f.write(f"Inventário gerado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Total de arquivos encontrados: {len(arquivos_encontrados)}\n\n")

        for arquivo in arquivos_encontrados:
            caminho_completo = os.path.join(pasta_raw, arquivo)
            tamanho_kb = os.path.getsize(caminho_completo) / 1024
            f.write(f"- {arquivo} ({tamanho_kb:.1f} KB)\n")

    return caminho_log


# ============================================================
# EXTRACT - CARREGAMENTO
# ============================================================

def carregar_arquivos(caminho_raw, arquivos_encontrados):
    """Lê cada arquivo csv e converte em DataFrame, registrando o arquivo de origem."""
    lista_dataframes = []

    for arquivo in arquivos_encontrados:
        caminho_arquivo = os.path.join(caminho_raw, arquivo)

        df = pd.read_csv(caminho_arquivo)

        # registra o nome do arquivo atual (não a lista inteira) para rastreio
        df["arquivo_origem"] = arquivo

        lista_dataframes.append(df)

    return lista_dataframes


# ============================================================
# VALIDATION - ESTRUTURA
# ============================================================

def validar_estrutura(df):
    """Compara as colunas do DataFrame com o contrato de colunas obrigatórias."""
    colunas_recebidas = set(df.columns) - {"arquivo_origem"}
    colunas_esperadas = set(COLUNAS_OBRIGATORIAS)

    faltantes = sorted(colunas_esperadas - colunas_recebidas)
    extras = sorted(colunas_recebidas - colunas_esperadas)

    estrutura_valida = len(faltantes) == 0 and len(extras) == 0

    return estrutura_valida, faltantes, extras


def validar_dataframes(lista_dataframes, logger):
    """Separa os DataFrames em válidos e rejeitados de acordo com o contrato de colunas."""
    lista_validos = []
    lista_rejeitados = []

    for df in lista_dataframes:
        arquivo_origem = df["arquivo_origem"].iloc[0]

        estrutura_valida, faltantes, extras = validar_estrutura(df)

        if estrutura_valida:
            lista_validos.append(df)
        else:
            lista_rejeitados.append({
                "arquivo": arquivo_origem,
                "faltantes": faltantes,
                "extras": extras,
                "motivo": "Schema inválido",
            })
            log(
                logger,
                f"Arquivo rejeitado: {arquivo_origem} | "
                f"faltantes={faltantes} | extras={extras}",
                console=True,
                nivel=logging.WARNING,
            )

    return lista_validos, lista_rejeitados


# ============================================================
# TRANSFORM - CONSOLIDAÇÃO
# ============================================================

def consolidar_dataframes(lista_validos):
    """Concatena todos os DataFrames válidos em um único DataFrame."""
    if not lista_validos:
        raise ValueError("Nenhum DataFrame válido disponível para transformação")

    df_consolidado = pd.concat(lista_validos, ignore_index=True)

    return df_consolidado


# ============================================================
# TRANSFORM - LIMPEZA DOS DADOS
# ============================================================

def limpar_dados(df):
    """Remove nulos, valores negativos/zerados e duplicados do DataFrame consolidado."""
    total_inicial_registros = len(df)

    # Remoção dos nulos
    df = df.dropna(subset=COLUNAS_OBRIGATORIAS)
    removidos_nulos = total_inicial_registros - len(df)

    # Remoção dos negativos/zerados
    quantidade_antes = len(df)
    df = df[(df["quantidade"] > 0) & (df["valor_unitario"] > 0)]
    removidos_negativos = quantidade_antes - len(df)

    # Remoção dos duplicados
    quantidade_antes = len(df)
    df = df.drop_duplicates()
    removidos_duplicados = quantidade_antes - len(df)

    # .copy() evita SettingWithCopyWarning nas transformações seguintes
    return df.copy(), removidos_nulos, removidos_negativos, removidos_duplicados


# ============================================================
# TRANSFORM - VALOR TOTAL
# ============================================================

def valor_total(df):
    """Calcula a coluna valor_total a partir de quantidade e valor_unitario."""
    df["valor_total"] = df["quantidade"] * df["valor_unitario"]

    return df


# ============================================================
# LOAD - CAMADA TRUSTED
# ============================================================

def salvar_trusted(df, pasta_trusted):
    """Salva o DataFrame final consolidado na camada trusted."""
    os.makedirs(pasta_trusted, exist_ok=True)
    caminho_saida = os.path.join(pasta_trusted, "vendas_consolidadas.csv")
    df.to_csv(caminho_saida, index=False)

    return caminho_saida


# ============================================================
# CAMINHOS DA PIPELINE
# ============================================================

diretorio_inicial = os.path.dirname(os.path.abspath(__file__))
diretorio_final = os.path.dirname(diretorio_inicial)

pasta_raw = os.path.join(diretorio_final, "data_lake", "raw")
pasta_trusted = os.path.join(diretorio_final, "data_lake", "trusted")
pasta_logs = os.path.join(diretorio_final, "data_lake", "logs")


# ============================================================
# EXECUÇÃO DA PIPELINE
# ============================================================

def log_secao(logger, titulo, console=False):
    """Imprime um cabeçalho de seção no log, para organizar visualmente a execução."""
    log(logger, "=" * 60, console=console)
    log(logger, titulo, console=console)
    log(logger, "=" * 60, console=console)


def main():
    logger = configurar_logger(pasta_logs)
    inicio_execucao = datetime.now()

    log(logger, "Iniciando pipeline de vendas", console=True)

    # ------------------------------------------------------
    # EXTRACT - LOCALIZAÇÃO (visível no console)
    # ------------------------------------------------------
    log_secao(logger, "EXTRACT - LOCALIZAÇÃO DE ARQUIVOS", console=True)

    arquivos_encontrados = localizar_arquivos(pasta_raw)
    log(logger, f"Arquivos encontrados: {len(arquivos_encontrados)}", console=True)
    for arquivo in arquivos_encontrados:
        log(logger, f"  - {arquivo}", console=True)

    gerar_inventario_raw(pasta_raw, arquivos_encontrados, pasta_logs)
    log(logger, "Inventário salvo em logs/inventario_raw.txt", console=True)

    # ------------------------------------------------------
    # EXTRACT - CARREGAMENTO (só vai para o arquivo de log)
    # ------------------------------------------------------
    log_secao(logger, "EXTRACT - CARREGAMENTO DE ARQUIVOS", console=False)

    lista_dataframes = carregar_arquivos(pasta_raw, arquivos_encontrados)
    for df in lista_dataframes:
        origem = df["arquivo_origem"].iloc[0]
        log(logger, f"  {origem:<25} linhas={len(df):<6} colunas={list(df.columns)}")

    # ------------------------------------------------------
    # VALIDATION (visível no console)
    # ------------------------------------------------------
    log_secao(logger, "VALIDATION - ESTRUTURA DOS ARQUIVOS", console=True)

    lista_validos, lista_rejeitados = validar_dataframes(lista_dataframes, logger)
    log(logger, f"Válidos: {len(lista_validos)}  |  Rejeitados: {len(lista_rejeitados)}", console=True)

    if lista_rejeitados:
        log(logger, "Detalhamento dos rejeitados:", console=True)
        for item in lista_rejeitados:
            log(
                logger,
                f"  - {item['arquivo']}: {item['motivo']} "
                f"(faltantes={item['faltantes']}, extras={item['extras']})",
                console=True,
            )

    # ------------------------------------------------------
    # TRANSFORM (visível no console)
    # ------------------------------------------------------
    log_secao(logger, "TRANSFORM - CONSOLIDAÇÃO E LIMPEZA", console=True)

    df_consolidado = consolidar_dataframes(lista_validos)
    total_bruto = len(df_consolidado)
    log(logger, f"Registros consolidados (antes da limpeza): {total_bruto}", console=True)

    df_limpo, removidos_nulos, removidos_negativos, removidos_duplicados = limpar_dados(df_consolidado)
    log(logger, f"  Nulos removidos:              {removidos_nulos}", console=True)
    log(logger, f"  Negativos/zerados removidos:  {removidos_negativos}", console=True)
    log(logger, f"  Duplicados removidos:         {removidos_duplicados}", console=True)
    log(logger, f"  Total removido:               {total_bruto - len(df_limpo)}", console=True)

    df_transformado = valor_total(df_limpo)
    log(logger, "Coluna valor_total calculada", console=True)

    # ------------------------------------------------------
    # LOAD (só vai para o arquivo de log)
    # ------------------------------------------------------
    log_secao(logger, "LOAD - CAMADA TRUSTED", console=False)

    caminho_final = salvar_trusted(df_transformado, pasta_trusted)
    log(logger, f"Arquivo salvo em: {caminho_final}")

    # ------------------------------------------------------
    # RESUMO FINAL (visível no console)
    # ------------------------------------------------------
    duracao = (datetime.now() - inicio_execucao).total_seconds()

    log_secao(logger, "RESUMO DA EXECUÇÃO", console=True)
    log(logger, f"Arquivos processados:     {len(arquivos_encontrados)}", console=True)
    log(logger, f"Arquivos válidos:         {len(lista_validos)}", console=True)
    log(logger, f"Arquivos rejeitados:      {len(lista_rejeitados)}", console=True)
    log(logger, f"Registros brutos:         {total_bruto}", console=True)
    log(logger, f"Registros finais:         {len(df_transformado)}", console=True)
    log(logger, f"Valor total em vendas:    R$ {df_transformado['valor_total'].sum():,.2f}", console=True)
    log(logger, f"Tempo de execução:        {duracao:.2f}s", console=True)
    log(logger, "Pipeline finalizada com sucesso", console=True)


if __name__ == "__main__":
    main()