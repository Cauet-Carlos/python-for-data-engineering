-- =================================================================
-- CTES
-- =================================================================

-- ========================================================================
-- Ex1 - Clientes com faturamento acima da média de clientes
-- ========================================================================
WITH faturmento_clientes as (
	SELECT
		c.id_cliente as id,
        c.nome as cliente,
        ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_cliente
    FROM clientes as c	
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
)
SELECT
	fc.id,
    fc.cliente,
    fc.faturamento_cliente
FROM faturmento_clientes as fc
WHERE fc.faturamento_cliente > (
	SELECT
		AVG(faturamento_cliente)
    FROM faturmento_clientes
)
ORDER BY fc.faturamento_cliente DESC;

-- ========================================================================
-- Ex2 - Vendas mensais acima da média de vendas 
-- ========================================================================
WITH faturamentos_mensais as (
	SELECT
		YEAR(ped.data_pedido) as ano,
        MONTH(ped.data_pedido) as mes,
        ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
    FROM pedidos as ped	
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
)
SELECT
	fm.ano,
    fm.mes,
    fm.faturamento
FROM faturamentos_mensais as fm
WHERE fm.faturamento > (
	SELECT
		AVG(faturamento)
    FROM faturamentos_mensais
)
ORDER BY fm.faturamento DESC;

-- ==========================================================================
-- Ex3 - Classificação de produtos acima e abaixo da média por faturamento
-- ==========================================================================
WITH faturamentos_produtos as (
	SELECT
		prod.id_produto,
        prod.nome,
        ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
    FROM produtos as prod	
		INNER JOIN itens_pedido as ip
			ON prod.id_produto = ip.id_produto
		INNER JOIN pedidos as ped
			ON ip.id_pedido = ped.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY prod.id_produto, prod.nome
),
media_produtos as (
	SELECT
		AVG(faturamento) as media
    FROM faturamentos_produtos
)
SELECT
	fp.id_produto,
    fp.nome,
    fp.faturamento,
    CASE
		WHEN fp.faturamento > mp.media THEN 'Acima da média'
        WHEN fp.faturamento < mp.media THEN 'Abaixo da média'
        ELSE 'Na média'
	END as Classificação
FROM faturamentos_produtos as fp
	CROSS JOIN media_produtos as mp
ORDER BY fp.faturamento DESC;

-- ==========================================================================
-- Ex4 - Pipeline analítico de ticket médio por cliente
-- ==========================================================================
WITH tickt_cliente as (
	SELECT
		c.id_cliente,
		c.nome as cliente,
		ROUND(SUM(ip.preco_unitario * ip.quantidade) / COUNT(DISTINCT ped.id_pedido), 2) 
			as ticket_medio_cliente
	FROM clientes as c
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
),
ticket_medio as (
	SELECT 
        ROUND(AVG(ticket_medio_cliente), 2) AS ticket_medio_geral
    FROM tickt_cliente
)
SELECT 
	tc.id_cliente,
    tc.cliente,
    tc.ticket_medio_cliente,
    tcc.ticket_medio_geral
FROM tickt_cliente as tc
	INNER JOIN ticket_medio as tcc;

-- ==========================================================================
-- Ex5 - Clientes mais frenquentes por quantidade de pedidos
-- ==========================================================================
WITH cliente_qtd_pedido as (
	SELECT
		c.id_cliente as id,
		c.nome as cliente,
		COUNT(ped.id_pedido) as qtd_pedido
	FROM clientes as c
		LEFT JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente AND ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
)
SELECT
	cqp.id,
    cqp.cliente,
    cqp.qtd_pedido
FROM cliente_qtd_pedido as cqp
ORDER BY cqp.qtd_pedido DESC
LIMIT 5;

-- ==========================================================================
-- Ex6 - Análise de faturamento mensal com acumulado
-- ==========================================================================
WITH faturamento as (
	SELECT
		YEAR(ped.data_pedido) as ano,
		MONTH(ped.data_pedido) as mes,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal
	FROM pedidos as ped
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
)
SELECT
	fat.ano,
    fat.mes,
    fat.faturamento_mensal,
    ROUND(SUM(faturamento_mensal) 
		over(order by ano, mes), 2) as acumulado
FROM faturamento as fat
ORDER BY ano, mes;

-- ==========================================================================
-- Ex7 - CTE temporal por crescimento percentual
-- ==========================================================================
WITH faturamento as (
	SELECT
		YEAR(ped.data_pedido) as ano,
		MONTH(ped.data_pedido) as mes,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal
	FROM pedidos as ped
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
),
faturamento_com_lag AS (
    SELECT
        ano,
        mes,
        faturamento_mensal,
        LAG(faturamento_mensal) OVER (ORDER BY ano, mes) AS faturamento_mes_anterior
    FROM faturamento
)
SELECT
    ano,
    mes,
    faturamento_mensal,
    COALESCE(
        ROUND(((faturamento_mensal - faturamento_mes_anterior) * 100.0) / 
        NULLIF(faturamento_mes_anterior, 0), 2)
    , 0) AS crescimento_percentual
FROM faturamento_com_lag
ORDER BY ano, mes;
		
-- ==========================================================================
-- Ex8 - Segmentação simples de clientes:
-- VIP / Médio / Baixo
-- ==========================================================================
WITH faturamento_cliente as (
	SELECT
		c.id_cliente as id,
		c.nome as cliente,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
	FROM clientes as c
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
),
clientes_quartil as (
	SELECT
		id, 
        cliente,
        faturamento,
        NTILE(4) over(order by faturamento asc) as grupo_distribuicao
    FROM faturamento_cliente
)
SELECT
	id,
    cliente,
    faturamento,
    CASE
		WHEN grupo_distribuicao = 4 then 'VIP'
        WHEN grupo_distribuicao in (2, 3) then 'MÉDIO'
        ELSE 'BAIXO'
	END as classificação_clientes
FROM clientes_quartil 
ORDER BY faturamento DESC;

-- ==========================================================================
-- Ex9 - Múltiplas CTEs para:
-- faturamento / ticket médio / ranking de clientes
-- ==========================================================================
WITH faturamento_cliente as (
	SELECT 
		c.id_cliente as id,
		c.nome as cliente,
		SUM(ip.preco_unitario * ip.quantidade) as faturamento,
        COUNT(DISTINCT ip.id_pedido) as total_pedidos
	FROM clientes as c 
		INNER JOIN pedidos as ped 
			ON ped.id_cliente = c.id_cliente
		INNER JOIN itens_pedido as ip 
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
),
tickt_medio as (
	SELECT
		id,
		cliente,
        faturamento,
		ROUND(faturamento / NULLIF(total_pedidos, 0), 2) 
			as ticket_medio_cliente
	FROM faturamento_cliente
),
ranking_e_segmentacao as (
	SELECT
		id,
		cliente,
        faturamento,
		ticket_medio_cliente,
        DENSE_RANK() OVER(ORDER BY faturamento DESC) as ranking,
        NTILE(4) OVER(ORDER BY faturamento ASC) as grupo_distribuicao
	FROM tickt_medio
)
SELECT
	id,
	cliente,
	faturamento,
	ticket_medio_cliente,
    ranking,
    CASE 
        WHEN grupo_distribuicao = 4 THEN 'VIP'        -- Top 25% maiores faturamentos
        WHEN grupo_distribuicao IN (2, 3) THEN 'Médio' -- 50% intermediários
        ELSE 'Baixo'                                  -- 25% menores faturamentos
    END as classificação_clientes
FROM ranking_e_segmentacao
ORDER BY ranking ASC;

-- ==========================================================================
-- Ex10 - Múltiplas CTEs para:
-- faturamento / quantidade pedidos / ticket médio / crescimento mensal
-- ==========================================================================
WITH faturamento_mensal as (
	SELECT 
		YEAR(ped.data_pedido) as ano,
		MONTH(ped.data_pedido) as mes,
		SUM(ip.preco_unitario * ip.quantidade) as faturamento,
        COUNT(DISTINCT ip.id_pedido) as total_pedidos
	FROM pedidos as ped 
		INNER JOIN itens_pedido as ip 
			ON ped.id_pedido = ip.id_pedido
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
),
ticket_medio_and_lag as (
	SELECT
		ano,
		mes,
        total_pedidos,
        faturamento,
		ROUND(faturamento / NULLIF(total_pedidos, 0), 2) 
			as ticket_medio_cliente,
		LAG(faturamento) over(order by ano, mes) as fat_mes_ant
	FROM faturamento_mensal
),
status_final as (
	SELECT
		ano,
		mes,
        total_pedidos,
        faturamento,
		ticket_medio_cliente,
        COALESCE(
			ROUND(((faturamento - fat_mes_ant) * 100.0) / 
			NULLIF(fat_mes_ant, 0), 2)
		, 0) AS crescimento_mensal
	FROM ticket_medio_and_lag
)
SELECT
	ano,
	mes,
	total_pedidos,
	faturamento,
	ticket_medio_cliente,
	crescimento_mensal
FROM status_final;