import pandas as pd


def inspecao_inicial(analise_dados):
    linhas, colunas = analise_dados.shape
    colunas_frame = analise_dados.columns.tolist()
    
    return linhas, colunas, colunas_frame


def verificacao_qualidade(investigacao_df):
    # 1. ANÁLISE DAS COLUNAS 
    clientes_nulos = investigacao_df["cliente"].isna()
    clientes_vazios = investigacao_df["cliente"].fillna("").str.strip() == ""
    
    # Tratando nulos, vazios e o texto literal "None"
    cidades_nulos = investigacao_df["cidade"].isna() | (investigacao_df["cidade"] == "None")
    cidades_vazias = investigacao_df["cidade"].fillna("").str.strip() == ""
    
    valores_nulos = investigacao_df["valor_compra"].isna()
    valores_negativos = investigacao_df["valor_compra"] < 0

    # 2. CONTAGEM DOS VALORES
    total_clientes_nulos = clientes_nulos.sum()
    total_clientes_vazios = clientes_vazios.sum()
    total_cidades_nulos = cities_nulos = cidades_nulos.sum()
    total_cidades_vazias = cidades_vazias.sum()
    total_valores_nulos = valores_nulos.sum()
    total_valores_negativos = valores_negativos.sum()

    # 3. SEPARAÇÃO DOS REGISTROS INVÁLIDOS
    linhas_invalidas = (
        clientes_nulos
        | clientes_vazios
        | cidades_nulos
        | cidades_vazias
        | valores_nulos
        | valores_negativos
    )

    # 4. REALIZA A INVERSÃO DAS LINHAS INVÁLIDAS PARA GERAR AS VÁLIDOS
    df_validos = investigacao_df[~linhas_invalidas]
    df_total_clientes_validos = df_validos.copy()
    total_validos = len(df_total_clientes_validos)

    return (
        total_clientes_nulos, 
        total_clientes_vazios, 
        total_cidades_nulos, 
        total_cidades_vazias, 
        total_valores_nulos, 
        total_valores_negativos, 
        total_validos, 
        df_total_clientes_validos,
        linhas_invalidas,  
        df_validos         # 
    )


def consultas_comerciais(total_clientes_validos):
    # CONSULTA 1: Compras Acima de R$ 1.000 ordenadas da maior para a menor
    compras_acima_mil = total_clientes_validos["valor_compra"] > 1000
    df_compras_acima_mil = total_clientes_validos[compras_acima_mil]
    df_ordenado_compras_condicao = df_compras_acima_mil.sort_values("valor_compra", ascending=False)

    # CONSULTA 2: Apenas Clientes de Manaus ou Belém
    clientes_manaus = total_clientes_validos["cidade"] == "Manaus"
    clientes_manaus_belem = (total_clientes_validos["cidade"] == "Manaus") | (total_clientes_validos["cidade"] == "Belém")
    df_clientes_manaus = total_clientes_validos[clientes_manaus]
    df_clientes_manaus_belem = total_clientes_validos[clientes_manaus_belem]

    # CONSULTA 3: Clientes de Manaus com Compras Acima de R$ 1.000 (Ordenado)
    clientes_mao_mil = df_clientes_manaus["valor_compra"] > 1000
    df_clientes_mao_mil = df_clientes_manaus[clientes_mao_mil]
    df_clientes_mao_mil_ordenado = df_clientes_mao_mil.sort_values("valor_compra", ascending=False)

    # CONSULTA 4: Ranking de compras
    ranking_compras = total_clientes_validos.sort_values("valor_compra", ascending=False)

    return df_ordenado_compras_condicao, df_clientes_manaus, df_clientes_manaus_belem, df_clientes_mao_mil_ordenado, ranking_compras


def validacao_erros(linhas_invalidas_mascara, df_validos_limpo):
    total_com_problemas = int(linhas_invalidas_mascara.sum())
    total_potencialmente_validos = int(len(df_validos_limpo))

    return total_com_problemas, total_potencialmente_validos


dados = [
    {"cliente": "Ana", "cidade": "Manaus", "categoria": "Notebook", "valor_compra": 1500},
    {"cliente": "João", "cidade": "Belém", "categoria": "Mouse", "valor_compra": 80},
    {"cliente": "Maria", "cidade": "Manaus", "categoria": "Notebook", "valor_compra": 3200},
    {"cliente": "Carlos", "cidade": "Boa Vista", "categoria": "Monitor", "valor_compra": -500},
    {"cliente": None, "cidade": "Manaus", "categoria": "Teclado", "valor_compra": 250},
    {"cliente": "Fernanda", "cidade": "None", "categoria": "Notebook", "valor_compra": 4100},
    {"cliente": "Lucas", "cidade": "Belém", "categoria": "Mouse", "valor_compra": None},
    {"cliente": "Juliana", "cidade": "Manaus", "categoria": "Monitor", "valor_compra": 950},
    {"cliente": "Gabriel", "cidade": "Boa Vista", "categoria": "Notebook", "valor_compra": 2800},
    {"cliente": "   ", "cidade": "Manaus", "categoria": "Mouse", "valor_compra": 120},
    {"cliente": "Rodrigo", "cidade": "Belém", "categoria": "Monitor", "valor_compra": 1100},
    {"cliente": "Amanda", "cidade": "   ", "categoria": "Notebook", "valor_compra": 3500}
]


df_dados = pd.DataFrame(dados)

# Execução das funções salvando os retornos necessários
qtd_registros, qtd_colunas, colunas = inspecao_inicial(df_dados)

# Capturando as duas novas variáveis finais retornadas pela verificação de qualidade
(qtd_clientes_nulos, qtd_clientes_vazios, qtd_cidades_nulos, qtd_cidade_vazios, 
 qtd_valores_nulos, qtd_valores_negativos, qtd_clentes_validos, df_clientes_validos,
 mascara_erros, tabela_limpa) = verificacao_qualidade(df_dados)

faturamento_maior_mil, clientes_manaus, clientes_manaus_belem, clientes_mao_mil, ranking = consultas_comerciais(df_clientes_validos)

qtd_problemas, qtd_validos = validacao_erros(mascara_erros, tabela_limpa)


# --- IMPRESSÕES DOS RELATÓRIOS ---
print("==" * 40)
print(f'{"BASE DE DADOS CARREGADA":^80}')
print("==" * 40)
print()

print("=-" * 40)
print(f'{"INSPEÇÃO INICIAL":^80}')
print("=-" * 40)
print(df_dados)
print()
print(f"Quantidade de registros: {qtd_registros}")
print(f"Quantidade de colunas: {qtd_colunas}")
print(f"Matriz: {df_dados.shape}\n")
for coluna in colunas:
    print(f"{coluna} -> {df_dados[coluna].dtype}\n")

print("=-" * 40)
print(f'{"INVESTIGAÇÃO DE QUALIDADE":^80}')
print("=-" * 40)
print(f"Clientes nulos:  {qtd_clientes_nulos}")
print(f"Clientes vazios: {qtd_clientes_vazios}")
print("--" * 40)
print(f"Cidades nulas:   {qtd_cidades_nulos}")
print(f"Cidades vazios:  {qtd_cidade_vazios}")
print("--" * 40)
print(f"Valores nulos:     {qtd_valores_nulos}")
print(f"Compras negativas: {qtd_valores_negativos}")
print("--" * 40)
print(f"Registros válidados: {qtd_clentes_validos}")

print("=-" * 40)
print(f'{"CONSULTAS COMERCIAIS":^80}')
print("=-" * 40)
print("Compras Acima de R$ 1.000:")
print(faturamento_maior_mil)
print("--" * 40)
print("Clientes de Manaus:")
print(clientes_manaus)
print("--" * 40)
print("Clientes de Manaus e Belém:")
print(clientes_manaus_belem)
print("--" * 40)
print("Clientes de Manaus com Compras Acima de R$ 1.000:")
print(clientes_mao_mil)
print("--" * 40)
print("Ranking de Compras:")
print(ranking)

print("=-" * 40)
print(f'{"SIMULAÇÃO DE VALIDAÇÃO DE DADOS":^80}')
print("=-" * 40)
print(f"Desafio A - Quantidade de Registros com Problemas: {qtd_problemas}")
print("--" * 40)
print(f"Desafio B - Registros Potencialmente Válidos: {qtd_validos}")
print("--" * 40)
