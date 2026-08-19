import pandas as pd
import os

# 1. Configuração do diretório
diretorio_atual = os.path.dirname(os.path.abspath(__file__))

# 2. Dados de Clientes
clientes = [
    [1001, "Carlos Silva", "carlos@email.com", "Manaus", "AM", "2025-01-10", "Ativo"],
    [1002, "Ana Souza", "ana@email.com", "Belém", "PA", "2025-02-15", "Ativo"],
    [1003, "Pedro Santos", None, "Manaus", "AM", "2025-03-01", "Inativo"],
    [1004, "Maria Costa", "maria@email.com", "Boa Vista", "RR", "2025-04-20", "Ativo"],
    [1005, "Lucas Lima", "lucas@email.com", "Manaus", "AM", "2025-05-12", "Ativo"]
]

df_clientes = pd.DataFrame(
    clientes,
    columns=["cliente_id", "nome", "email", "cidade", "uf", "data_cadastro", "status"]
)

caminho_clientes = os.path.join(diretorio_atual, "data_lake", "raw", "clientes.csv")
df_clientes.to_csv(caminho_clientes, index=False)



# 3. Dados de Produtos
produtos = [
    [1, "Notebook Dell", "Informática", 3500.00, 15],
    [2, "Mouse Logitech", "Periféricos", 120.00, 80],
    [3, "Teclado Mecânico", "Periféricos", 250.00, 50],
    [4, "Monitor LG 27", "Monitores", 1200.00, 20],
    [5, "Headset HyperX", "Áudio", 300.00, 35]
]

df_produtos = pd.DataFrame (
    produtos,
    columns=["produto_id", "produto", "categoria", "preco_unitario", "estoque"]
)

caminho_produto = os.path.join(diretorio_atual, "data_lake", "raw", "produtos.csv")
df_produtos.to_csv(caminho_produto, index=False)



# 4. Dados das vendas Fevereiro
fornecedores = [
    [1, "Dell Brasil", "Informática"],
    [2, "Logitech", "Periféricos"],
    [3, "LG Electronics", "Monitores"]
]

df_fornecedores = pd.DataFrame(
    fornecedores,
    columns=["fornecedor_id", "nome_fornecedor","segmento"
    ]
)

caminho_fornecedores = os.path.join(diretorio_atual, "data_lake", "raw", "fornecedores.csv")
df_produtos.to_csv(caminho_fornecedores, index=False)



# 5. Dados das vendas Janeiro
vendas_jan = [
    [1, 1001, 1, 1, 3500.00, "2026-01-05"],
    [2, 1002, 2, 2, 120.00, "2026-01-07"],
    [3, 1004, 4, 1, 1200.00, "2026-01-08"],
    [4, 1001, 5, 1, 300.00, "2026-01-10"],
    [5, 1005, 3, 2, 250.00, "2026-01-15"]
]

df_vendas_jan = pd.DataFrame(
    vendas_jan,
    columns=[
        "venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda"
    ]
)

caminho_venda_jan = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_jan.csv")
df_vendas_jan.to_csv(caminho_venda_jan, index=False)



# 6. Dados das vendas Fevereiro
vendas_fev = [
    [1, 1003, 2, 3, 150.00, "2026-02-02"],
    [2, 1005, 5, 1, 450.00, "2026-02-11"],
    [3, 1001, 3, 4, 80.00, "2026-02-14"],
    [4, 1002, 1, 2, 3200.00, "2026-02-20"],
    [5, 1004, 4, 1, 1150.00, "2026-02-25"]
]

df_vendas_fev = pd.DataFrame(
    vendas_fev, 
    columns=["venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda"
    ]
)

caminho_venda_fev = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_fev.csv")
df_vendas_fev.to_csv(caminho_venda_fev, index=False)



# 7. Dados das vendas Março
vendas_mar = [
    [1, 1001, 1, 2, "2026-03-05"],
    [2, 1004, 3, 1, "2026-03-12"],
    [3, 1002, 5, 3, "2026-03-22"],
    [4, 1005, 2, 1, "2026-03-25"],
    [5, 1003, 4, 4, "2026-03-28"],
    [6, 1001, 2, 2, "2026-03-30"]
]
df_vendas_mar = pd.DataFrame(
    vendas_mar, 
    columns=["venda_id", "cliente_id", "produto_id", "quantidade", "data_venda"]
)
caminho_venda_mar = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_mar.csv")
df_vendas_mar.to_csv(caminho_venda_mar, index=False)



# 8. Dados das vendas Abril
vendas_abr = [
    [1, 1002, 4, 1, 120.00, "2026-04-02"],
    [2, 1003, 2, 2, 450.00, "2026-04-15"],
    [3, 1005, 1, 1, 3200.00, "2026-04-18"],
    [4, 1001, 5, 3, 150.00, "2026-04-22"],
    [5, 1004, 3, 2, 80.00, "2026-04-27"],
    [6, 1002, 2, 1, 450.00, "2026-04-29"]
]
df_vendas_abr = pd.DataFrame(
    vendas_abr, 
    columns=["venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda"]
)
caminho_venda_abr = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_abr.csv")
df_vendas_abr.to_csv(caminho_venda_abr, index=False)



# 9. Dados das vendas Maio
vendas_mai = [
    [1, 1005, 3, 1, 850.00, "2026-05-10", "Cartão"],
    [2, 1001, 1, 2, 90.00, "2026-05-14", "Pix"],
    [3, 1003, 5, 1, 1150.00, "2026-05-19", "Boleto"],
    [4, 1002, 2, 4, 450.00, "2026-05-22", "Pix"],
    [5, 1004, 4, 1, 120.00, "2026-05-25", "Cartão"],
    [6, 1005, 1, 2, 3200.00, "2026-05-28", "Transferência"]
]
df_vendas_mai = pd.DataFrame(
    vendas_mai, 
    columns=["venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda", "forma_pagamento"]
)
caminho_venda_mai = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_mai.csv")
df_vendas_mai.to_csv(caminho_venda_mai, index=False)



# 10. Dados das vendas Junho
vendas_jun = [
    [1, 1003, 2, 5, 300.00, "2026-06-04"],
    [2, 1001, 4, 1, 1200.00, "2026-06-09"],
    [3, 1002, 1, 3, 150.00, "2026-06-15"],
    [4, 1005, 3, 2, 80.00, "2026-06-19"],
    [5, 1004, 5, 1, 450.00, "2026-06-24"],
    [6, 1002, 2, 4, 1150.00, "2026-06-28"]
]
df_vendas_jun = pd.DataFrame(
    vendas_jun, 
    columns=["venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda"]
)
caminho_venda_jun = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_jun.csv")
df_vendas_jun.to_csv(caminho_venda_jun, index=False)



# 11. Dados das vendas Julho
vendas_jul = [
    [1, 1004, 5, 2, 150.00, "2026-07-02"],
    [2, 1002, 3, 1, 650.00, "2026-07-08"],
    [3, 1001, 2, 5, 450.00, "2026-07-12"],
    [4, 1005, 4, 1, 1150.00, "2026-07-17"],
    [5, 1003, 1, 2, 3200.00, "2026-07-22"],
    [6, 1004, 3, 3, 80.00, "2026-07-29"]
]
df_vendas_jul = pd.DataFrame(
    vendas_jul, 
    columns=["venda_id", "cliente_id", "produto_id", "quantidade", "valor_unitario", "data_venda"]
)
caminho_venda_jul = os.path.join(diretorio_atual, "data_lake", "raw", "vendas_jul.csv")
df_vendas_jul.to_csv(caminho_venda_jul, index=False)