import pandas as pd

def inspecao(analise_DataFrame):
    # Variáveis que vão receber os dados do shape e columns
    registros, colunas = analise_DataFrame.shape
    inf_colunas = analise_DataFrame.columns.tolist()

    return registros, colunas, inf_colunas


def qualidade_dados(DataFrame):
    df_varredura = DataFrame.copy()

    # Identificando padrões inválido para serem analisados
    padros_invalidos = [
        r'^\s*$', r'^Nan$', r'^nan$', r'^null$', r'^none$',
        r'^N/A$', r'^n/a$', r'^NA$', r'^na$'
     ]
    
    # Substituição dos padrões textuais inválidos por nulos nativos do Pandas
    df_varredura = df_varredura.replace(
        padros_invalidos,
        value=pd.NA,
        regex=True
    )

    # Verifica colunas numéricas e transforma valores negativos em nulos
    colunas_numericas = df_varredura.select_dtypes(include=["number"]).columns
    for coluna in colunas_numericas:
        df_varredura[coluna] = df_varredura[coluna].where(df_varredura[coluna] >= 0)
    
    # Análise de qualidade de registros
    total_registros = len(df_varredura)
    # any(axis=1) verifica linha por linha:
    # Se existir pelo menos um valor nulo na linha, retorna True
    linhas_invalidas = df_varredura.isna().any(axis=1)
    qtd_invalidas = linhas_invalidas.sum()
    qtd_validas = total_registros - qtd_invalidas
    pct_erros = round((qtd_invalidas / total_registros) * 100, 2)

    # Relatório gerencial de qualidade dos dados
    relatorio_erros = pd.DataFrame({
        "qtd_registros": [total_registros],
        "qtd_invalidos": [qtd_invalidas],
        "qtd_validos": [qtd_validas],
        "percentual_erros": [pct_erros]
    })

    # Remove qualquer linha que tenha restado com valores nulos
    df_limpo = df_varredura.dropna()

    # Garantia de que IDs não fiquem salvos como inteiros
    if "id_cliente" in df_limpo.columns:
        df_limpo["id_cliente"] = df_limpo["id_cliente"].astype("Int64")

    return df_limpo, relatorio_erros


def consolidar_dados(DataFrame_clientes, DataFrame_vendas):
    df_ligacao= DataFrame_clientes.merge(
        DataFrame_vendas,
        on="id_cliente",
        how="inner"
    )

    return df_ligacao


def kpis_executivos(df_ligacao):
    # KPI 01 - Faturamento Total
    fat_total = df_ligacao["valor_compra"].sum()

    # KPI 02 - Ticket Médio
    tict_med = df_ligacao["valor_compra"].mean()

    # KPI 03 - Faturamento por Cidade
    fat_cidade = (
        df_ligacao.groupby("cidade")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
    )

    # KPI 04 - Faturamento por Segmento
    fat_seg = (
        df_ligacao.groupby("segmento")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
    )

    # KPI 05 - Faturamento por Categoria
    fat_cat = (
        df_ligacao.groupby("categoria")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
    )

    # KPI 06 - Top 3 Clientes
    top_3 = (
        df_ligacao.groupby("cliente")["valor_compra"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
    )

    # KPI 07 - Cidade Líder de Faturamento
    lider_fat_cidade = fat_cidade.idxmax()

    # KPI 08 - Categoria Mais Rentável
    cat_mais_rentavel = fat_cat.idxmax()

    return (
        fat_total, 
        tict_med, 
        fat_cidade, 
        fat_seg, 
        fat_cat, 
        top_3, 
        lider_fat_cidade, 
        cat_mais_rentavel
    )


def insights_negocio(fat_total, tict_med, fat_cidade, fat_seg, fat_cat, top_3_clientes, lider_fat_cidade, cat_mais_rentavel):
    seg_lider = fat_seg.idxmax()
    val_cidade_lider = fat_cidade.max()
    val_cat_lider = fat_cat.max()
    val_seg_lider = fat_seg.max()
    
    # Extrai o nome e o valor do cliente número 1 do Top 3
    melhor_cliente_nome = top_3_clientes.index[0]
    melhor_cliente_val = top_3_clientes.iloc[0]

    frase_01 = f"O faturamento total acumulado do período foi de R$ {fat_total:,.2f}."
    frase_02 = f"O ticket médio por transação foi de R$ {tict_med:,.2f}."
    frase_03 = f"O faturamento por cidade é liderado por {lider_fat_cidade}, gerando R$ {val_cidade_lider:,.2f}."
    frase_04 = f"O segmento {seg_lider} concentra a maior parcela das vendas, totalizando R$ {val_seg_lider:,.2f}."
    frase_05 = f"A categoria {cat_mais_rentavel} representa a principal fonte de receita da empresa, somando R$ {val_cat_lider:,.2f}."
    frase_06 = f"O principal comprador do Top 3 clientes foi {melhor_cliente_nome}, com um total de R$ {melhor_cliente_val:,.2f} investidos."
    frase_07 = f"A cidade líder de faturamento identificada no período foi {lider_fat_cidade}."
    frase_08 = f"A categoria de produtos mais rentável para a operação foi {cat_mais_rentavel}." 
    
    return [frase_01, frase_02, frase_03, frase_04, frase_05, frase_06, frase_07, frase_08]
    

# --- RECEBIMENTO DOS DADOS ---
clientes = [
    {"id_cliente": 1, "cliente": "Ana", "cidade": "Manaus", "segmento": "Pessoa Física"},
    {"id_cliente": 2, "cliente": "João", "cidade": "Belém", "segmento": "Pessoa Jurídica"},
    {"id_cliente": 3, "cliente": "Maria", "cidade": "Manaus", "segmento": "Pessoa Física"},
    {"id_cliente": 4, "cliente": "Carlos", "cidade": "Boa Vista", "segmento": "Pessoa Física"},
    {"id_cliente": 5, "cliente": "Fernanda", "cidade": "Manaus", "segmento": "Pessoa Jurídica"},
    {"id_cliente": 6, "cliente": "", "cidade": "Macapá", "segmento": "Pessoa Física"},
    {"id_cliente": None, "cliente": "Lucas", "cidade": "Palmas", "segmento": "Pessoa Física"},
    {"id_cliente": 8, "cliente": "Amanda", "cidade": None, "segmento": "Pessoa Jurídica"},
]
df_clientes_inicial = pd.DataFrame(clientes)

vendas = [
    {"id_cliente": 1, "categoria": "Notebook", "valor_compra": 3500},
    {"id_cliente": 1, "categoria": "Mouse", "valor_compra": 120},
    {"id_cliente": 2, "categoria": "Monitor", "valor_compra": 900},
    {"id_cliente": 3, "categoria": "Notebook", "valor_compra": 4200},
    {"id_cliente": 5, "categoria": "Headset", "valor_compra": 250},
    {"id_cliente": 3, "categoria": "Teclado", "valor_compra": -150},
    {"id_cliente": 4, "categoria": "", "valor_compra": 300},
    {"id_cliente": 99, "categoria": "Webcam", "valor_compra": 450},
    {"id_cliente": 2, "categoria": "Monitor", "valor_compra": None},
]
df_vendas_inicial = pd.DataFrame(vendas)


# --- EXECUÇÃO DO PIPELINE DE DADOS ---
tot_registros_clientes, tot_colunas_clientes, colunas_clientes = inspecao(df_clientes_inicial)
tot_registros_vendas, tot_colunas_vendas, colunas_vendas = inspecao(df_vendas_inicial)

df_limpo_clientes, relatorio_erros_clientes = qualidade_dados(df_clientes_inicial)
df_limpo_vendas, relatorio_erros_vendas = qualidade_dados(df_vendas_inicial)

df_ligacao_cv = consolidar_dados(df_limpo_clientes, df_limpo_vendas)

(
    fat_total, 
    tict_med, 
    fat_cidade, 
    fat_seg, 
    fat_cat, 
    top_3_clientes, 
    lider_fat_cidade, 
    cat_mais_rentavel
) = kpis_executivos(df_ligacao_cv)

lista_de_frases = insights_negocio(
    fat_total, 
    tict_med, 
    fat_cidade, 
    fat_seg, 
    fat_cat, 
    top_3_clientes, 
    lider_fat_cidade, 
    cat_mais_rentavel
)

# --- EXIBIÇÃO DAS INFORMAÇÕES ---
print("==" * 50)
print(f'{"ETAPA 1 - INSPEÇÃO DOS DADOS":^100}')
print("==" * 50)
print()

print(df_clientes_inicial)
print()
print(f"Registros: {tot_registros_clientes} | Colunas: {tot_colunas_clientes} | Matriz: {df_clientes_inicial.shape}")
print()
for coluna_c in colunas_clientes:
    print(f"{coluna_c} -->{df_clientes_inicial[coluna_c].dtype}")
print()
print()
print(df_vendas_inicial)
print()
print(f"Registros: {tot_registros_vendas} | Colunas: {tot_colunas_vendas} | Matriz: {df_vendas_inicial.shape}")
print()
for coluna_v in colunas_vendas:
    print(f"{coluna_v} -->{df_vendas_inicial[coluna_v].dtype}")
print()


print("==" * 50)
print(f'{"ETAPA 2 - ANÁLISE DOS DADOS":^100}')
print("==" * 50)
print()
print(relatorio_erros_clientes.to_string(formatters={'percentual_erros': '{:.2f}%'.format}))
print()
print(relatorio_erros_vendas.to_string(formatters={'percentual_erros': '{:.2f}%'.format}))
print()

print("==" * 50)
print(f'{"ETAPA 3 - CONSOLIDAÇÃO DAS INFORMAÇÕES":^100}')
print("==" * 50)
print()
print(df_ligacao_cv)
print()


print("==" * 50)
print(f'{"ETAPA 4 - RELATÓRIO DE INSIGHTS EXECUTIVOS":^100}')
print("==" * 50)
for frase in lista_de_frases:
    print(frase)