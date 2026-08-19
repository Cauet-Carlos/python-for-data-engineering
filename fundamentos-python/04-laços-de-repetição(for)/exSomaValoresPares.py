print("\nSOMA DOS NÚMEROS PARES\n")

soma = 0

for cont in range (1,7):
    num = int(input(f"Digite o valor {cont}: "))
    if num % 2 == 0:
        num_par = num
        soma += num_par
print(f"A soma dos números pares é {soma}")