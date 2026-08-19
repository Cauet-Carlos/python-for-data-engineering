import os 

# Pega a pasta onde esse arquivo está
diretorio_atual = os.path.dirname(os.path.abspath(__file__))
# sobe um nível pra chegar na pasta do projeto (03_pipeline_etl_avançado)
diretorio_final = os.path.dirname(diretorio_atual)

# Pastas que quero criar dentro do data_lake
pastas = [
    "data_lake/raw",
    "data_lake/trusted",
    "data_lake/logs"
]

# Para cada pasta, junta com o diretório final (pasta principal) e cria um único caminho com as subpastas
for pasta in pastas:
    caminho_completo = os.path.join(diretorio_final, pasta)
    os.makedirs(caminho_completo, exist_ok=True)  # exist_ok evita erro se a pasta já existir

print("Estrutura criada!")