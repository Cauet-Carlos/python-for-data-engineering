# Padrões SQL Utilizados

Durante os exercícios foram utilizados padrões recorrentes de construção analítica em SQL.

---

# Padrão de Agregação

Estrutura frequentemente utilizada:

```sql
SELECT
    coluna,
    SUM(valor)
FROM tabela
GROUP BY coluna;
```

Objetivos:
- cálculo de métricas;
- análise de faturamento;
- contagem de registros.

---

# Padrão de Análise Temporal

Estrutura aplicada:

```sql
YEAR(data)
MONTH(data)
GROUP BY período
```

Aplicações:
- faturamento mensal;
- crescimento percentual;
- médias temporais;
- acumulados.

---

# Padrão de JOINs

Estrutura recorrente:

```sql
FROM tabela_a
INNER JOIN tabela_b
    ON relacionamento
```

Objetivos:
- relacionar entidades;
- consolidar informações;
- permitir análises entre tabelas.

---

# Padrão de Subqueries

Aplicações frequentes:

- comparação com médias;
- filtros analíticos;
- validações condicionais.

Exemplo conceitual:

```sql
WHERE valor > (
    SELECT AVG(valor)
)
```

---

# Padrão de CTEs

Estrutura utilizada:

```sql
WITH etapa_1 AS (),
etapa_2 AS ()
SELECT ...
```

Objetivos:
- modularização;
- organização;
- reutilização lógica;
- construção de pipelines analíticos.

---

# Padrão de Ranking

Estruturas utilizadas:

```sql
RANK() OVER()
DENSE_RANK() OVER()
ROW_NUMBER() OVER()
```

Aplicações:
- ranking de clientes;
- ranking de faturamento;
- classificação analítica.

---

# Padrão de Segmentação

Estruturas utilizadas:

```sql
NTILE()
CASE
```

Aplicações:
- classificação de clientes;
- segmentação VIP;
- agrupamentos analíticos.

---

# Padrão de Crescimento Temporal

Estruturas utilizadas:

```sql
LAG()
LEAD()
```

Objetivos:
- comparação entre períodos;
- crescimento percentual;
- análise histórica.

---

# Padrão de Acumulados

Estrutura aplicada:

```sql
SUM(valor) OVER()
```

Aplicações:
- acumulado mensal;
- acumulado anual;
- evolução financeira.

---

# Objetivo dos Padrões

Os padrões utilizados buscaram aproximar os exercícios de cenários encontrados em:

- dashboards analíticos;
- pipelines de dados;
- relatórios executivos;
- análises financeiras;
- ambientes de BI.