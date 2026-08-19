# Boas Práticas Aplicadas

Durante o desenvolvimento dos exercícios foram aplicadas práticas voltadas para organização, legibilidade e padronização das consultas SQL.

---

# Organização das Queries

As consultas foram separadas por temas e níveis de complexidade:

- fundamentos;
- joins;
- análises temporais;
- subqueries;
- CTEs;
- window functions.

Objetivo:
- facilitar manutenção;
- melhorar leitura;
- permitir progressão técnica organizada.

---

# Padronização

Foi utilizado um padrão consistente de escrita SQL:

- aliases padronizados;
- indentação organizada;
- separação lógica das cláusulas;
- comentários descritivos;
- agrupamento visual das consultas.

Exemplo:

```sql
SELECT
    c.nome,
    ped.id_pedido
FROM clientes as c
INNER JOIN pedidos as ped
    ON c.id_cliente = ped.id_cliente;
```

---

# Utilização de Aliases

Aliases foram utilizados para:

- reduzir repetição;
- melhorar legibilidade;
- simplificar joins;
- facilitar manutenção.

Exemplos:
- c -> clientes
- ped -> pedidos
- ip -> itens_pedido
- prod -> produtos

---

# Legibilidade

As consultas foram estruturadas visando fácil interpretação.

Práticas utilizadas:

- quebra de linhas;
- alinhamento de JOINs;
- separação de blocos;
- organização de cláusulas;
- comentários antes dos exercícios.

---

# Modularização

As consultas mais complexas foram modularizadas utilizando:

- subqueries;
- CTEs;
- múltiplas etapas analíticas.

Objetivos:
- reutilização lógica;
- clareza;
- redução de complexidade.

---

# Tratamento de Dados

Funções utilizadas para tratamento e controle:

- ROUND()
- COALESCE()
- NULLIF()

Objetivos:
- evitar divisões por zero;
- melhorar visualização;
- tratar valores nulos.

---

# Estrutura Analítica

As análises seguiram padrões comuns em ambientes de dados:

- agregações;
- rankings;
- segmentações;
- análises temporais;
- acumulados;
- médias móveis.

---

# Comentários e Documentação

Todos os exercícios foram documentados utilizando comentários descritivos.

Objetivos:
- facilitar revisão;
- melhorar navegação;
- identificar rapidamente o objetivo da query.

---

# Objetivo Técnico

As práticas aplicadas buscaram aproximar os exercícios de padrões utilizados em:

- Business Intelligence;
- Engenharia de Dados;
- Analytics Engineering;
- Análise de Dados.