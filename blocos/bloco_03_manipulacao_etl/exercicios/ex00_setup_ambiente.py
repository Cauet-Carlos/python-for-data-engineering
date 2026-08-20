import os # Biblioteca padrão do Python que permite ao código conversar com o seu S.O

# diretorio_atual: Pega a pasta onde o arquivo ex00_setup_ambiente.py está (03_manipulacao_arquivos_etl)
# os.path.dirname(...): Isola apenas a pasta onde o arquivo está, descartando o nome do arquivo .py
# os.path.abspath(...): Garante que esse caminho seja absoluto (completo desde o C:/ ou /user/)
# __file__: É uma variável interna do Python que guarda o caminho completo de onde o seu arquivo ex00_setup_ambiente.py está físico no seu HD

diretorio_atual = os.path.dirname(os.path.abspath(__file__))

pastas = [
    "data_lake/raw",
    "data_lake/trusted",
    "data_lake/logs",
    "scripts"
]

for pasta in pastas:
    # Junta o caminho da pasta onde o script está (diretorio_atual) com a subpasta da vez (pasta)
    caminho_completo = os.path.join(diretorio_atual, pasta)
    # os.makedirs: Cria a pasta final se as pastas anteriores do caminho não existirem
    # exist_ok=True: Evita que o programa dê erro e trave se você rodar o script pela segunda vez e as pastas já existirem
    os.makedirs(caminho_completo, exist_ok=True)

print("Estrutura criada com sucesso no lugar certo!")


