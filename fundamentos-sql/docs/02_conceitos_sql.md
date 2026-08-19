# Conceitos SQL Aplicados

Este repositório foi desenvolvido com foco em prática analítica utilizando SQL aplicado a um cenário de e-commerce.

Os exercícios foram organizados por níveis e temas amplamente utilizados em ambientes de análise de dados, BI e engenharia de dados.

---

# Fundamentos SQL

Conceitos praticados:

- SELECT
- WHERE
- ORDER BY
- DISTINCT
- LIMIT
- BETWEEN
- LIKE
- IS NULL
- operadores lógicos

Objetivos:
- filtragem de dados;
- ordenação;
- consultas básicas;
- manipulação inicial de tabelas.

---

# JOINS

Tipos utilizados:

- INNER JOIN
- LEFT JOIN
- CROSS JOIN

Aplicações:
- relacionamento entre clientes e pedidos;
- associação entre produtos e vendas;
- identificação de registros inexistentes;
- cálculo de faturamento.

Principais análises:
- produtos não vendidos;
- clientes sem pedidos;
- quantidade de vendas por produto;
- faturamento por pedido;
- Comparações de médias com faturamentos.

---

# Análise Temporal

Funções utilizadas:

- YEAR()
- MONTH()

Métricas desenvolvidas:

- faturamento mensal;
- ticket médio;
- crescimento percentual;
- acumulado mensal;
- média móvel;
- ranking mensal.

Objetivos:
- análise histórica;
- identificação de tendências;
- comparação entre períodos.

---

# Subqueries

Estruturas utilizadas:

- subqueries no WHERE;
- subqueries no FROM;
- EXISTS;
- NOT EXISTS;
- subqueries correlacionadas.

Aplicações:
- comparação com médias;
- identificação de exceções;
- análises condicionais;
- filtros analíticos.

---

# CTEs (Common Table Expressions)

Objetivos:
- modularização de consultas;
- reutilização de lógica;
- melhoria de legibilidade;
- construção de pipelines analíticos.

Aplicações:
- segmentação de clientes;
- cálculo de ticket médio;
- crescimento mensal;
- ranking de faturamento.

---

# Window Functions

Funções utilizadas:

- RANK()
- DENSE_RANK()
- ROW_NUMBER()
- LAG()
- LEAD()
- FIRST_VALUE()
- NTILE()
- AVG() OVER()
- SUM() OVER()

Aplicações:
- rankings;
- análises temporais;
- acumulados;
- médias móveis;
- segmentação de clientes;
- comparações entre períodos.

---

# Métricas Desenvolvidas

Durante os exercícios foram calculadas métricas como:

- faturamento;
- ticket médio;
- quantidade de pedidos;
- crescimento percentual;
- média mensal;
- acumulados;
- ranking de clientes;
- ranking de faturamento;
- segmentação de clientes.

---

# Objetivo Técnico

Os exercícios foram desenvolvidos com foco em:

- raciocínio analítico;
- construção de queries complexas;
- organização de consultas;
- prática de SQL analítico;
- preparação para projetos de dados.