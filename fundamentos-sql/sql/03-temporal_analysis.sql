-- =================================================================
-- ANÁLISES TEMPORAIS
-- =================================================================

-- ========================================================================
-- Ex1 - faturamento por mês
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex2 - Quantidade de pedidos por mês
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
	COUNT(ped.id_pedido) as quantidade_pedidos
FROM pedidos as ped
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex3 - Ticket médio mensal
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
	ROUND(SUM(ip.preco_unitario * ip.quantidade) / COUNT(DISTINCT ip.id_pedido), 2)
		as tickt_medio_mensal
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex4 - Mês com maior faturamento
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY faturamento_mensal DESC
LIMIT 1;

-- ========================================================================
-- Ex5 - Crescimento percentual entre meses
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal,
    LAG(ROUND(SUM(ip.preco_unitario * ip.quantidade), 2)) 
		OVER(ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido))
			AS fat_mes_anterior,
	COALESCE(
        ROUND(((SUM(ip.preco_unitario * ip.quantidade) - LAG(SUM(ip.preco_unitario * ip.quantidade)) OVER(ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido))) * 100) /
        NULLIF(LAG(SUM(ip.preco_unitario * ip.quantidade)) OVER(ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)), 0), 2), 
    0) AS comp_percentual
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex6 - Faturamento acumulado por mês
-- ========================================================================
SELECT 
    YEAR(ped.data_pedido) AS ano,
    MONTH(ped.data_pedido) AS mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) AS faturamento_mensal,
    ROUND(SUM(SUM(ip.preco_unitario * ip.quantidade)) 
		OVER(ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)), 2) 
			AS faturamento_acumulado
FROM pedidos AS ped
    INNER JOIN itens_pedido AS ip
        ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex7 - Média móvel de faturamento considerando os últimos 3 meses
-- ========================================================================
SELECT 
    YEAR(ped.data_pedido) AS ano,
    MONTH(ped.data_pedido) AS mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) AS faturamento_mensal,
    ROUND(AVG(SUM(ip.preco_unitario * ip.quantidade))
		over(
			ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
            ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
        ), 2) AS media_movel_3_meses
FROM pedidos AS ped
    INNER JOIN itens_pedido AS ip
        ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex8 - Mês com menor quantidade de pedidos
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
	COUNT(ped.id_pedido) as quantidade_pedidos
FROM pedidos as ped
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY quantidade_pedidos
LIMIT 1;

-- ========================================================================
-- Ex9 - Média faturamento mensal
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal,
    ROUND(AVG(SUM(ip.preco_unitario * ip.quantidade)) OVER(), 2) as media_faturamento_geral
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- Ex10 - Ranking dos meses por faturamento
-- ========================================================================
SELECT 
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
    ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal,
    RANK() 
		OVER(
			partition by YEAR(ped.data_pedido)
			order by SUM(ip.preco_unitario * ip.quantidade) desc
        ) as ranking
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
ORDER BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);
