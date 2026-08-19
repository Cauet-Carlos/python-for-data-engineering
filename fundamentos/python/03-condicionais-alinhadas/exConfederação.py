print("\nCONFEDERAÇÃO NACIONAL DE NATAÇÃO\n")
print("ANALISE DE CATEGORIA")

nome = str(input("Informe seu nome: "))
ano_nasc = int(input("Informe o ano de nascimento do atleta(a): "))

idade = 2026 - ano_nasc
print(f"\n{nome}: {idade} anos")

if idade <= 9:
    print("CATEGORIA: MIRIM")
elif idade <= 14: 
    print("CATEGORIA: INFANTIL")
elif idade <= 19: 
    print("CATEGORIA: JÚNIOR")
elif idade == 20:
    print("CATEGORIA: SÊNIOR")
else:
    print("CATEGORIA: MASTER")
