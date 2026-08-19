-- =================================================================
-- ANALYTICAL CHALLENGES
-- =================================================================

-- ========================================================================
-- Clientes vip
-- ========================================================================
WITH faturamento_clientes as (
	SELECT
		c.id_cliente as id,
		c.nome as cliente,
		ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento
	FROM clientes as c
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
),
classificacao_clientes as (
	SELECT
		id, cliente, faturamento,
        NTILE(4)
			OVER(order by faturamento)
		as classificacao_cliente
    FROM faturamento_clientes
)
SELECT
	id, cliente, faturamento,
    CASE
		WHEN classificacao_cliente = 4 then 'VIP'
        WHEN classificacao_cliente IN (2, 3) then 'ALTO'
        ELSE 'BAIXO'
	END as ranking
FROM classificacao_clientes
WHERE classificacao_cliente = 4
ORDER BY faturamento DESC;

-- ========================================================================
-- Produtos mais rentaveis
-- ========================================================================
WITH faturamento_produtos as (
	SELECT
		prod.id_produto as id,
		prod.nome as produto,
		ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento
	FROM produtos as prod
			INNER JOIN itens_pedido as ip
				ON prod.id_produto = ip.id_produto
			INNER JOIN pedidos as ped
				ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY prod.id_produto, prod.nome
)
SELECT
	id, produto, faturamento,
    DENSE_RANK() 
		OVER(order by faturamento DESC) 
	as ranking
FROM faturamento_produtos;

-- ========================================================================
-- Analise de cancelamentos
-- ========================================================================
WITH total_cancelamentos_cliente as (
	SELECT
		c.id_cliente as id,
		c.nome as cliente,
		COUNT(ped.id_pedido) as qtd_ped_cancelados
	FROM pedidos as ped
		INNER JOIN clientes as c
			ON c.id_cliente = ped.id_cliente
	WHERE ped.status = 'Cancelado'
	GROUP BY c.id_cliente, c.nome
)
SELECT
	id, cliente, qtd_ped_cancelados,
	SUM(qtd_ped_cancelados) 
		OVER() 
	as total_pedidos_cancelados,
	ROUND((qtd_ped_cancelados * 100.0) / SUM(qtd_ped_cancelados) 
		OVER(), 2) 
	as percentual_do_total
FROM total_cancelamentos_cliente
ORDER BY qtd_ped_cancelados DESC;

-- ========================================================================
-- Crescimento mensal
-- ========================================================================
WITH faturamento_mensal as (
	SELECT
		YEAR(ped.data_pedido) as ano,
		MONTH(ped.data_pedido) as mes,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
	FROM pedidos as ped
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
),
analise_faturamento as (
	SELECT
		ano, mes, faturamento,
        LAG(faturamento) 
			OVER(order by ano, mes)
		as faturamento_anterior
    FROM faturamento_mensal
)
SELECT
	ano, mes, faturamento,
    COALESCE (
		ROUND(
			((faturamento - faturamento_anterior) * 100.0) /
			NULLIF(faturamento_anterior, 0),
		2)
	, 0) as crescimento_mensal
FROM analise_faturamento;

-- ========================================================================
-- Segmentação dos clientes
-- ========================================================================
WITH faturamento_clientes as (
	SELECT
		c.id_cliente as id,
		c.nome as cliente,
		ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento
	FROM clientes as c
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
)
SELECT
	id, cliente, faturamento,
    CASE
		WHEN faturamento >= 10000 then 'VIP'
        WHEN faturamento >= 5000 then 'OURO'
        WHEN faturamento BETWEEN 2000 AND 4900 THEN 'PRATA'
        ELSE 'BRONZE'
	END as ranking
FROM faturamento_clientes
ORDER BY faturamento DESC;

-- ========================================================================
-- Ticket médio dos clientes
-- ========================================================================
WITH ticket_medio_clientes AS (
    SELECT
        c.id_cliente,
        c.nome,
        ROUND(
            SUM(ip.quantidade * ip.preco_unitario) /
            COUNT(DISTINCT ped.id_pedido),
        2) AS ticket_medio
    FROM clientes c
		INNER JOIN pedidos ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido ip
			ON ped.id_pedido = ip.id_pedido
    WHERE ped.status = 'Confirmado'
    GROUP BY c.id_cliente, c.nome
)
SELECT *
FROM ticket_medio_clientes
ORDER BY ticket_medio DESC;

-- ========================================================================
-- Top produtos por mês
-- ========================================================================
WITH faturamento_produtos_mes as (
	SELECT
		YEAR(ped.data_pedido) as ano,
		MONTH(ped.data_pedido) as mes,
        prod.nome as produto,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
	FROM pedidos as ped
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
		INNER JOIN produtos as prod
			ON prod.id_produto = ip.id_produto
	WHERE ped.status = 'Confirmado'
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido), prod.nome
),
ranking_produtos as (
	SELECT
		ano, mes, produto, faturamento,
		DENSE_RANK()
			OVER(
				partition by ano, mes
				order by faturamento DESC
			) 
		as ranking_vendas_produtos
	FROM faturamento_produtos_mes
)
SELECT
	ano, 
	mes, 
	ranking_vendas_produtos as posicao,
	produto, 
	faturamento
FROM ranking_produtos
WHERE ranking_vendas_produtos <= 3 
ORDER BY ano DESC, mes DESC, posicao ASC;

-- ========================================================================
-- Análise de Retenção Geral (Fidelidade do Cliente)
-- ========================================================================
WITH historico_compras_cliente AS (
	SELECT
		id_cliente,
		COUNT(id_pedido) AS total_compras
	FROM pedidos
	WHERE status = 'Confirmado'
	GROUP BY id_cliente
),
faixas_retencao AS (
	SELECT
		id_cliente,
		total_compras,
		CASE 
			WHEN total_compras = 1 THEN '1. Comprou apenas 1 vez (Sem Retenção)'
			WHEN total_compras = 2 THEN '2. Comprou 2 vezes (Início de Retenção)'
			WHEN total_compras BETWEEN 3 AND 5 THEN '3. Recorrente (3 a 5 compras)'
			ELSE '4. Altamente Fiel (Mais de 5 compras)'
		END AS status_retencao
	FROM historico_compras_cliente
)
SELECT
	status_retencao,
	COUNT(id_cliente) AS qtd_clientes,
	ROUND(
		(COUNT(id_cliente) * 100.0) / SUM(COUNT(id_cliente)) OVER(), 
		2
	) AS percentual_da_base
FROM faixas_retencao
GROUP BY status_retencao
ORDER BY status_retencao ASC;

-- ========================================================================
-- Faturamento acumulado
-- ========================================================================
WITH faturamento_mensal as (
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
	ano, mes, faturamento,
    SUM(faturamento)
		OVER(
			partition by ano
			order by ano, mes
		)
	as faturamento_acumulado
FROM faturamento_mensal;

-- ========================================================================
-- Ranking clientes
-- ========================================================================
WITH faturamento_clientes as (
	SELECT
		c.id_cliente as id,
		c.nome as cliente,
		ROUND(SUM(ip.quantidade * ip.preco_unitario), 2) as faturamento
	FROM clientes as c
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.id_cliente, c.nome
)
SELECT
	id, cliente, faturamento,
    DENSE_RANK()
		OVER(order by faturamento DESC)
	as ranking
FROM faturamento_clientes;
