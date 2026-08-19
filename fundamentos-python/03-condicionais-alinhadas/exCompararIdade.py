print("VERIFICAÇÃO DE IDADES\n")

nome1 = str(input("Informe seu nome: "))
idade1 = int(input("Informe sua idade: "))

nome2 = str(input("\nInforme seu nome: "))
idade2 = int(input("Informe sua idade: "))

if idade1 > idade2:
    print(f"\n{nome1} é mais velho que {nome2}")
elif idade2 > idade1:
    print(f"\n{nome2} é mais velho que {nome1}")
else:
    print("\nIdade semelhante")