print("\nFASE DE VERIFICAÇÃO\n")
print("Preenchimento do ano do nascimento:")

from datetime import date

ano_atual = date.today().year # Pega o ano atual automaticamente
cont_maioridade = 0
cont_minoridade = 0

for cont in range(1,8):
    ano_nasc = int(input(f"Informe o ano de nascimento da {cont}ª pessoa: "))
    if ano_nasc < 1900 or ano_nasc < ano_atual:
        print("Ano de nascimento inválido!")
    
    idade = ano_atual - ano_nasc
    if idade >= 18:
        cont_maioridade += 1 # Adiciona 1 à contagem de maiores
    else:
        cont_minoridade += 1 # Adiciona 1 à contagem de menores

print(f"\nTotal que alcançou a maioridade: {cont_maioridade}")
print(f"\nTotal que não alcançou a maioridade: {cont_minoridade}")