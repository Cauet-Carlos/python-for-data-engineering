# Data Cleaning
def data_cleaning(dados_vendas):
    total_vendas = len(dados_vendas)
    vendas_corrompidas = []
    qtd_vendas_corrompidas = 0
    vendas_processadas = []
    qtd_vendas_processadas = 0

    for venda in dados_vendas:
        if venda["valor"] is None or venda["valor"] <= 0:
            vendas_corrompidas.append(venda)
            qtd_vendas_corrompidas += 1
        else:
            vendas_processadas.append(venda)
            qtd_vendas_processadas += 1

    return total_vendas, qtd_vendas_processadas, qtd_vendas_corrompidas, vendas_processadas


def list_filtering(vendas_processadas):
    vendas_aprovadas = []
    vendas_canceladas = []
    vendas_recusadas = []

    for venda_status in vendas_processadas:
        if venda_status["status"].lower() == "pago":
            vendas_aprovadas.append(venda_status)
        if venda_status["status"].lower() == "cancelado":
            vendas_canceladas.append(venda_status)
        if venda_status["status"].lower() == "recusado":
            vendas_recusadas.append(venda_status)

    return vendas_aprovadas, vendas_canceladas, vendas_recusadas


def kpiss(vendas_aprovadas):
    qtd_vendas_validas = len(vendas_aprovadas)
    faturamento_total = sum(venda["valor"] for venda in vendas_aprovadas)
    ticket_medio = faturamento_total / qtd_vendas_validas

    return faturamento_total, ticket_medio


def customer_billing(vendas_aprovadas):
    resumo_clientes = {}

    for venda in vendas_aprovadas:
        nome_cliente = venda["cliente"]
        valor = venda["valor"]

        if nome_cliente not in resumo_clientes:
            resumo_clientes[nome_cliente] = {"faturamento": 0}
        
        resumo_clientes[nome_cliente]["faturamento"] += valor

    
    lista_ranking = []
    for nome, dados in resumo_clientes.items():
        lista_ranking.append({
            "cliente": nome,
            "faturamento_total": dados["faturamento"]
        })
        
    return lista_ranking


def ranking(lista_ranking):
    ranking_clientes = sorted(lista_ranking, key=lambda x: x["faturamento_total"], reverse=True)

    return ranking_clientes


vendas = [
    {"id_venda": 1001, "cliente": "Ana", "valor": -100.00, "status": "pago"},
    {"id_venda": 1002, "cliente": "Maria", "valor": None, "status": "pago"},
    {"id_venda": 1003, "cliente": "João", "valor": 250.00, "status": "pago"},
    {"id_venda": 1004, "cliente": "Carlos", "valor": -50.00, "status": "cancelado"},
    {"id_venda": 1005, "cliente": "Ana", "valor": 150.50, "status": "pago"},
    {"id_venda": 1006, "cliente": "Maria", "valor": 89.90, "status": "recusado"},  
    {"id_venda": 1008, "cliente": "Ana", "valor": 300.00, "status": "pago"},
    {"id_venda": 1009, "cliente": "Carlos", "valor": 120.00, "status": "cancelado"},
    {"id_venda": 1010, "cliente": "Maria", "valor": 55.20, "status": "pago"},
    {"id_venda": 1011, "cliente": "Marcos", "valor": 450.00, "status": "cancelado"},    
    {"id_venda": 1012, "cliente": "Ana", "valor": None, "status": "pago"},   
    {"id_venda": 1013, "cliente": "Carlos", "valor": -19.90, "status": "pago"},
    {"id_venda": 1014, "cliente": "Maria", "valor": 200.00, "status": "pago"},
    {"id_venda": 1015, "cliente": "João", "valor": 105.00, "status": "recusado"}
]


qtd_registros, qtd_registros_validos, qtd_registros_invalidos, vendas_processadas = data_cleaning(vendas)

q_vendas_aprovadas, q_vendas_canceladas, q_vendas_recusadas = list_filtering(vendas_processadas)

fat_total, ticket = kpiss(q_vendas_aprovadas)

lista_faturamento = customer_billing(q_vendas_aprovadas)

lista_ordenada = ranking(lista_faturamento)


print("=="*30)
print(f'{"INÍCIO DO PROCESSAMENTO":^60}')
print("=="*30)
print()

print("Etapa 1 - Validação dos dados")
print("--"*30)
print(f"Registros recebidos: {qtd_registros}")
print(f"Registros válidos:   {qtd_registros_validos}")
print(f"Registros inválidos: {qtd_registros_invalidos}")
print("--"*30)
print()

print("Etapa 2 - Status das vendas")
print("--"*30)
print(f"Quantidade de vendas pagas:      {len(q_vendas_aprovadas)}")
print(f"Quantidade de vendas canceladas: {len(q_vendas_canceladas)}")
print(f"Quantidade de vendas recusadas:  {len(q_vendas_recusadas)}")
print("--"*30)
print()

print("Etapa 3 - KPIs")
print("--"*30)
print(f"Faturamento Total: R$ {fat_total:.2f}")
print(f"Ticket Médio: R$ {ticket:.2f}")
print("--"*30)
print()

print("Etapa 4 - Faturamento por Cliente")
print("--"*30)
for item in lista_faturamento:
    print(f"{item['cliente']}: R$ {item['faturamento_total']:.2f}")
print("--"*30)
print()

print("Etapa 5 - Ranking\n")
for posicao, item in enumerate(lista_ordenada, start=1):
    print(f"{posicao}º {item['cliente']:<6} -> R$ {item['faturamento_total']:.0f}")

