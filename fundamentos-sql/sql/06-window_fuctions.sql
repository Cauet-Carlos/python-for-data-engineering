-- =================================================================
-- WINDOW FUNCTIONS
-- =================================================================

-- ========================================================================
-- Ex1 - Média global de valor dos pedidos usando OVER()
-- ========================================================================
WITH faturamento_pedidos as (
	SELECT
		ped.id_pedido as id,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
	FROM pedidos as ped	
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY ped.id_pedido
)
SELECT
	id,
    faturamento,
    ROUND(AVG(faturamento) 
		over(), 2) 
	as média_global
FROM faturamento_pedidos;

-- ========================================================================
-- Ex2 - Média de faturamento por cliente usando PARTITION BY
-- ========================================================================
WITH valor_pedidos AS (
    SELECT
        ped.id_pedido,
        c.nome AS cliente,
        SUM(ip.quantidade * ip.preco_unitario) AS valor_pedido
    FROM pedidos ped
    INNER JOIN clientes c
        ON ped.id_cliente = c.id_cliente
    INNER JOIN itens_pedido ip
        ON ped.id_pedido = ip.id_pedido
    WHERE ped.status = 'Confirmado'
    GROUP BY ped.id_pedido, c.nome
)
SELECT
    cliente,
    id_pedido,
    valor_pedido,
    ROUND(AVG(valor_pedido)
			OVER(PARTITION BY cliente),
			2
    ) as media_cliente
FROM valor_pedidos
ORDER BY cliente;

-- ========================================================================
-- Ex3 - Ranking de clientes por faturamento usando RANK()
-- ========================================================================
WITH faturmento_clientes as (
	SELECT
        c.nome as cliente,
        ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento
    FROM clientes as c	
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.nome
)
SELECT
    fc.cliente,
    fc.faturamento,
    RANK() 
		OVER( 
			order by faturamento DESC
        ) 
	as ranking
FROM faturmento_clientes as fc;

-- ========================================================================
-- Ex4 - ROW_NUMBER dos pedidos por cliente
-- ========================================================================
WITH pedidos_cliente AS (
    SELECT
        c.nome as cliente,
        COUNT(DISTINCT ped.id_pedido) as pedidos
    FROM pedidos ped
    INNER JOIN clientes c
        ON ped.id_cliente = c.id_cliente
    WHERE ped.status = 'Confirmado'
    GROUP BY c.nome
)
SELECT
    cliente,
    pedidos,
    ROW_NUMBER() 
		OVER(
			order by pedidos DESC
		) 
	as ranking
FROM pedidos_cliente;

-- ========================================================================
-- Ex5 - Faturamento do mês anterior usando LAG()
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
	ano,
    mes,
    faturamento,
    COALESCE(
		LAG(faturamento)
			OVER(
				order by ano, mes
			) 
	, 0) as fat_mes_anterior
FROM faturamentos_mensais as fm;

-- ========================================================================
-- Ex6 - Faturamento do próximo mês usando LEAD()
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
	ano,
    mes,
    faturamento,
    COALESCE(
		LEAD(faturamento)
			OVER(
				order by ano, mes
			) 
	, 0) as fat_prox_mes
FROM faturamentos_mensais as fm;

-- ========================================================================
-- Ex7 - Acumulado de faturamento anual usando SUM OVER
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
	ano,
    mes,
    faturamento,
    SUM(faturamento)
		OVER(
			partition by ano
            order by ano, mes
        )
	as acumulado
FROM faturamentos_mensais as fm;

-- ========================================================================
-- Ex8 - Média móvel de 3 meses
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
	ano,
    mes,
    faturamento,
    ROUND(AVG(faturamento)
		OVER(
			partition by ano
			order by ano, mes
            rows between 2 preceding and current row
        ), 2)
	as media_movel_3
FROM faturamentos_mensais as fm;

-- ========================================================================
-- Ex9 - FIRST_VALUE para mostrar o primeiro faturamento mensal
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
	ano,
    mes,
    faturamento,
    FIRST_VALUE(faturamento) 
		OVER(
			order by ano, mes
        )
	as primeiro_faturamento
FROM faturamentos_mensais as fm;

-- ========================================================================
-- Ex10 - Segmentar clientes em quartis usando NTILE(4)
-- ========================================================================
WITH faturmento_clientes as (
	SELECT
        c.nome as cliente,
        ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_cliente
    FROM clientes as c	
		INNER JOIN pedidos as ped
			ON c.id_cliente = ped.id_cliente
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY c.nome
)
SELECT
    fc.cliente,
    fc.faturamento_cliente,
    NTILE(4)
		OVER(
			order by faturamento_cliente
        )
	as agrupação
FROM faturmento_clientes as fc;
