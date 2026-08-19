print("\nCALCULO DO VALOR DO PRODUTO\n")

produto = str(input("Informe o nome do produto: "))
preco = float(input("Valor da compra: "))

print("\nFORMAS DE PAGAMENTO:")
print("1 - À vista (Dinheiro/Pix)")
print("2 - À vista no cartão")
print("3 - 2x no cartão")
print("4 - 3x ou mais no cartão")

opcao = int(input("Digite o número da opção do pagamento: "))

if opcao == 1:
    total = preco - (preco * 0.10) # Desconto de 10% ao total
    print(f"Sua compra de R$ {preco:.2f} vai custar R$ {total:.2f} no final.")

elif opcao == 2:
    total = preco - (preco * 0.05) # Desconto de 5% ao total
    print(f"Sua compra de R$ {preco:.2f} vai custar R$ {total:.2f} no final.")

elif opcao == 3:
    parcela = preco / 2 # Dividindo o valor em 2x
    print(f"Sua compra será parcelada em 2x de R$ {parcela:.2f} SEM JUROS.")

elif opcao == 4:
    total = preco + (preco * 0.20) # Adiciona 20% ao total
    total_parcelas = int(input("Quantas parcelas? "))
    
    if total_parcelas >= 3: # Avalia a condição para que as parcelas sejam acima ou igual à 3
        valor_parcela = total / total_parcelas # Divide o valor com juros pelo total de parcelas
        print(f"Sua compra será parcelada em {total_parcelas}x de R$ {valor_parcela:.2f} COM JUROS.")
        print(f"Sua compra de R$ {preco:.2f} vai custar R$ {total:.2f} no final.")
    else:
        print("Para esta opção, o mínimo são 3 parcelas.")
else:
    print("Opção inválida de pagamento!")


