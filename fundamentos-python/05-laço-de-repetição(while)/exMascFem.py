print("\nMasculino ou Feminino\n")
  
# Lê o sexo pela primeira vez
sexo = str(input('Informe seu sexo [M/F]: ')).strip().upper()

# Enquanto não for 'M' E não for 'F' pede novamente
while sexo not in 'MF':
    sexo = str(input('Dados inválidos. Por favor, informe seu sexo [M/F]: ')).strip().upper()

print(f'Sexo registrado com sucesso!')


