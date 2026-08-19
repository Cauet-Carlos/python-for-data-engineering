import pandas as pd

# FUNÇÕES
# 1. INSPEÇÃO DOS DADOS
def inspecao(analise_dados):
    # Retorna o formato da matriz e converte o índice de colunas em lista
    registros, colunas = analise_dados.shape
    inf_colunas = analise_dados.columns.tolist()

    return registros, colunas, inf_colunas


# 2. VAREREDURA DE QUALIDADE
def varredura_dados(df_entrada):
    # Cria uma cópia para evitar alterações no DataFrame original (evita avisos de memória)
    df_limpo = df_entrada.copy()

    # Lista de strings com variações de falhas textuais e nulos
    padroes_invalidos = [
        r'^\s*$',   # Expressão regular para texto vazio ou espaços em branco
        'NaN', 'nan', 'null', 'none', 
        'N/A', 'n/a', 'na', 'NA', 
    ]

    # Substitui os padrões da lista pelo nulo oficial do Pandas (<NA>)
    df_limpo = df_limpo.replace(
        padroes_invalidos, 
        value=pd.NA, 
        regex=True, # Necessário para ativar o motor de regex do padrão r'^\s*$'
    )

    # Filtra negativos: mantém valores >= 0 e transforma os menores em NaN
    colunas_numericas = df_limpo.select_dtypes(include=['number']).columns
    for coluna in colunas_numericas:
        df_limpo[coluna] = df_limpo[coluna].where(df_limpo[coluna] >= 0)

    # Relatório de diagnóstico contando os nulos antes e depois da limpeza
    relatorio = pd.DataFrame({
        'DF_nulos_antes'  : df_entrada.isna().sum(),
        'DF_nulos_varredura' : df_limpo.isna().sum(),
        'pct_falhas'   : (df_limpo.isna().sum() / len(df_limpo) * 100).round(2),
    })

    return df_limpo, relatorio


dados = [
    {"cliente": "Carlos", "cidade": "São Paulo", "estado": "SP", "categoria": "Notebook", "valor_compra": 4500},
    {"cliente": "Amanda", "cidade": "Rio de janeiro ", "estado": "RJ", "categoria": "Monitor", "valor_compra": 1200},
    {"cliente": "Lucas", "cidade": "São Paulo", "estado": "SP", "categoria": "Mouse", "valor_compra": 85},
    {"cliente": "Fernanda", "cidade": "Curitiba", "estado": "PR", "categoria": "Cadeira Gamer", "valor_compra": 1590},
    {"cliente": "Bruno", "cidade": None, "estado": None, "categoria": "Headset", "valor_compra": 420},
    {"cliente": "Beatriz", "cidade": "São Paulo", "estado": "SP", "categoria": "Notebook", "valor_compra": 3800},
    {"cliente": "Thiago", "cidade": "Rio de Janeiro", "estado": "RJ", "categoria": "Mouse", "valor_compra": -90},
    {"cliente": "Camila", "cidade": "São Paulo", "estado": "SP", "categoria": "Notebook", "valor_compra": 4100},
    {"cliente": "Felipe", "cidade": "Manaus", "estado": "AM", "categoria": "Cadeira Gamer", "valor_compra": "NaN"},
    {"cliente": "Larissa", "cidade": "Belo Horizonte", "estado": "MG", "categoria": "Headset", "valor_compra": 390},
    {"cliente": "", "cidade": "Curitiba", "estado": "PR", "categoria": "Teclado", "valor_compra": 250},
    {"cliente": "Letícia", "cidade": "São Paulo", "estado": "SP", "categoria": "Notebook", "valor_compra": 4900},
    {"cliente": "Gustavo", "cidade": "Salvador", "estado": "BA", "categoria": "Teclado", "valor_compra": 280},
    {"cliente": "Priscila", "cidade": "Rio de Janeiro", "estado": "SP", "categoria": "Mouse", "valor_compra": 110},
    {"cliente": "Mateus", "cidade": "Manaus", "estado": "AM", "categoria": "Notebook", "valor_compra": 0},
    {"cliente": "Isabela", "cidade": "Curitiba", "space": "PR", "categoria": "Notebook", "valor_compra": 4200},
    {"cliente": "Leonardo", "cidade": "Belo Horizonte", "estado": "MG", "categoria": "Headset", "valor_compra": 310},
    {"cliente": "Bianca", "cidade": "Salvador", "estado": "BA", "categoria": "Cadeira Gamer", "valor_compra": 1480},
    {"cliente": "Diego", "cidade": "Manaus", "estado": "AM", "categoria": "Mouse", "valor_compra": 343000},
    {"cliente": "Carolina", "cidade": "Rio de Janeiro", "estado": "RJ", "categoria": "Headset", "valor_compra": 330}
]
df_dados = pd.DataFrame(dados)


# --- EXECUÇÃO DO PIPELINE DE DADOS ---
tot_registros, tot_colunas, colunas = inspecao(df_dados)
df_dados_limpo, relatorio_erros = varredura_dados(df_dados)


# --- INSPEÇÕES DOS DADOS ---
print("==" * 35)
print(f'{"BASE DE DADOS CARREGADA":^70}')
print("==" * 35)
print()

print("=-" * 35)
print(f'{"INSPEÇÃO":^70}')
print("=-" * 35)
print(df_dados)
print()
print(f"Quantidade de registros: {tot_registros}")
print(f"Quantidade de linhas: {tot_colunas}")
print(f"Matriz: {df_dados.shape}\n")
for coluna in colunas:
    print(f"{coluna} --> {df_dados[coluna].dtype}")
print()

print("=-" * 35)
print(f'{"VARREDURA DOS DADOS":^70}')
print("=-" * 35)
print(relatorio_erros)
print()


# Converte a coluna para tipo numérico; textos inválidos residuais viram NaN
df_dados_limpo["valor_compra"] = pd.to_numeric(df_dados_limpo["valor_compra"], errors="coerce")
# Aplica máscara global para exibir valores numéricos flutuantes no formato R$ 0.00
pd.options.display.float_format = 'R$ {:,.2f}'.format

print("=-" * 35)
print(f'{"RELATÓRIO GERENCIAL":^70}')
print("=-" * 35)

# 1. Análise por Estado
print("\n[ ESTADO ]")
df_estado = df_dados_limpo.groupby("estado")["valor_compra"].agg(
    Total="sum", Qtd_Vendas="count", Média="mean", Máximo="max", Mínimo="min"
)
print(df_estado.to_string())

# 2. Análise por Cidade
print("\n[ CIDADE - Faturamento por Cidade ]")
df_cidade = df_dados_limpo.groupby("cidade")["valor_compra"].agg(
    Total="sum", Qtd_Vendas="count", Média="mean", Máximo="max", Mínimo="min"
)
print(df_cidade.to_string())

# 3. Análise por Categoria
print("\n[ CATEGORIA - Categorias mais Lucrativas ]")
df_categoria = df_dados_limpo.groupby("categoria")["valor_compra"].agg(
    Total="sum", Máximo="max", Mínimo="min"
).sort_values(by="Total", ascending=False) # Ordenação decrescente pelo faturamento total
print(df_categoria.to_string())

# 4. Ranking de Faturamento
print("\n[ RANKING - Cidades que mais Faturaram ]")
df_ranking = df_dados_limpo.groupby("cidade")["valor_compra"] \
    .sum() \
    .sort_values(ascending=False) \
    .to_frame(name="Faturamento Total") # Converte a Series gerada em DataFrame para exibição tabular
print(df_ranking.to_string())

print("\n" + "=-" * 35)
