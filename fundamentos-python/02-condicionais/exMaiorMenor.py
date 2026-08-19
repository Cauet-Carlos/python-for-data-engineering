num1 = int(input("Informe o 1ª número: "))
num2 = int(input("Informe o 2ª número: "))
num3 = int(input("Informe o 3ª número: "))

# Testando quem é o maior
maior = num1
if num2 > num1 and num2 > num3:
    maior = num2
if num3 > num1 and num3 > num2:
    maior = num3

# Testando quem é o menor
menor = num1
if num2 < num1 and num2 < num3:
    menor = num2
if num3 < num1 and num3 < num2:
    menor = num3

print(f"O maior valor digitado foi {maior}")
print(f"O menor valor digitado foi {menor}")
