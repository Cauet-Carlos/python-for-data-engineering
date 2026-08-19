num = int(input("Digite um número: "))
total_divisores = 0

for c in range(1, num + 1):
    if num % c == 0:
        print(f"\033[33m{c}\033[m", end=" ") # Amarelo se for divisor
        total_divisores += 1
    else:
        print(f"\033[31m{c}\033[m", end=" ") # Vermelho se não for

print(f"\n\nO número {num} foi dividido {total_divisores} vezes.")

if total_divisores == 2:
    print("E por isso ele É PRIMO!")
else:
    print("E por isso ele NÃO É PRIMO!")
