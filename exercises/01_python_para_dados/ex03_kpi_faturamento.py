# Funções
def titulo():
    print("=-"*30)
    print(f'{"KPI de Faturamento":^60}')
    print("=-"*30)


def faturamento_total(lista_valores):
    faturamento_vendas = 0
    for venda in lista_valores:
        faturamento_vendas += venda
    print(f"Faturamento Total: R${faturamento_vendas:<10}")
    return faturamento_vendas


def quantidade_vendas(totalidade):
    n_quantidade = len(totalidade)
    print(f"Quantidade de itens: {n_quantidade:<10}")
    return n_quantidade


def tickt_medio(n_quantidade, faturamento_vendas):
    tickt = faturamento_vendas / n_quantidade
    print(f"Ticket Médio: R${tickt:<10.2f}")
    return tickt
    
# Inicio do código
# Declaração dos dados da lista
valores_vendas = [1542, 5412, 2463, 125, 545, 321, 125, 454, 124, 252, 984]

# Input que será enviado para ser recebido no parâmetro da função título
titulo()

# Salvando os retornos dentro de variáveis
faturamento = faturamento_total(valores_vendas)
quantidade = quantidade_vendas(valores_vendas)

# Passando as duas variáveis numéricas
tickt_medio(quantidade, faturamento)