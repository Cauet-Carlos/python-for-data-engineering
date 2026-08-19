# Funções Analíticas Utilizadas

Este documento apresenta as principais funções analíticas aplicadas durante os exercícios SQL.

---

# Funções de Agregação

## COUNT()

Utilizada para contagem de registros.

Aplicações:
- quantidade de pedidos;
- quantidade de produtos;
- total de clientes.

---

## SUM()

Utilizada para cálculo de faturamento e acumulados.

Aplicações:
- faturamento por pedido;
- faturamento mensal;
- vendas por produto.

---

## AVG()

Utilizada para cálculo de médias.

Aplicações:
- ticket médio;
- média de faturamento;
- média por cliente.

---

# Funções Temporais

## YEAR()

Utilizada para extração do ano de datas.

---

## MONTH()

Utilizada para agrupamento mensal de métricas.

---

# Window Functions

## RANK()

Cria rankings considerando empates.

Aplicações:
- ranking de faturamento;
- ranking de clientes.

---

## DENSE_RANK()

Semelhante ao RANK(), porém sem saltos entre posições.

Aplicações:
- classificação analítica.

---

## ROW_NUMBER()

Cria numeração sequencial.

Aplicações:
- ordenação de clientes;
- classificação de pedidos.

---

## LAG()

Acessa valores anteriores da sequência.

Aplicações:
- comparação entre meses;
- crescimento percentual.

---

## LEAD()

Acessa valores posteriores da sequência.

Aplicações:
- projeção temporal;
- comparação entre períodos.

---

## FIRST_VALUE()

Retorna o primeiro valor de uma janela.

Aplicações:
- identificação do primeiro faturamento.

---

## NTILE()

Divide os registros em grupos.

Aplicações:
- segmentação de clientes;
- classificação VIP.

---

# OVER()

Cláusula responsável pela criação de janelas analíticas.

Aplicações:
- médias móveis;
- acumulados;
- rankings;
- análises temporais.

---

# PARTITION BY

Responsável pela separação lógica das análises dentro das janelas.

Aplicações:
- média por cliente;
- acumulado anual;
- rankings segmentados.

---

# CASE

Utilizado para classificações condicionais.

Aplicações:
- segmentação de clientes;
- classificação de faturamento.

---

# EXISTS e NOT EXISTS

Utilizados para verificações condicionais entre tabelas.

Aplicações:
- produtos não vendidos;
- clientes com pedidos;
- validações relacionais.

---

# Objetivo das Funções

As funções aplicadas permitiram desenvolver análises próximas de cenários reais de:

- Business Intelligence;
- Analytics Engineering;
- Engenharia de Dados;
- Análise de Dados.