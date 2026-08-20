import pandas as pd
import os

diretorio_atual = os.path.dirname(os.path.abspath(__file__))
diretorio_final = os.path.dirname(diretorio_atual)

colunas = ["venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda"]

# colunas específicas para os meses com schema alterado de propósito
colunas_janeiro = ["venda_id", "cliente_id", "produto_id", "quantidade", "data_venda"]  # sem valor_unitario
colunas_junho = ["venda_id", "cliente_id", "produto_id", "valor_unitario", "data_venda"]  # sem quantidade
colunas_abril = colunas + ["status_entrega"]  # coluna extra

# Janeiro: Coluna faltando (valor_unitario removida)
vendas_jan = [
    [1, 1001, 1, 1, "2026-01-05"],
    [2, 1002, 2, -2, "2026-01-07"],
    [3, 1004, 4, 1, "2026-01-08"],
    [4, 1001, None, 1, "2026-01-10"],
    [5, 1005, 3, 2, "2026-01-15"],
    [6, 1022, 1, 1, "2026-01-16"],
    [7, 1014, 2, 3, "2026-01-18"],
    [8, 1009, 3, 1, "2026-01-19"],
    [9, 1033, 5, 2, "2026-01-22"],
    [10, 1045, 4, 1, "2026-01-25"],
    [11, 1012, 1, 1, "2026-01-26"],
    [12, 1002, 3, 4, "2026-01-28"],
    [13, 1027, 2, 2, "2026-01-29"],
    [14, 1050, 5, 1, "2026-01-30"],
    [1, 1001, 1, 1, "2026-01-05"]
]

# Fevereiro: Colunas normais + Erros inclusos
vendas_fev = [
    [30001, 1006, 5, 2, 300.0, "2026-04-02"],
    [30002, 1023, 2, 1, 120.0, "2026-04-05"],
    [30003, 1041, 1, -1, 3500.0, "2026-04-07"],
    [30004, 1017, 4, 1, 1200.0, "2026-04-11"],
    [30005, 1039, 3, 3, 250.0, "2026-04-14"],
    [30006, 1049, 1, 1, None, "2026-04-17"],
    [30007, 1011, 5, 1, 300.0, "2026-04-20"],
    [30008, 1028, 2, 2, 120.0, "2026-04-22"],
    [30009, 1002, 4, 1, 1200.0, "2026-04-25"],
    [30010, 1034, 3, 2, 250.0, "2026-04-28"],
    [30011, 1046, 2, 1, 120.0, "2026-04-30"],
    [30002, 1023, 2, 1, 120.0, "2026-04-05"]
]

# Março: Colunas normais
vendas_mar = [
    [50001, 1036, 4, 1, 1200.0, None],
    [50002, 1010, 2, 2, 120.0, "2026-06-05"],
    [50003, 1045, 1, 1, 3500.0, "2026-06-08"],
    [50004, 1026, 3, -5, 250.0, "2026-06-12"],
    [50005, 1018, 5, 3, 300.0, "2026-06-15"],
    [50006, 1009, 2, 1, 120.0, "2026-06-18"],
    [50007, 1040, 1, 1, 3500.0, "2026-06-20"],
    [50008, 1031, 4, 1, 1200.0, "2026-06-23"],
    [50009, 1022, 3, 2, 250.0, "2026-06-26"],
    [50010, 1015, 5, 1, 300.0, "2026-06-28"],
    [50011, 1044, 2, 4, 120.0, "2026-06-30"],
    [50003, 1045, 1, 1, 3500.0, "2026-06-08"]

]

# Abril: Coluna extra ("status_entrega")
vendas_abr = [
    [10001, 1011, 2, 5, 120.0, "2026-02-01", "Entregue"],
    [10002, 1044, 4, 1, 1200.0, "2026-02-02", "Entregue"],
    [10003, 1001, 1, 1, -3500.0, "2026-02-05", "Entregue"],
    [10004, 1029, 3, 2, 250.0, "2026-02-06", "Entregue"],
    [10005, None, 5, 1, 300.0, "2026-02-09", "Entregue"],
    [10006, 1018, 1, 2, 3500.0, "2026-02-12", "Entregue"],
    [10007, 1007, 2, 1, 120.0, "2026-02-15", "Entregue"],
    [10008, 1040, 3, 3, 250.0, "2026-02-18", "Entregue"],
    [10009, 1015, 4, 1, 1200.0, "2026-02-20", "Entregue"],
    [10010, 1022, 5, 2, 300.0, "2026-02-22", "Entregue"],
    [10011, 1031, 2, 1, 120.0, "2026-02-25", "Entregue"],
    [10012, 1004, 1, 1, 3500.0, "2026-02-28", "Entregue"],
    [10002, 1044, 4, 1, 1200.0, "2026-02-02", "Entregue"]
]

# Maio: Colunas normais
vendas_mai = [
    [40001, 1020, 1, 1, 3500.0, "2026-05-01"],
    [40002, 1013, 3, 2, -250.0, "2026-05-04"],
    [40003, 1047, 2, 1, 120.0, "2026-05-07"],
    [40004, 1005, 5, 4, 300.0, "2026-05-10"],
    [None, 1032, 4, 1, 1200.0, "2026-05-13"],
    [40006, 1016, 1, 1, 3500.0, "2026-05-16"],
    [40007, 1043, 3, 1, 250.0, "2026-05-19"],
    [40008, 1024, 2, 3, 120.0, "2026-05-22"],
    [40009, 1038, 5, 1, 300.0, "2026-05-25"],
    [40010, 1007, 4, 2, 1200.0, "2026-05-28"],
    [40011, 1011, 1, 1, 3500.0, "2026-05-31"],
    [40004, 1005, 5, 4, 300.0, "2026-05-10"]
]

# Junho: Coluna faltando (quantidade removida)
vendas_jun = [
    [20001, 1025, 3, -250.0, "2026-03-01"],
    [20002, 1008, 1, 3500.0, "2026-03-03"],
    [20003, 1019, 5, 300.0, "2026-03-06"],
    [20004, None, 2, 120.0, "2026-03-10"],
    [20005, 1048, 4, 1200.0, "2026-03-12"],
    [20006, 1012, 1, 3500.0, "2026-03-15"],
    [20007, 1003, 3, 250.0, "2026-03-17"],
    [20008, 1037, 2, 120.0, "2026-03-20"],
    [20009, 1021, 5, 300.0, "2026-03-24"],
    [20010, 1014, 4, 1200.0, "2026-03-27"],
    [20011, 1042, 3, 250.0, "2026-03-29"],
    [20012, 1009, 1, 3500.0, "2026-03-31"],
    [20003, 1019, 5, 300.0, "2026-03-06"]
]


# cada mês aponta para a lista de dados e a lista de colunas que
# realmente correspondem à estrutura daquele CSV
meses = {
    "janeiro": (vendas_jan, colunas_janeiro),
    "favereiro": (vendas_fev, colunas),
    "marco": (vendas_mar, colunas),
    "abril": (vendas_abr, colunas_abril),
    "maio": (vendas_mai, colunas),
    "junho": (vendas_jun, colunas_junho),
}


def salvar_vendas(nome_mes, dados, colunas_mes, diretorio_final):
    df = pd.DataFrame(dados, columns=colunas_mes)
    caminho = os.path.join(diretorio_final, "data_lake", "raw", f"vendas_{nome_mes}.csv")
    df.to_csv(caminho, index=False)
    return caminho


for nome_mes, (dados, colunas_mes) in meses.items():
    caminho = salvar_vendas(nome_mes, dados, colunas_mes, diretorio_final)
    print(f"Gerado: {caminho}")