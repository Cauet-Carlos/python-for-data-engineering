
print("\nINFINITY\n")

num = int(input("Informe um valor (999 para parar): "))
soma = 0

# A condição verifica o número ANTES de somar
while num != 999:
    soma += num
    num = int(input("Informe um valor (999 para parar): "))

print("\nParada no sistema!")
print(f"A soma dos números: {soma}")




