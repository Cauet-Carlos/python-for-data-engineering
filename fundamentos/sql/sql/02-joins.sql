-- =====================================================
-- UTILIZAÇÃO DO JOIN
-- =====================================================

-- =====================================================
-- Ex1 - Status do pedido do cliente
-- =====================================================
SELECT
	c.nome,
    ped.id_pedido,
    ped.status
FROM clientes as c
	INNER JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente;

-- =====================================================
-- Ex2 - Quantidade vendida por produto
-- =====================================================
SELECT
	prod.nome,
	SUM(ip.quantidade) as total_vendido
FROM produtos as prod
	INNER JOIN itens_pedido as ip
		ON prod.id_produto = ip.id_produto
	INNER JOIN pedidos as ped
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY prod.nome;

-- =====================================================
-- Ex3 - Pedidos dos clientes com suas datas
-- =====================================================
SELECT
	ped.id_pedido,
    c.nome,
    ped.data_pedido
FROM clientes as c
	INNER JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
WHERE ped.status = 'Confirmado';

-- =====================================================
-- Ex4 - Produtos que nunca foram vendidos
-- =====================================================
SELECT
	prod.nome
FROM produtos as prod
	LEFT JOIN itens_pedido as ip
		ON prod.id_produto = ip.id_produto
WHERE ip.id_produto IS NULL;

-- =====================================================
-- Ex5 - clientes que nunca realizaram pedidos
-- =====================================================
SELECT
	c.nome
FROM clientes as c
	LEFT JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
WHERE ped.id_pedido is null;

-- =====================================================
-- Ex6 - Faturamento por pedido
-- =====================================================
SELECT
	ped.id_pedido,
    SUM(ip.preco_unitario * ip.quantidade) as faturamento
FROM pedidos as ped
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Confirmado'
GROUP BY ped.id_pedido;

-- =====================================================
-- Ex7 - Produtos vendidos em pedidos cancelados
-- =====================================================
SELECT
	prod.nome,
    SUM(ip.preco_unitario * ip.quantidade) as faturamento,
    ped.status
FROM produtos as prod
	INNER JOIN itens_pedido as ip
		ON prod.id_produto = ip.id_produto
	INNER JOIN pedidos as ped
		ON ped.id_pedido = ip.id_pedido
WHERE ped.status = 'Cancelado'
GROUP BY prod.nome, ped.status
ORDER BY faturamento DESC;

-- =====================================================
-- Ex8 - Quantidade de pedidos por cliente
-- =====================================================
SELECT
	c.id_cliente,
	c.nome,
    COUNT(ped.id_pedido) as quantidade_pedidos
FROM clientes as c
	LEFT JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
GROUP BY c.id_cliente, c.nome
ORDER BY quantidade_pedidos DESC;

-- =====================================================
-- Ex9 - Clientes e quantidade de produtos comprados
-- =====================================================
SELECT
	c.id_cliente,
    c.nome,
    prod.nome,
    SUM(ip.quantidade) as quantidade,
    SUM(ip.preco_unitario * ip.quantidade) as faturamento
FROM clientes as c
	INNER JOIN pedidos as ped
		ON c.id_cliente = ped.id_cliente
	INNER JOIN itens_pedido as ip
		ON ped.id_pedido = ip.id_pedido
	INNER JOIN produtos as prod
		ON ip.id_produto = prod.id_produto
WHERE ped.status = 'Confirmado'
GROUP BY c.id_cliente, c.nome, prod.nome
ORDER BY c.id_cliente, c.nome, quantidade DESC;

-- =====================================================
-- Ex10 - Pedidos com mais de 2 produtos diferentes
-- =====================================================
SELECT
	ped.id_pedido,
	COUNT(DISTINCT ip.id_produto) as total_produtos_diferentes
FROM pedidos as ped
INNER JOIN itens_pedido as ip
	ON ped.id_pedido = ip.id_pedido
GROUP BY ped.id_pedido
HAVING COUNT(DISTINCT ip.id_produto) > 2
ORDER BY total_produtos_diferentes DESC;