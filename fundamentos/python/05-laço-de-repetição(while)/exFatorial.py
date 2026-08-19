print("\nFATORIAL\n")

num = int(input("Digite um número: "))
fatorial = 1

while num > 1:
    fatorial *= num  # Multiplica o resultado pelo número atual
    num -= 1  # Diminui 1 do número para o próximo passo

print(f"O fatorial é: {fatorial}")