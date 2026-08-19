num = int(input("Digite um número: "))

print(f"\nTABUADA DO {num}:")

for contador in range(1, 11):
    resultado = num * contador  # Calcula o valor real da tabuada
    print(f"{num} x {contador:2} = {resultado}") # Uso do :2 para alinnhar a fileira do contador
