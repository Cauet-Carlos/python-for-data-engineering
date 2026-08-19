print("--"*15)
print("\nBEM VINDO AO BANCO MASTER\n")
print("--"*15)

cont_saldo = 200

while True:
    print("\n1 - Saldo")
    print("2 - Deposito")
    print("3 - Saque")
    print("4 - Finalizar operação\n")

    usuario = int(input("Qual operação deseja realizar: "))
    
    if usuario == 1:
        print(f"\nSaldo atual: R$ {cont_saldo}")
        print("Deseja realizar outra operação?")
        print("1 - Sim (Voltar ao menu)")
        print("2 - Não (Finalizar)")
        
        escolha = int(input("Escolha: "))
        if escolha == 2:
            break
        continue # Volta para o início do while e mostra o menu de novo

    elif usuario == 2:
        deposito = int(input("Qual valor deseja depositar: R$ "))
        while deposito <= 0:
            print("Valor Inválido!")
            deposito = int(input("Qual valor deseja depositar: R$ "))
        
        cont_saldo += deposito # Atualiza o saldo diretamente
        print(f"\nDepósito de R$ {deposito} realizado com sucesso!")
        print(f"Novo saldo: R$ {cont_saldo}")

    elif usuario == 3:
        print(f"\nSaldo disponível: R$ {cont_saldo}")
        verificacao = input("Deseja sacar? (S/N): ").strip().upper()
        
        if verificacao == "S":
            valor_saque = int(input("Valor do saque: R$ "))

            if valor_saque <= cont_saldo:
                cont_saldo -= valor_saque
                total = valor_saque
                cedula = 50
                tot_ced = 0

                while True:
                    if total >= cedula:
                        total -= cedula
                        tot_ced += 1
                    else:
                        if tot_ced > 0:
                            print(f"Entregando {tot_ced} cédulas de R${cedula}")
                        if cedula == 50: cedula = 20
                        elif cedula == 20: cedula = 10
                        elif cedula == 10: cedula = 1
                        tot_ced = 0
                        if total == 0: break
                print(f"Saque finalizado. Saldo atual: R${cont_saldo}")
            else:
                print("Saldo insuficiente!")

    elif usuario == 4:
        break # Sai do loop principal e encerra o programa

print("\n" + "--"*15)
print("OBRIGADO POR USAR O BANCO MASTER!")
print("--"*15)







                
        

        
