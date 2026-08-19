-- ========================================================================
-- Business KPIs
-- ========================================================================

-- ========================================================================
-- KPI - Faturamento Total
-- ========================================================================
SELECT
	ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento_total
FROM itens_pedido as ip
	INNER JOIN pedidos as ped
		ON ip.id_pedido = ped.id_pedido
WHERE ped.status = 'Confirmado';

-- ========================================================================
-- KPI - Ticket medio
-- ========================================================================
SELECT
	ROUND(
		SUM(ip.quantidade * ip.preco_unitario) 
        / NULLIF(COUNT(DISTINCT ip.id_pedido), 0) , 
	2) as ticket_medio
FROM itens_pedido as ip
	INNER JOIN pedidos as ped
		ON ip.id_pedido = ped.id_pedido
WHERE ped.status = 'Confirmado';

-- ========================================================================
-- KPI - Total clientes
-- ========================================================================
SELECT
	COUNT(c.id_cliente) as total_clientes
FROM clientes as c;

-- ========================================================================
-- KPI - Total pedidos
-- ========================================================================
SELECT
	COUNT(ped.id_pedido) as total_pedidos
FROM pedidos as ped
WHERE ped.status = 'Confirmado';

-- ========================================================================
-- KPI - Produtos mais vendidos
-- ========================================================================
WITH faturamento_produtos as (
	SELECT
		prod.nome as produto,
		SUM(ip.quantidade) AS quantidade_vendida
	FROM produtos as prod
		INNER JOIN itens_pedido as ip
			ON prod.id_produto = ip.id_produto
	GROUP BY prod.nome
),
tendencias as (
	SELECT
		produto, quantidade_vendida,
		DENSE_RANK()
			OVER(order by quantidade_vendida DESC)
		as ranking
	FROM faturamento_produtos
)
SELECT
	ranking, produto, quantidade_vendida
FROM tendencias
WHERE ranking <= 5;

-- ========================================================================
-- KPI - Faturamento Mensal
-- ========================================================================
SELECT
	YEAR(ped.data_pedido) as ano,
    MONTH(ped.data_pedido) as mes,
	ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido);

-- ========================================================================
-- KPI - Taxa de cancelamentos
-- ========================================================================
SELECT
    COUNT(id_pedido) as total_pedidos,
    COUNT(CASE WHEN status = 'Cancelado' THEN 1 END) as pedidos_cancelados,
    ROUND(
        (COUNT(CASE WHEN status = 'Cancelado' THEN 1 END) * 100.0) / COUNT(id_pedido), 
        2
    ) as taxa_cancelamento_percentual
FROM pedidos;

-- ========================================================================
-- KPI - Clientes recorrentes
-- ========================================================================
SELECT
    c.nome as cliente,
    COUNT(ped.id_pedido) as qtd_pedido
FROM clientes as c
	INNER JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
WHERE ped.status = 'Confirmado'
GROUP BY c.nome
HAVING qtd_pedido >= 3
ORDER BY qtd_pedido DESC;

-- ========================================================================
-- KPI - Média pedidos dos clientes
-- ========================================================================
SELECT
    ROUND(COUNT(ped.id_pedido) / COUNT(DISTINCT c.id_cliente), 1) as media_pedidos_cliente
FROM clientes as c
	INNER JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
WHERE ped.status = 'Confirmado';

-- ========================================================================
-- KPI - Ranking de faturamento dos produtos
-- ========================================================================
WITH faturamento_produtos as (
	SELECT
		prod.nome as produto,
		ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento
	FROM produtos as prod
		INNER JOIN itens_pedido as ip
			ON prod.id_produto = ip.id_produto
	GROUP BY prod.nome
),
tendencias as (
	SELECT
		produto, faturamento,
		DENSE_RANK()
			OVER(order by faturamento DESC)
		as ranking
	FROM faturamento_produtos
)
SELECT
	ranking, produto, faturamento
FROM tendencias;