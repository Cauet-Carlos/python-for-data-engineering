print("APROVAÇÃO DE EMPRÉSTIMO: CASA\n")

nome = input("Informe seu nome: ")
print(f"\nOlá, {nome}. Preencha os dados para verificarmos seu empréstimo.\n")

valor_casa = float(input("Informe o valor da casa: "))
salario = float(input("Informe seu salário mensal: "))
anos = int(input("Quantos anos você deseja pagar a casa: "))

# Cálculo prestação mensal
prestacao_mensal = valor_casa / (anos * 12)

# Limite de 30% do salário
limite = salario * 0.30

print(f"\nValor da prestação mensal: R$ {prestacao_mensal:.2f}")
print(f"Limite permitido (30% do salário): R$ {limite:.2f}")

if prestacao_mensal > limite:
    print(f"\nInfelizmente, {nome}, seu empréstimo foi NEGADO.")
else:
    print(f"\nParabéns, {nome}! Seu empréstimo foi APROVADO.")


