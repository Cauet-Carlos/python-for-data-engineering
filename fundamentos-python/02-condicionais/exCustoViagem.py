print("Distância da viagem\n")

distancia = float(input("Informe a distância da sua viagem (Km): "))

if distancia <= 200:
    preco = distancia * 0.50
else:
    preco = distancia * 0.45

print(f"O valor da sua passagem é: R${preco:.2f}")