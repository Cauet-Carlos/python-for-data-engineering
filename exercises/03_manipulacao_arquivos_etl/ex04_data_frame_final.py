import os
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------------------------
# CONTRATO DE SCHEMA
# ---------------------------------------------------------------------------
# Lista das colunas que todo arquivo de vendas precisa ter para ser
# considerado válido. Isso funciona como uma espécie de "contrato de dados":
# qualquer CSV que não siga esse padrão é rejeitado antes de entrar na
# camada "trusted" do data lake.
COLUNAS_VALIDAS_DF = [
    "venda_id",
    "cliente_id",
    "produto_id",
    "quantidade",
    "valor_unitario",
    "data_venda"
]


def localizar_arquivos(caminho_raw):
    """
    Varre a pasta 'raw' e retorna apenas os arquivos que seguem a
    convenção de nomenclatura esperada: começam com 'vendas_' e
    terminam em '.csv'.

    Isso evita processar arquivos que não pertencem ao pipeline
    (ex: .txt, README, arquivos temporários etc).
    """
    arquivos_vendas = []

    for arquivo in os.listdir(caminho_raw):
        if arquivo.startswith("vendas_") and arquivo.endswith(".csv"):
            arquivos_vendas.append(arquivo)

    return arquivos_vendas


def validar_estrutura(df):
    """
    Compara as colunas do DataFrame recebido com as colunas esperadas,
    usando operações de conjunto (set) para identificar diferenças
    de forma eficiente.

    Retorna:
        estrutura_valida (bool): True se não faltar nenhuma coluna esperada
        faltantes (list): colunas que deveriam existir e não existem
        extras (list): colunas que existem no arquivo mas não eram esperadas
    """
    colunas_recebidas = set(df.columns)
    colunas_esperadas = set(COLUNAS_VALIDAS_DF)

    # Diferença de conjuntos: o que está em "esperadas" mas não em "recebidas"
    faltantes = sorted(
        colunas_esperadas - colunas_recebidas
    )

    # Diferença de conjuntos: o que está em "recebidas" mas não em "esperadas"
    extras = sorted(
        colunas_recebidas - colunas_esperadas
    )

    # A estrutura só é considerada válida se NADA estiver faltando.
    # Colunas extras não invalidam o arquivo, apenas são registradas.
    estrutura_valida = len(faltantes) == 0

    return estrutura_valida, faltantes, extras


def carregar_vendas(caminho_raw, arquivos_vendas):
    """
    Lê cada arquivo CSV encontrado, valida sua estrutura e separa em
    dois grupos: DataFrames válidos (prontos para consolidar) e
    registros de arquivos rejeitados (com o motivo da rejeição).

    Essa função é o "coração" da etapa de Extract + validação do ETL.
    """
    lista_dataframes = []
    arquivos_rejeitados = []

    for arquivo in arquivos_vendas:
        caminho_arquivo = os.path.join(
            caminho_raw,
            arquivo
        )

        try:
            df = pd.read_csv(caminho_arquivo)
            estrutura_valida, faltantes, extras = validar_estrutura(df)

            if estrutura_valida:
                # Rastreabilidade: guarda de qual arquivo cada linha veio.
                # Isso é essencial em pipelines de dados para auditoria
                # e para investigar problemas depois (linhagem de dados).
                df["arquivo_origem"] = arquivo
                lista_dataframes.append(df)

            else:
                # Arquivo com schema errado: não entra no pipeline,
                # mas fica registrado o motivo para análise posterior.
                arquivos_rejeitados.append({
                    "arquivo": arquivo,
                    "motivo": "Schema inválido",
                    "faltantes": faltantes,
                    "extras": extras
                })

        except Exception as erro:
            # Captura qualquer erro de leitura (arquivo corrompido,
            # encoding errado, CSV mal formado etc.) sem derrubar
            # o pipeline inteiro — só esse arquivo é descartado.
            arquivos_rejeitados.append({
                "arquivo": arquivo,
                "motivo": str(erro)
            })

    return lista_dataframes, arquivos_rejeitados


def consolidar_vendas(lista_dataframes):
    """
    Junta (empilha) todos os DataFrames válidos em um único DataFrame.
    'ignore_index=True' evita que os índices originais de cada arquivo
    se repitam no resultado final.
    """
    return pd.concat(
        lista_dataframes,
        ignore_index=True
    )


def salvar_trusted(df, caminho_trusted):
    """
    Salva o DataFrame consolidado na camada 'trusted' do data lake.
    Cria a pasta de destino automaticamente caso ainda não exista.
    """
    os.makedirs(
        caminho_trusted,
        exist_ok=True
    )

    caminho_saida = os.path.join(
        caminho_trusted,
        "vendas_consolidadas.csv"
    )

    df.to_csv(
        caminho_saida,
        index=False,
        encoding="utf-8"
    )

    return caminho_saida


def gerar_metricas(arquivos, lista_df, rejeitados, df_final):
    """
    Gera um resumo da execução do pipeline.
    Retorna um dicionário contendo as principais métricas.
    """
    metricas = {
        # Quantidade total de arquivos encontrados na pasta RAW
        "arquivos_encontrados": len(arquivos),
        # Quantidade de DataFrames que passaram na validação
        "arquivos_validos": len(lista_df),
        # Quantidade de arquivos rejeitados
        "arquivos_rejeitados": len(rejeitados),
        # Quantidade total de registros após a consolidação
        "registros_consolidados": len(df_final),
        # Número de colunas do DataFrame consolidado
        "colunas_finais": len(df_final.columns),
        # Data e hora em que o pipeline terminou
        "data_execucao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
        # Status da execução
        "status": "SUCESSO"
    }

    return metricas


def gerar_log(caminho_logs, metricas, rejeitados):
    """
    Gera um arquivo de log contendo as métricas da execução
    e a relação dos arquivos rejeitados.
    """
    # Garante que a pasta de logs exista
    os.makedirs(caminho_logs, exist_ok=True)
    # Caminho completo do arquivo de log
    caminho_log = os.path.join(
        caminho_logs,
        "pipeline_execucao.txt"
    )

    # Abre o arquivo para escrita
    with open(caminho_log, "w", encoding="utf-8") as arquivo:
        arquivo.write("=" * 60 + "\n")
        arquivo.write("LOG DE EXECUÇÃO DO PIPELINE\n")
        arquivo.write("=" * 60 + "\n\n")
        # Escreve todas as métricas
        for chave, valor in metricas.items():
            arquivo.write(
                f"{chave:<25}: {valor}\n"
            )

        # Caso existam arquivos rejeitados
        if rejeitados:
            arquivo.write("\n")
            arquivo.write("=" * 60 + "\n")
            arquivo.write("ARQUIVOS REJEITADOS\n")
            arquivo.write("=" * 60 + "\n")

            for erro in rejeitados:
                arquivo.write(f"\nArquivo : {erro['arquivo']}\n")
                arquivo.write(f"Motivo  : {erro['motivo']}\n")

                if "faltantes" in erro:
                    arquivo.write(
                        f"Colunas faltantes : {erro['faltantes']}\n"
                    )

                if "extras" in erro:
                    arquivo.write(
                        f"Colunas extras    : {erro['extras']}\n"
                    )

    return caminho_log

# ---------------------------------------------------------------------------
# EXECUÇÃO DO PIPELINE
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# DEFINIÇÃO DOS CAMINHOS DO DATA LAKE
# ---------------------------------------------------------------------------
# Usa o caminho do próprio arquivo como referência, para que o script
# funcione independente de onde ele seja executado (evita caminhos
# relativos "quebradiços" dependentes do diretório atual do terminal).
diretorio = os.path.dirname(os.path.abspath(__file__))

pasta_raw = os.path.join(
    diretorio,
    "data_lake",
    "raw"
)

pasta_trusted = os.path.join(
    diretorio,
    "data_lake",
    "trusted"
)

pasta_logs = os.path.join(
    diretorio,
    "data_lake",
    "logs"
)

# 1) Descobre quais arquivos de vendas existem na camada raw
arquivos = localizar_arquivos(pasta_raw)

# 2) Lê e valida cada arquivo, separando válidos de rejeitados
lista_df, rejeitados = carregar_vendas(
    pasta_raw,
    arquivos
)


if not lista_df:
    # Nenhum arquivo passou na validação: pipeline encerra sem gerar saída.
    print("=" * 60)
    print("PIPELINE ENCERRADO")
    print("=" * 60)
    print("Nenhum arquivo válido foi encontrado.\n")

    print("Arquivos rejeitados:")

    for erro in rejeitados:

        print(f"\nArquivo: {erro['arquivo']}")
        print(f"Motivo : {erro['motivo']}")

        # Nem todo erro tem 'faltantes'/'extras' (ex: erro de leitura),
        # por isso verifica se a chave existe antes de imprimir.
        if "faltantes" in erro:

            print(f"Colunas faltantes: {erro['faltantes']}")

        if "extras" in erro:

            print(f"Colunas extras: {erro['extras']}")


else:
    # 3) Consolida todos os DataFrames válidos em um só
    df_final = consolidar_vendas(
        lista_df
    )

    # 4) Salva o resultado consolidado na camada trusted
    arquivo_final = salvar_trusted(
        df_final,
        pasta_trusted
    )

    # 4) informa os metadados da pipeline
    metricas = gerar_metricas(
        arquivos,
        lista_df,
        rejeitados,
        df_final
    )

    arquivo_log = gerar_log(
        pasta_logs,
        metricas,
        rejeitados
    )
    
    # 5) Relatório final de execução do pipeline
    print("=" * 60)
    print("PIPELINE EXECUTADO COM SUCESSO")
    print("=" * 60)

    print(f"Arquivos encontrados : {len(arquivos)}")
    print(f"Arquivos válidos     : {len(lista_df)}")
    print(f"Arquivos rejeitados  : {len(rejeitados)}")
    print(f"Registros finais     : {len(df_final)}")
    print(f"Arquivo gerado       : {arquivo_final}")

    # Mesmo com sucesso, exibe detalhes dos arquivos que foram
    # rejeitados ao longo do processo (se houver algum).
    if rejeitados:
        print("\nArquivos rejeitados:")

        for erro in rejeitados:
            print(f"\nArquivo: {erro['arquivo']}")
            print(f"Motivo : {erro['motivo']}")

            if "faltantes" in erro:
                print(f"Colunas faltantes: {erro['faltantes']}")

            if "extras" in erro:
                print(f"Colunas extras: {erro['extras']}")

    print("\n" + "=" * 60)
    print("MÉTRICAS DA EXECUÇÃO")
    print("=" * 60)

    for chave, valor in metricas.items():
        print(f"{chave:<25}: {valor}")

    print(f"Log gerado          : {arquivo_log}")