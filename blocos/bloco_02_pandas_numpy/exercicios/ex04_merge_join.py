import pandas as pd

def inspecao(analisa_dados):
    """Retorna o formato da matriz e os nomes das colunas da tabela."""
    registros, colunas = analisa_dados.shape
    inf_colunas = analisa_dados.columns.tolist()
    return registros, colunas, inf_colunas


def varredura_dados(df_entrada):
    """Identifica padrões inválidos, padroniza como nulo e limpa o DataFrame."""
    df_varredura = df_entrada.copy()

    # Identificando padrões inválido para serem analisados
    padroes_invalidos = [
        r'^\s*$', r'^NaN$', r'^nan$', r'^null$', r'^none$',
        r'^N/A$', r'^n/a$', r'^na$', r'^NA$'
    ]

    # Substituição dos padrões textuais inválidos por nulos nativos do Pandas
    df_varredura = df_varredura.replace(
        padroes_invalidos,
        value=pd.NA,
        regex=True
    )

    # Verifica colunas numéricas e transforma valores negativos em nulos
    colunas_numericas = df_varredura.select_dtypes(include=["number"]).columns
    for coluna in colunas_numericas:
        df_varredura[coluna] = df_varredura[coluna].where(df_varredura[coluna] >= 0)

    # Relatório estatístico gerado ANTES da exclusão das linhas erradas
    relatorio_varredura = pd.DataFrame ({
        "DF_nulos_inicial" : df_entrada.isna().sum(),
        "DF_nulos_varredura" : df_varredura.isna().sum(),
        'pct_falhas'   : (df_varredura.isna().sum() / len(df_varredura) * 100).round(2),
    })

    # Remove qualquer linha que tenha restado com valores nulos
    df_limpos = df_varredura.dropna()
    
    # Garantia de que IDs não fiquem salvos como Float (ex: 1.0) devido aos nulos anteriores
    if "id_cliente" in df_limpos.columns:
        df_limpos["id_cliente"] = df_limpos["id_cliente"].astype("Int64")

    return df_limpos, relatorio_varredura


def realizar_merge(df_clientes, df_vendas):
    """Realiza a união interna das duas tabelas através da chave id_cliente."""
    df_merge = df_clientes.merge(
        df_vendas,
        on="id_cliente",
        how="inner"
    )
    return df_merge


def kpis_comerciais(df_merge):
    """Calcula os agrupamentos financeiros e os destaques do relatório."""
    
    # Agrupamentos de faturamento (Soma de valores)
    faturamento_cliente = (
        df_merge.groupby("cliente")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
    )

    faturamento_cidade = (
        df_merge.groupby("cidade")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
    )

    faturamento_categoria = (
        df_merge.groupby("categoria")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
    )

    # Identificação dos líderes de faturamento (.idxmax() puxa o nome do índice)
    cliente_top = faturamento_cliente.idxmax()
    cidade_top = faturamento_cidade.idxmax()
    categoria_top = faturamento_categoria.idxmax()

    return (
        faturamento_cliente,
        faturamento_cidade,
        faturamento_categoria,
        cliente_top,
        cidade_top,
        categoria_top
    )


# --- CRIAÇÃO DOS DADOS DE TESTE ---
clientes = [
    {"id_cliente": 1, "cliente": "Ana", "cidade": "Manaus"},
    {"id_cliente": 2, "cliente": "João", "cidade": "Belém"},
    {"id_cliente": 3, "cliente": "Maria", "cidade": "Manaus"},
    {"id_cliente": 4, "cliente": "Carlos", "cidade": "Boa Vista"},
    {"id_cliente": 5, "cliente": "Fernanda", "cidade": "Manaus"},
    {"id_cliente": 6, "cliente": "", "cidade": "Macapá"},       
    {"id_cliente": 7, "cliente": "Pedro", "cidade": None},         
    {"id_cliente": None, "cliente": "Lucas", "cidade": "Palmas"}, 
    {"id_cliente": -1, "cliente": "Erro", "cidade": "Invisível"},  
]
df_clientes = pd.DataFrame(clientes)

vendas = [
    {"id_cliente": 1, "categoria": "Notebook", "valor_compra": 3500},
    {"id_cliente": 1, "categoria": "Mouse", "valor_compra": None},      
    {"id_cliente": 2, "categoria": "Monitor", "valor_compra": 900},
    {"id_cliente": 3, "categoria": "Notebook", "valor_compra": 4200},
    {"id_cliente": 5, "categoria": "Headset", "valor_compra": 250},
    {"id_cliente": 3, "categoria": "Teclado", "valor_compra": -150},   
    {"id_cliente": 4, "categoria": "", "valor_compra": 50},           
    {"id_cliente": 2, "categoria": "Cabo HDMI", "valor_compra": None},  
    {"id_cliente": 99, "categoria": "Webcam", "valor_compra": 300},    
]
df_vendas = pd.DataFrame(vendas)


# --- EXECUÇÃO DO PIPELINE DE DADOS ---
tot_registros_clientes, tot_colunas_clientes, colunas_clientes = inspecao(df_clientes)
tot_registros_vendas, tot_colunas_vendas, colunas_vendas = inspecao(df_vendas)

df_dados_limpos_c, relatorio_erros_c = varredura_dados(df_clientes)
df_dados_limpos_v, relatorio_erros_v = varredura_dados(df_vendas)

df_consolidado = realizar_merge(df_dados_limpos_c, df_dados_limpos_v)

(
    kpi_cliente,
    kpi_cidade,
    kpi_categoria,
    top_cliente,
    top_cidade,
    top_categoria
) = kpis_comerciais(df_consolidado)


# --- IMPRESSÕES DOS RELATÓRIOS ---
print("==" * 40)
print(f'{"BASE DE DADOS CARREGADA":^80}')
print("==" * 40)

print("=-" * 40)
print(f'{"INSPEÇÃO INICIAL":^80}')
print("=-" * 40)

print("\nDADOS - CLIENTES\n")
print(df_clientes)
print(f"\nRegistros: {tot_registros_clientes} | Colunas: {tot_colunas_clientes} | Matriz: {df_clientes.shape}\n")
for coluna_c in colunas_clientes:
    print(f"{coluna_c} --> {df_clientes[coluna_c].dtype}")
print("--" * 40)

print("\nDADOS - VENDAS\n")
print(df_vendas)
print(f"\nRegistros: {tot_registros_vendas} | Colunas: {tot_colunas_vendas} | Matriz: {df_vendas.shape}\n")
for coluna_v in colunas_vendas:
    print(f"{coluna_v} --> {df_vendas[coluna_v].dtype}")

print("\n" + "=-" * 40)
print(f'{"VARREDURA E TRATAMENTO DOS DADOS":^80}')
print("=-" * 40)
print("RELATÓRIO DE ERROS - CLIENTES:")
print(relatorio_erros_c)
print("-" * 40)
print("CLIENTES APROVADOS:")
print(df_dados_limpos_c)
print("." * 80)
print("RELATÓRIO DE ERROS - VENDAS:")
print(relatorio_erros_v)
print("-" * 40)
print("VENDAS APROVADAS:")
print(df_dados_limpos_v)

print("\n" + "==" * 40)
print(f'{"DASHBOARD EXECUTIVO DE VENDAS":^80}')
print("==" * 40)

print(f"\nKPI 01 - FATURAMENTO POR CLIENTE\n{'-'*40}")
print(kpi_cliente.map('R$ {:,.2f}'.format))

print(f"\nKPI 02 - FATURAMENTO POR CIDADE\n{'-'*40}")
print(kpi_cidade.map('R$ {:,.2f}'.format))

print(f"\nKPI 03 - FATURAMENTO POR CATEGORIA\n{'-'*40}")
print(kpi_categoria.map('R$ {:,.2f}'.format))

print(f"\nKPI 04 - CLIENTE COM MAIOR FATURAMENTO: {top_cliente} (R$ {kpi_cliente.max():,.2f})")
print(f"KPI 05 - CIDADE COM MAIOR FATURAMENTO: {top_cidade} (R$ {kpi_cidade.max():,.2f})")
print(f"KPI 06 - CATEGORIA MAIS RENTÁVEL: {top_categoria} (R$ {kpi_categoria.max():,.2f})")
print("==" * 40)
