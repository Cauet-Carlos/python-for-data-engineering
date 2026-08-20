def titulo():
    print("=-"*30)
    print(f'{"Limpeza de dados":^60}')
    print("=-"*30)


def qtd_inicial_registros(total_registros):
    qtd_inicial = len(total_registros)
    print(f"Quantidade inicial de registros: {qtd_inicial}")
    return qtd_inicial

def qtd_removida_registros(carga_vendas):
    cont_registros_invalidos = 0
    for venda in carga_vendas:
        if venda["valor"] is None:
            cont_registros_invalidos += 1
        elif isinstance(venda["valor"], str) and not venda["valor"].replace('.', '', 1).isdigit():
            cont_registros_invalidos += 1
        elif float(venda["valor"]) <= 0:
            cont_registros_invalidos += 1
        elif venda["status"].lower() != "efetivado":
            cont_registros_invalidos += 1
    print(f"Quantidade registros removidos: {cont_registros_invalidos}")
    return cont_registros_invalidos


def qtd_final_registros(qtd_inicial, cont_registros_invalidos):
    qtd_final = qtd_inicial - cont_registros_invalidos
    print(f"Quantidade final de registros: {qtd_final}")
    return qtd_final

# Carga de dados bruta recebida do sistema externo
carga_vendas_bruta = [
    {"id_venda": 101, "valor": 1542, "status": "efetivado"},
    {"id_venda": 102, "valor": -5412, "status": "efetivado"},    
    {"id_venda": 103, "valor": 2463, "status": "efetivado"},
    {"id_venda": 104, "valor": 0, "status": "pendente"},         
    {"id_venda": 105, "valor": "545", "status": "efetivado"},    
    {"id_venda": 106, "valor": 321, "status": "cancelado"},      
    {"id_venda": 107, "valor": None, "status": "efetivado"},     
    {"id_venda": 108, "valor": 454, "status": "efetivado"},
    {"id_venda": 109, "valor": "erro_sistema", "status": ""},    
    {"id_venda": 111, "valor": 984, "status": "efetivado"},
    {"id_venda": 112, "valor": -125, "status": "efetivado"},     
    {"id_venda": 113, "valor": 0, "status": "efetivado"},         
    {"id_venda": 114, "valor": 1250, "status": "EFETIVADO"},     
    {"id_venda": 115, "valor": 45.90, "status": "efetivado"}    
]

titulo()

inicial = qtd_inicial_registros(carga_vendas_bruta)
removidos = qtd_removida_registros(carga_vendas_bruta)
qtd_final_registros(inicial, removidos)