print("\nINSERÇÃO DE VALORES\n")

entrada = input("Informe um número ou 'sair': ")

if entrada != "sair":
    num = int(entrada)
    maior = num
    menor = num
    soma = num
    contador = 1
    
    entrada = input("Informe outro número ou 'sair': ")
    while entrada != "sair":
        num = int(entrada)
        
        soma += num
        contador += 1
    
        if num > maior:
            maior = num
        if num < menor:
            menor = num
        
        entrada = input("Informe outro número ou 'sair': ")

    media = soma / contador
    print("\nParada no sistema!")
    print(f"Maior: {maior} | Menor: {menor} | Média: {media}")
else:
    print("Sistema encerrado sem dados.")

    

