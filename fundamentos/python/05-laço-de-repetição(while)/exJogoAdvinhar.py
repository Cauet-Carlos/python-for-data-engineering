import random

print("\nJOGO DA ADVINHAÇÃO\n")

# Escolha dos números dos jogadores 
num_computador = random.randint(1,5) # Função de escolha automatica do computador entre o intervalo definido
num_jogador = int(input("Digite um número entre (1, 2, 3, 4 ou 5): "))
cont_palpites = 0

# Inicio do loop de verificação e comparação dos números escolhidos
while num_jogador != num_computador:
    num_jogador = int(input("NÚMERO ERRADO! Digite novamente: "))
    cont_palpites += 1

print(f"\nParabéns, você acertou!\n")
print(f"Número Computador: {num_computador}\nQuantidade de palpites: {cont_palpites}")
    
