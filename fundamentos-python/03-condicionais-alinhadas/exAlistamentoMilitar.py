print("\nALISTAMENTO MILITAR")

nome = str(input("Informe seu nome: "))
print(f"\nOlá {nome}. Vamos verificar o status do seu alistamento.")

# Verificação da idade do individuo 
ano_nascim = int(input("\nInfome o ano do seu nascimento: "))
ano_atual = 2026
idade = ano_atual - ano_nascim
print(f"Sua idade: {idade} anos")

# Analise do alistamento
if idade == 18:
    condicao_fisica = input("Possui algum problema físico (sim ou não): ").strip().lower()
    if condicao_fisica in ["não", "nao", "n"]:
        print(f"\n{nome}, você está apto para se alistar!")
    elif condicao_fisica in ["sim", "s"]:
        print(f"\n{nome}, infelizmente você não está apto por conta da condição física.")
    else:
        print("\nResposta inválida. Por favor, responda Sim ou Não.") 
elif idade < 18:
    print(f"\n{nome}: Idade não apropriada para se alistar")
    prazo_restante = 18 - idade
    print(f"Tempo que falta para seu alistamento: {prazo_restante} anos")
else:
    print(f"\n{nome} seu tempo de alistamento passou do prazo!")        
    prazo_atrasado = idade - 18
    print(f"passou do prazo: {prazo_atrasado} anos")


