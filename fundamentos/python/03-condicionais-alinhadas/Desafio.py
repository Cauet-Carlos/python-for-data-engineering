print("\nJOGO PEDRA, PEPEL E TESOURA\n")

# Escolha da jogada do computador

import random # Módulo nativo para gerar dados aleatórios
opcoes = ["pedra", "papel", "tesoura"] 
escolha_computador = random.choice(opcoes) # Variavel irá percorrer a biblioteca e escolher uma opção / choice escolhe item aleatorio de uma LISTA

# Escolha do jogador
escolha_jogador = input("Escolha pedra, papel ou tesoura: ").strip().lower()
if escolha_jogador not in opcoes:
    print("Jogada invalida. Digite uma das opções acima!")
else:
    print(f"\nComputador escolheu: {escolha_computador}")
    print(f"Você escolheu: {escolha_jogador}\n")

# Processamento das jogadas

# Formas do jogador ganhar
vitoria_jogador = (escolha_jogador == "pedra" and escolha_computador == "tesoura") or \
                  (escolha_jogador == "papel" and escolha_computador == "pedra") or \
                  (escolha_jogador == "tesoura" and escolha_computador == "papel")

if escolha_jogador == escolha_computador:
    print("\nEmpate")
elif vitoria_jogador:
    print(f"\n{escolha_jogador.capitalize()} vence o computador!")
else:
    print(f"\nO computador venceu com {escolha_computador}!")

