print("Radar Eletrônico\n")

velocidade = float(input("Informe a velocidade do seu carro (km): "))

if velocidade > 80:
    print("Você foi multado por ultrapassar o limite de 80km/h")
    print("Multa de R$ 7,00 por km ultrapassado \n")
    excesso = velocidade - 80
    multa = excesso * 7
    print(f"Valor da multa: R${multa:.2f}")
else:
    print("Parabéns. Você estava no limite de velocidade adequado!")