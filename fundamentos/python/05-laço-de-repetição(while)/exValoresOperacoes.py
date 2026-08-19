print("\nSOMA DOS VALORES\n")

# Leitura dos valoree
n1 = int(input("Informe o primeiro valor: "))
n2 = int(input("Informe o segundo valor: "))

# Inicio do loop 
opcao = 0
while opcao != 5: # Loop se encerrará quando o usúario digitar 5

    # Menu de opções
    print("\nMENU DE OPÇÕES\n")
    print("1 - Somar")
    print("2 - multiplicar")
    print("3 - Maior")
    print("4 - Novos números")
    print("5 - Sair do programa\n")

    opcao = int(input("Escolha uma das opções: "))

    # Processamento das opções a partir da variável "opcao"
    if opcao == 1:
        soma = (n1 + n2)
        print(f"{n1} + {n2} = {soma}")
    elif opcao == 2:
        mult = n1 * n2
        print(f"{n1} * {n2} = {mult}")
    elif opcao == 3: 
        if n1 > n2:
            maior = n1
            print(f"O maior valor é {n1}")
        elif n2 > n1:
            maior = n2
            print(f"O maior valor é {n2}")
        else:
            print("Números Iguais")
    elif opcao == 4:
        n1 = int(input("Digite novamente o primeiro valor: "))
        n2 = int(input("Digite novamente o segundo valor: "))
    elif opcao < 1 or opcao > 5:
        print("\nOpção inválida. Escolha uma das opções do Menu!")
    else: 
        print("\nOperção Finalizada!")
        
        



