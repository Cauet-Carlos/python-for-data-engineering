def titulo(dia):
    print("-" * 30)
    print(f'{"VALIDAÇÃO DE VENDAS":^30}')
    print(f'{f"DADOS DO DIA {dia}":^30}')
    print("-" * 30)


def verificao_vendas(lista_de_vendas):
    cont_registros_validos = 0
    cont_registros_n_validos = 0
    for venda in lista_de_vendas:
        if venda > 0:
            cont_registros_validos += 1
        else:
            cont_registros_n_validos += 1
    print(f"Registros válidos: {cont_registros_validos}")
    print(f"Registros inválidos: {cont_registros_n_validos}")

# Dados a serem analisados 
vendas_day_1 = [100, 56, -35, 458, 0, -80, 0, 524, 231, 349]
vendas_day_2 = [-1369, 0, -254, 251, 0, -98, 100, 395, -142, 221]
vendas_day_3 = [223, 102, 100, 200, 150, -658, 0, 0, 758, 997]

# Execução do código
titulo(1)
verificao_vendas(vendas_day_1)
print("\n")
titulo(2)
verificao_vendas(vendas_day_2)
print("\n")
titulo(3)
verificao_vendas(vendas_day_3)