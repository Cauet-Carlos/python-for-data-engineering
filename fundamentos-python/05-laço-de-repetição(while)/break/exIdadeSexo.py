
contIdade = 0 # Contador de pessoas acima ou igual à 18 anos
contMasc = 0 # Contador para armazenar quantos homens foram informados
contFemin = 0 # Contador para armazenar quantas mulheres abaixo dos 20

while True:
    print("-"*30)
    print("CADASTRO DE PESSOAS")
    print("-"*30)

    nome = input("\nInsira seu nome: ")

    # Analise para que a idade seja válida e contabilizada
    idade = int(input("Informe sua idade: "))
    while idade < 0 or idade >= 110:
        print("Idade Inválida!")
        idade = int(input("Informe sua idade: "))
    if idade >= 18:
        contIdade += 1

    # Analise para que o sexo sejá valido e contabilizado
    sexo = input("Informe seu sexo (M/F): ").strip().upper()[0] 
    while sexo not in ("M", "F"):
        print("Sexo Inválido!")
        sexo = input("Informe seu sexo (M/F): ").strip().upper()[0] 
    if sexo == "M":
        contMasc += 1

    # Verificação para que o contador receba os dados de mulheres abaixo de 20
    if sexo == "F" and idade < 20:
        contFemin += 1

    # Condição de parada
    fim = str(input("\nDeseja continuar (S/N): \n")).strip().upper()[0]
    if fim == "N":
        print("Encerrando o programa... Até logo!")
        break  

print("-" * 30)
print(f"RESULTADO FINAL:")
print(f"Total de pessoas com mais de 18 anos: {contIdade}")
print(f"Total de homens cadastrados: {contMasc}")
print(f"Total de mulheres com menos de 20 anos: {contFemin}")
    
