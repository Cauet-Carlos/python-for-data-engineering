import os
from collections import Counter


def obter_pasta_raw():
    # Obtém o caminho absoluto (pasta) do diretório onde este arquivo .py está salvo
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    # Retorna o caminho completo até a pasta 'raw'
    return os.path.join(diretorio_base, "data_lake", "raw")


def listar_arquivos(caminho_raw):
    arquivos = []
    # Varre todos os elementos (arquivos, pastas, links) presentes na pasta de origem
    for item in os.listdir(caminho_raw):
        # Reconstrói o caminho completo do item para que o sistema possa inspecioná-lo
        caminho_item = os.path.join(caminho_raw, item)

        # Filtro de segurança: ignora subpastas ou atalhos, processando apenas arquivos físicos
        if os.path.isfile(caminho_item):
            arquivos.append(item)

    return arquivos


def gerar_inventario(caminho_raw, lista_arquivos):
    inventario = []
    
    # Inicializa uma subclasse de dicionário especializada em contagem de elementos repetidos
    extensoes = Counter()

    for arquivo in lista_arquivos:
        # Associa a pasta ao nome do arquivo para permitir a consulta de tamanho
        caminho_arquivo = os.path.join(caminho_raw, arquivo)
        # Divide a string do nome no último ponto (ex: 'vendas_jan' e '.csv')
        nome, extensao = os.path.splitext(arquivo)
        # Consulta os metadados do sistema operacional para capturar o tamanho físico em bytes
        tamanho = os.path.getsize(caminho_arquivo)

        # Estrutura os metadados extraídos em um dicionário amigável para manipulação ou carga posterior
        inventario.append(
            {
                "nome": nome,
                "arquivo": arquivo,
                "extensao": extensao.lower(), # .lower() evita duplicar categorias como '.CSV' e '.csv'
                "tamanho": tamanho
            }
        )

        # Registra e incrementa dinamicamente a contagem da extensão mapeada
        extensoes[extensao.lower()] += 1

    # Retorna a lista de dicionários detalhada e converte o Counter em um dicionário padrão do Python
    return inventario, dict(extensoes)


def gerar_relatorio(inventario, contagem_extensoes):
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    # Define o local do arquivo de saída na pasta corporativa de auditoria e logs
    pasta_logs = os.path.join(diretorio_base, "data_lake", "logs")
    # Cria a pasta 'logs' dinamicamente caso ela não exista, prevenindo erros de 'FolderNotFound'
    os.makedirs(pasta_logs, exist_ok=True)
    caminho_relatorio = os.path.join(pasta_logs, "inventario_raw.txt")

    # Abre o arquivo TXT em modo de escrita ('w'), limpando conteúdos antigos (sobrescrevendo), com codificação UTF-8
    with open(caminho_relatorio, "w", encoding="utf-8") as arquivo:

        # Escrita do bloco do cabeçalho estético de identificação do log
        arquivo.write("=" * 50 + "\n")
        arquivo.write("INVENTÁRIO DATA LAKE - RAW\n")
        arquivo.write("=" * 50 + "\n\n")

        # Varre a lista de dicionários estruturados gerando as quebras de linhas solicitadas no formato
        for item in inventario:
            arquivo.write(f"Arquivo   : {item['arquivo']}\n")
            arquivo.write(f"Extensão  : {item['extensao']}\n")
            arquivo.write(f"Tamanho   : {item['tamanho']} bytes\n")
            arquivo.write("-" * 50 + "\n")

        # Mede o total geral de itens válidos processados contando o comprimento da lista de inventário
        arquivo.write(f"\nTotal de arquivos: {len(inventario)}\n\n")

        arquivo.write("Quantidade por extensão\n")

        # Desestrutura o dicionário estatístico para gravar o resumo de volumetria no final do arquivo de texto
        for extensao, quantidade in contagem_extensoes.items():
            arquivo.write(f"{extensao}: {quantidade}\n")

    return caminho_relatorio


def main():
    # Orquestração sequencial e controle do pipeline de diagnóstico
    pasta_raw = obter_pasta_raw()
    arquivos = listar_arquivos(pasta_raw)

    # Coleta e desestrutura os dois retornos gerados pela função analítica
    inventario, extensoes = gerar_inventario(pasta_raw, arquivos)

    # Grava o histórico estruturado no disco rígido local
    relatorio = gerar_relatorio(inventario, extensoes)

    # Interface com o usuário: exibe no terminal apenas o resumo leve para evitar poluição visual no console
    print("=" * 50)
    print("INVENTÁRIO FINALIZADO")
    print("=" * 50)
    print(f"Arquivos encontrados : {len(arquivos)}")
    print(f"Tipos encontrados    : {extensoes}")
    print(f"Relatório gerado em  :\n{relatorio}")


if __name__ == "__main__":
    # Garante que o script execute apenas se for rodado diretamente (evita execução acidental ao ser importado como módulo)
    main()
