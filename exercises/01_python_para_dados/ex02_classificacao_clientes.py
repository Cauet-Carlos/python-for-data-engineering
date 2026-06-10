def titulo():
    print("=-"*30)
    print(f'{"CLASSIFICAÇÃO CLIENTES":^60}')
    print("=-"*30)


# Adicionado parâmetro para receber a lista
def classificao_cliente(lista_clientes):
    # O loop percorre a lista, pegando um dicionário de cliente por vez
    for cliente in lista_clientes:
        nome = cliente["nome"]
        faturamento = cliente["faturamento"]
        
        # Regra de classificação baseada no faturamento
        if faturamento >= 3000:
            status = "Ouro"
        elif faturamento >= 2000:
            status = "Prata"
        else:
            status = "Bronze"
            
        print(f"Cliente: {nome:<10} | Faturamento: R${faturamento:<5} | Status: {status}")


clientes = [ 
    {"nome": "Cauet", "faturamento": 5000},
    {"nome": "Carlos", "faturamento": 2000},
    {"nome": "Farias", "faturamento": 2500},
    {"nome": "Anthonely", "faturamento": 6000},
    {"nome": "Maria", "faturamento": 1000}
]

titulo()
classificao_cliente(clientes)