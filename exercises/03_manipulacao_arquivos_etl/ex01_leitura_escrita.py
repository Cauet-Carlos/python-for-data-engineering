
conteudo_logs = """1,Carlos,100
2,Ana,250
3,Pedro,-50
4,Maria,0
5,João,300
6,Carla,-10"""


with open("logs_vendas.txt", "w", encoding="utf-8") as arquivo:
    arquivo.write(conteudo_logs)


def processar_logs(nome_arquivo):
    l_vendas = []

    with open(nome_arquivo, "r", encoding="utf-8") as arquivos_leitura:
        for arquivo in arquivos_leitura:
            linha_arquivo = arquivo.strip().split(",")

            vendas = {
                "id": int(linha_arquivo[0]),
                "cliente": linha_arquivo[1],
                "valor": int(linha_arquivo[2])
            }

            l_vendas.append(vendas)
    
    return l_vendas


def analisar_logs(analise_arquivo):
    
    lista_validos = []
    lista_invalidos = []

    for linha in analise_arquivo:
        if linha["valor"] > 0:
            lista_validos.append(linha)
        else:
            lista_invalidos.append(linha)
    
    validos = len(lista_validos)
    invalidos = len(lista_invalidos)
    percentual_qualidade = (validos / len(analise_arquivo)) * 100

    return lista_validos, validos, lista_invalidos, invalidos, percentual_qualidade


def gerar_relatorio(caminho_arquivo, registros, qtd_validos, qtd_invalidos, percentual_qualidade):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo_escrito:
        arquivo_escrito.write("RELATÓRIO DE AUDITORIA DE VENDAS\n\n")
        arquivo_escrito.write(f"Total de registros: {len(registros)}\n")
        arquivo_escrito.write(f"Registros válidos: {qtd_validos}\n")
        arquivo_escrito.write(f"Registros inválidos: {qtd_invalidos}\n")
        arquivo_escrito.write(f"Percentual de qualidade: {percentual_qualidade:.2f}%\n")


def gerar_rejeicoes(caminho_arquivo, lista_invalidos):
    with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:

        for venda in lista_invalidos:

            linha = (
                f'{venda["id"]},'
                f'{venda["cliente"]},'
                f'{venda["valor"]}\n'
            )

            arquivo.write(linha)


def ler_relatorio(leitura_arquivo):
    with open(leitura_arquivo, "r", encoding="utf-8") as arquivo_leitura_final:
        conteudo = arquivo_leitura_final.read()

    return conteudo



lista_vendas = processar_logs("logs_vendas.txt")
lista_validos, qtd_validos, lista_invalidos, qtd_invalidos, percentual_qualidade = analisar_logs(lista_vendas)
# Gera o arquivo final de relatório passando todas as informações necessárias
gerar_relatorio("relatorio_vendas.txt", lista_vendas, qtd_validos, qtd_invalidos, percentual_qualidade)
gerar_rejeicoes("rejeicoes.txt", lista_invalidos)
conteudo_relatorio = ler_relatorio("relatorio_vendas.txt")


print("Relatório 'relatorio_vendas.txt' gerado com sucesso!")
print("=="*20)
print(conteudo_relatorio)