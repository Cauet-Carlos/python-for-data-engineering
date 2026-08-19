print("\nINTERVALO DOS NÚMEROS iMPARES ENTRE 1 E 500\n")

soma = 0

# Inicio do loop entre 1 e 500
for cont in range(1,501): 
    if cont % 2 == 1: # Contador que irá percorrer os numeros impares
        num_ipmpar = cont # Variavel que irá receber os números impares
        if num_ipmpar % 3 == 0: # Numeros impares divisiveis por 3
            soma += num_ipmpar # Variavel que irá armazenar e somar
print(f"Soma entre os números ímpares múltiplos de 3: {soma}")
            