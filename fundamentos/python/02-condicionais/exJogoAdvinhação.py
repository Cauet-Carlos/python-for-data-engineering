import random

print("JOGO DA ADVINHAÇÃO\n")

num_escolhido = random.randint(0,5)

num_usuario = int(input("Digite um número entre 0 a 5:"))
if num_usuario == num_escolhido:
    print("Parabéns você venceu")
else:
    print("Perdeu!!")
    print(f"Número certo: {num_escolhido}")