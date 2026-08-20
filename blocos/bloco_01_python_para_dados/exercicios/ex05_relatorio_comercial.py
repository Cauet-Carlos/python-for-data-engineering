def titulo():
    print("=" * 95)
    print(f'{"RELATÓRIO DE DESEMPENHO COMERCIAL":^95}')
    print("=" * 95)
    print(f"{'CLIENTE':<28} | {'FATURAMENTO':^18} | {'REGIÃO':^15} | {'CATEGORIA':^15}")
    print("-" * 95)


def relatorio_cliente(info_cliente):
    faturamento_total = 0
    
    for cliente in info_cliente:
        firma = cliente["cliente"]
        faturamento = cliente["faturamento"]
        regiao = cliente["regiao"]
        faturamento_total += faturamento
        
        if faturamento >= 300000:
            status = "VIP"
        elif faturamento >= 100000:
            status = "Ouro"
        elif faturamento >= 50000:
            status = "Prata"
        else: 
            status = "Bronze"

        print(f"{firma:<28} | R$ {faturamento:>14,.2f} | {regiao:^15} | {status:^15}")

    print("=" * 95)
    return faturamento_total


def exibir_resumo_final(info_cliente, faturamento_total):
    qtd_clientes = len(info_cliente)
    maior_faturamento = 0
    nome_maior_cliente = ""

    for cliente in info_cliente:
        faturamento_cliente = cliente["faturamento"]
        if faturamento_cliente > maior_faturamento:
            maior_faturamento = faturamento_cliente
            nome_maior_cliente = cliente["cliente"]

    ticket_medio = faturamento_total / qtd_clientes if qtd_clientes > 0 else 0

    # Bloco único de indicadores estruturados
    print(f"{'RESUMO DOS INDICADORES':^95}")
    print("-" * 95)
    print(f" Total de Clientes Atendidos: {qtd_clientes:<15}")
    print(f" Faturamento Bruto Total:    R$ {faturamento_total:>14,.2f}")
    print(f" Ticket Médio por Cliente:   R$ {ticket_medio:>14,.2f}")
    print(f" Maior Conta Comercial:      {nome_maior_cliente} (R$ {maior_faturamento:,.2f})")
    print("=" * 95)


# Lista de dados utilizada
clientes_faturamento = [
    {"cliente": "Tech Inovação Ltda", "faturamento": 150000.00, "regiao": "Sudeste"},
    {"cliente": "Logística Expressa", "faturamento": 45000.50, "regiao": "Sul"},
    {"cliente": "Alimentos Saborosos", "faturamento": 85200.00, "regiao": "Nordeste"},
    {"cliente": "Construções Seguras", "faturamento": 320000.00, "regiao": "Centro-Oeste"},
    {"cliente": "Farma Vida", "faturamento": 12500.00, "regiao": "Norte"},
    {"cliente": "Varejo Total", "faturamento": 95000.00, "regiao": "Sudeste"},
    {"cliente": "Metalúrgica Central", "faturamento": 210000.00, "regiao": "Sul"},
    {"cliente": "Soluções Digitais", "faturamento": 63000.00, "regiao": "Nordeste"},
    {"cliente": "Agro Forte", "faturamento": 540000.00, "regiao": "Centro-Oeste"},
    {"cliente": "Moda Elegante", "faturamento": 28000.00, "regiao": "Sudeste"}
]

# Execução do sistema unificado
titulo()
total_faturado = relatorio_cliente(clientes_faturamento)
exibir_resumo_final(clientes_faturamento, total_faturado)
