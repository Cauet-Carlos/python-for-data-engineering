print("\nCALCULO DO SEU IMC\n")

nome = str(input("Digite seu nome: "))
peso = float(input("Informe seu peso (kg): "))
altura = float(input("Informe sua altura: "))

# calculo do IMC
imc = peso / (altura * altura)
print(f"\nSeu IMC é: {imc:.2f}\n")


# Processando a informação
if imc < 18.5:
    print("STATUS: ABAIXO DO PESO")
elif 18.5 <= imc < 25:  
    print("STATUS: PESO IDEAL")
elif 25 <= imc < 30:
    print("STATUS: SOBREPESO")
elif 30 <= imc < 40:
    print("STATUS: OBESIDADE")
else:
    print("STATUS: OBESIDADE MÓRBIDA")
