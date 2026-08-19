import pandas as pd

conteudo_csv = """id,nome,email,status
1,Carlos,carlos@email.com,Ativo
2,Ana,,Inativo
3,João,joao@email.com,Ativo
3,João,joao@email.com,Ativo
4,Pedro,pedro@email.com,Ativo
5,Maria,,Inativo
"""

with open("clientes.csv", "w", encoding="utf-8") as arquivo_escrita:
    arquivo_escrita.write(conteudo_csv)

df_clientes = pd.read_csv("clientes.csv")


def inspecao_df(df):
    dimensao = df.shape
    qtd_nulos = df.isna().sum().sum()
    qtd_duplicados = df.duplicated().sum()
    registros_duplicados = df[df.duplicated()]

    return (
        dimensao, 
        qtd_nulos, 
        qtd_duplicados, 
        registros_duplicados
    )

def limpeza_df(varredura_df):
    df_limpo = varredura_df.copy()

    df_limpo = df_limpo.drop_duplicates()
    df_limpo = df_limpo.dropna(subset=["email"])
    df_limpo = df_limpo[df_limpo["status"] == "Ativo"]

    return df_limpo



dimensao, qtd_nulos, qtd_duplicados, registros_duplicados = inspecao_df(df_clientes)
df_limpo = limpeza_df(df_clientes)


df_limpo.to_csv(
    "clientes_tratados.csv",
    index=False
)


print("=="*30)
print("Inspeção de qualidade") 
print("=="*30) 

print(f"Dimensão: {dimensao}") 
print(f"Quantidade de vazios/nulos: {qtd_nulos}") 
print(f"Quantidade de duplicados: {qtd_duplicados}") 
print("") 
print(registros_duplicados)
print("")

print("==" * 30)
print("Dados Após a Limpeza")
print("==" * 30)
print(df_limpo)