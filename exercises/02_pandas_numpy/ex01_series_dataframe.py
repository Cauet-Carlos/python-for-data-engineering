import pandas as pd

# Lista de dados suja para análise
dados = {
    "cliente": [
        "Ana",
        "João",
        "   ",
        "Carlos",
        "Fernanda",
        "Lucas",
        None,
        "Rodrigo",
        "Juliana",
        "Gabriel",
    ],

    "cidade": [
        "Manaus",
        "Manaus",
        "Belém",
        "Boa Vista",
        "Manaus",
        "   ",
        "Boa Vista",
        "Manaus",
        "Belém",
        "Boa Vista",
    ],

    "valor_compra": [150, 300, 450, -200, 600, 120, 250, None, 400, 180],
}


def titulo(nome):
    # Variável para receber a quantidade de letras do parâmetro e adicionar mais dez
    tamanho = len(nome) + 10
    print("=" * tamanho)
    print(f'{nome:^{tamanho}}')
    print("=" * tamanho)


def limpeza_dados(varredura):
    # lista vazia para guardar as linhas que passarem no teste
    registros_validos = []

    # iterrows() percorre o DataFrame linha por linha (id é o índice, linha é o conteúdo)
    for id, linha in varredura.iterrows():

        # 1. CRIAÇÃO DAS VARIAVEIS 
        cliente = linha["cliente"]
        cidade = linha["cidade"]
        valor = list([linha["valor_compra"]])[0] 

        # 2. VERIFICAÇÃO SE A VARIÁVEL É DO TIPO TEXTO
        # Uso do isinstance para realizar essa verificação 
        if isinstance(cliente, str):
            cliente = cliente.strip() # Retira espaços indesejados através do strip
        if isinstance(cidade, str):
            cidade = cidade.strip() # Retira espaços indesejados através do strip

        # 3. VERIFICAÇÃO DE REGISTROS NULOS, VAZIOS OU NEGATIVOS 
        # Analisa e verifica se cliente está nulo (pd.isna) ou em branco
        if pd.isna(cliente) or cliente == "":
            continue
        # Analisa e verifica se cidade está nulo (pd.isna) ou em branco
        if pd.isna(cidade) or cidade == "":
            continue
        # Analisa e verifica se valor está nulo (pd.isna) ou negativo
        if pd.isna(valor) or valor < 0:
            continue # 
        
        # 4. INSERI A LINHA VERIFICADA E APROVADA (VALIDAÇÃO) NA LISTA
        registros_validos.append({
            "cliente": cliente,
            "cidade": cidade,
            "valor_compra": valor
        })

    # Cria um dataframe limpo para receber a lista
    df_limpo = pd.DataFrame(registros_validos)
    
    return df_limpo


# RESULTADO FINAL
df_vendas = pd.DataFrame(dados)
df_verificado = limpeza_dados(df_vendas)


nome_titulo = str(input("Qual o nome do título: "))
titulo(nome_titulo)

linhas, colunas = df_verificado.shape
print(f"\nQuantidade de registros: {linhas}")
print(f"Quantidade de colunas: {colunas}\n")

print("Campos:")
for coluna in df_verificado.columns:
    print(f"- {coluna}")

print("\nTipos:")
for coluna in df_verificado.columns:
    print(f"{coluna} -> {df_verificado[coluna].dtype}")

media_compras = df_verificado["valor_compra"].mean()
maior_compra = df_verificado["valor_compra"].max()
menor_compra = df_verificado["valor_compra"].min()

print(f"\nValor médio das compras: R$ {media_compras:,.2f}")
print(f"Maior compra: R$ {maior_compra:,.2f}")
print(f"Menor compra: R$ {menor_compra:,.2f}")