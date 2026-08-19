-- =================================================================
-- SUBQUERYS
-- =================================================================

-- ========================================================================
-- Ex1 - Produtos acima da média de preço
-- ========================================================================
SELECT 
	prod.id_produto,
	prod.nome as produto, 
    ROUND(prod.preco, 2) preco_produto
FROM produtos as prod
WHERE prod.preco > (
	SELECT 
		AVG(prod.preco)
	FROM produtos as prod
)
ORDER BY preco_produto DESC;

-- ========================================================================
-- Ex2 - Clientes com faturamento acima da média dos clientes
-- ========================================================================
SELECT 
	c.id_cliente as id,
	c.nome as cliente,
	SUM(ip.preco_unitario * ip.quantidade) as faturamento_cliente
FROM clientes as c 
	INNER JOIN pedidos as ped 
		ON ped.id_cliente = c.id_cliente
	INNER JOIN itens_pedido as ip 
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY c.id_cliente, c.nome
HAVING SUM(ip.preco_unitario * ip.quantidade) > (
	SELECT 
		AVG(sub.faturamento_total)
	FROM (
		SELECT 
			SUM(ip2.preco_unitario * ip2.quantidade) as faturamento_total
		FROM clientes as c2
			INNER JOIN pedidos as ped2 ON ped2.id_cliente = c2.id_cliente
			INNER JOIN itens_pedido as ip2 ON ped2.id_pedido = ip2.id_pedido
		WHERE ped2.status = 'Confirmado'
		GROUP BY c2.id_cliente
	) as sub
);

-- ========================================================================
-- Ex3 - Pedidos acima do ticket médio
-- ========================================================================
SELECT
	ped.id_pedido as id,
	ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_pedido
FROM pedidos as ped
	INNER JOIN itens_pedido as ip 
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY ped.id_pedido
HAVING ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) > (
	SELECT 
		AVG(sub.faturamento_total)
	FROM (
		SELECT 
			SUM(ip2.preco_unitario * ip2.quantidade) as faturamento_total
		FROM pedidos as ped2
			INNER JOIN itens_pedido as ip2 
				ON ped2.id_pedido = ip2.id_pedido
		WHERE ped2.status = 'Confirmado'
		GROUP BY ped2.id_pedido
	) as sub
);

-- ========================================================================
-- Ex4 - Produtos nunca vendidos usando NOT EXISTS
-- ========================================================================
SELECT
	prod.id_produto as id,
    prod.nome as produto
FROM produtos as prod
WHERE NOT EXISTS (
	SELECT 1
    FROM itens_pedido as ip
    WHERE ip.id_produto = prod.id_produto
);

-- ========================================================================
-- Ex5 - Clientes que possuem ao menos um pedido confirmado usando EXISTS
-- ========================================================================
SELECT
	c.id_cliente as id,
    c.nome as cliente
FROM clientes as c
WHERE EXISTS (
	SELECT 1
    FROM pedidos as ped
    WHERE ped.id_cliente = c.id_cliente and ped.status = 'Confirmado'
)
ORDER BY c.id_cliente;

-- ========================================================================
-- Ex6 - Média mensal de faturamento usando subquery no FROM
-- ========================================================================
SELECT
	ROUND(AVG(med.faturamento_mensal), 2) as media_faturamento
FROM (
	SELECT 
		YEAR(ped.data_pedido) as ano,
		MONTH(ped.data_pedido) as mes,
		ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal
	FROM pedidos as ped
		INNER JOIN itens_pedido as ip
			ON ped.id_pedido = ip.id_pedido
	WHERE ped.status = 'Confirmado'
	GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
) as med;

-- ========================================================================
-- Ex7 - Meses cujo faturamento ficou acima da média mensal
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
HAVING ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) > (
	SELECT
		AVG(faturamento.faturamento_mensal)
    FROM (
		SELECT
			YEAR(ped.data_pedido) as ano,
			MONTH(ped.data_pedido) as mes,
			ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_mensal
		FROM pedidos as ped
			INNER JOIN itens_pedido as ip
				ON ped.id_pedido = ip.id_pedido
		WHERE ped.status = 'Confirmado'
		GROUP BY YEAR(ped.data_pedido), MONTH(ped.data_pedido)
    ) as faturamento
);

-- ========================================================================
-- Ex8 - Clientes com quantidade de pedidos acima da média
-- ========================================================================
SELECT
	c.nome as cliente,
    c.id_cliente,
    COUNT(ped.id_pedido) as qtd_pedidos
FROM clientes as c
	INNER JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
WHERE ped.status = 'Confirmado'
GROUP BY c.id_cliente, c.nome
HAVING COUNT(ped.id_pedido) > (
	SELECT
		AVG(qtd.qtd_pedidos)
    FROM (
		SELECT 
			COUNT(ped2.id_pedido) as qtd_pedidos
		FROM pedidos as ped2
		WHERE ped2.status = 'Confirmado'
		GROUP BY ped2.id_cliente
    ) as qtd
)
ORDER BY qtd_pedidos DESC;

-- ========================================================================
-- Ex9 - Pedidos acima da média do mês correspondente 
-- ========================================================================
SELECT
	ped.id_pedido as id,
	YEAR(ped.data_pedido) as ano,
	MONTH(ped.data_pedido) as mes,
	ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento_pedido,
	medias.media_mensal
FROM pedidos as ped
	INNER JOIN itens_pedido as ip 
		ON ped.id_pedido = ip.id_pedido
	-- Subconsulta simples no FROM para calcular a média de cada mês
	INNER JOIN (
		SELECT 
			YEAR(p.data_pedido) as ano_mes,
			MONTH(p.data_pedido) as mes_mes,
			ROUND(SUM(i.preco_unitario * i.quantidade) / COUNT(DISTINCT p.id_pedido), 2) 
				as media_mensal
		FROM pedidos as p
			INNER JOIN itens_pedido as i 
				ON p.id_pedido = i.id_pedido
		WHERE p.status = 'Confirmado'
		GROUP BY YEAR(p.data_pedido), MONTH(p.data_pedido)
	) as medias 
		ON medias.ano_mes = YEAR(ped.data_pedido) AND medias.mes_mes = MONTH(ped.data_pedido)
WHERE ped.status = 'Confirmado'
GROUP BY ped.id_pedido, YEAR(ped.data_pedido), MONTH(ped.data_pedido), medias.media_mensal
HAVING faturamento_pedido > medias.media_mensal
ORDER BY ano DESC, mes DESC, faturamento_pedido DESC;

-- ==============================================================================
-- Ex10 - Produtos cujo faturamento supera a média de faturamento dos produtos
-- ==============================================================================
SELECT
	prod.id_produto,
	prod.nome,
	ROUND(SUM(ip.preco_unitario * ip.quantidade)) as faturamento
FROM produtos as prod
	INNER JOIN itens_pedido as ip
		ON prod.id_produto = ip.id_produto
GROUP BY prod.id_produto, prod.nome
HAVING ROUND(SUM(ip.preco_unitario * ip.quantidade)) > (
	SELECT 
		AVG(fat.faturamento)
	FROM (
		SELECT
			prod.id_produto,
			prod.nome,
			ROUND(SUM(ip.preco_unitario * ip.quantidade)) as faturamento
		FROM produtos as prod
			INNER JOIN itens_pedido as ip
				ON prod.id_produto = ip.id_produto
		GROUP BY prod.id_produto, prod.nome
	) as fat
)
ORDER BY faturamento DESC;

-- ==============================================================================
-- Ex10.1 - Produtos cujo faturamento supera a média de faturamento dos produtos
-- Versão aprimorada
-- ==============================================================================
SELECT
	prod.id_produto,
	prod.nome,
	ROUND(SUM(ip.preco_unitario * ip.quantidade), 2) as faturamento,
    media_global.media_faturamento_prod 
FROM produtos as prod
	INNER JOIN itens_pedido as ip 
		ON prod.id_produto = ip.id_produto
	INNER JOIN (
		SELECT
			ROUND(AVG(sub.faturamento_total), 2) as media_faturamento_prod
        FROM (
			SELECT 
				SUM(ip2.preco_unitario * ip2.quantidade) as faturamento_total
			FROM itens_pedido as ip2
			GROUP BY ip2.id_produto
        ) as sub
    ) as media_global
GROUP BY prod.id_produto, prod.nome, media_global.media_faturamento_prod
HAVING faturamento > media_global.media_faturamento_prod
ORDER BY faturamento DESC;
 



























