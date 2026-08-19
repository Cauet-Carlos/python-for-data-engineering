print("\nJOGO DO PAR OU ÍMPAR\n")

import random

vitorias = 0

while True:

    jogador_num = int(input("Diga um valor: "))
    computador_num = random.randint(0, 10)
    total = jogador_num + computador_num

    # Definição da escolha entre somente par ou impar (P/I)
    escolha = " "
    while escolha not in "PI":
        escolha = input("Par ou Ímpar? [P/I] ").strip().upper()[0] 

    print(f"Você jogou {jogador_num} e o computador {computador_num}. Total de {total}: ", end="")
    print("DEU PAR" if total % 2 == 0 else "DEU ÍMPAR")

    # Lógica de vitória
    if escolha == "P":
        if total % 2 == 0:
            print("Você VENCEU!")
            vitorias += 1
        else:
            print("Você PERDEU!")
            break
    elif escolha == "I":
        if total % 2 == 1:
            print("Você VENCEU!")
            vitorias += 1
        else:
            print("Você PERDEU!")
            break
    
    print("Vamos jogar novamente...")

print(f"GAME OVER! Você venceu {vitorias} vezes.")
