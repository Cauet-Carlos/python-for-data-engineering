print("\nTABUADA")

# Inicio do loop de inserção do número da tabuada
while True:
    numero = int(input("\nQuer ver a tabuada de qual valor: "))

    # Parada no sistema se caso o valor for negativo
    if numero < 0:
        break
    
    # Tabuada irá iniciar em 0 devido ser o valor recebido pela variavel contador
    contador = 0
    for contador in range (1,11):
        mult = numero * contador
        print(f"{numero} x {contador} = {mult}")
        contador += 1  


