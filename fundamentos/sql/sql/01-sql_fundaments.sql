-- =====================================================
-- FUNDAMENTOS SQL
-- =====================================================

-- =====================================================
-- Ex1 - Clientes com e-mails em ordem alfabética
-- =====================================================
SELECT
	c.nome, 
    c.email
FROM clientes as c
ORDER BY c.email;

-- =====================================================
-- Ex2 - Produtos acima de 500 reais
-- =====================================================
SELECT
    prod.nome,
    prod.preco
FROM produtos as prod
WHERE prod.preco > 300
ORDER BY preco DESC;

-- =====================================================
-- Ex3 - Pedidos confirmados por data atual
-- =====================================================
SELECT
	ped.id_pedido,
    ped.data_pedido
FROM pedidos as ped
WHERE ped.status = 'Confirmado'
ORDER BY ped.data_pedido DESC;

-- =====================================================
-- Ex4 - Clientes que não possuem e-mail cadastrados
-- =====================================================
SELECT
	c.id_cliente,
	c.nome
FROM clientes as c
WHERE c.email is null;

-- =====================================================
-- Ex5 - Produtos cujo nome termina com GB
-- =====================================================
SELECT
	prod.id_produto,
    prod.nome
FROM produtos as prod
WHERE prod.nome like '%GB';

-- =====================================================
-- Ex6 - Pedidos realizados em 2024
-- =====================================================
SELECT
	ped.id_pedido,
    ped.data_pedido
FROM pedidos as ped
WHERE year(data_pedido) = '2024'
ORDER BY ped.data_pedido DESC;

-- =====================================================
-- Ex7 - Produtos entre 100 e 1000 reais
-- =====================================================
SELECT
    prod.nome,
    prod.preco
FROM produtos as prod
WHERE prod.preco between 100 and 1000
ORDER BY preco DESC;

-- =====================================================
-- Ex8 - Pedidos cancelados ou pendentes
-- =====================================================
SELECT
	ped.id_pedido,
    ped.data_pedido,
    ped.status
FROM pedidos as ped
WHERE ped.status = 'Cancelado' or ped.status = 'Bloqueado'
ORDER BY ped.data_pedido DESC;

-- =====================================================
-- Ex9 - Emails únicos dos clientes
-- =====================================================
SELECT distinct
	c.nome, 
    c.email
FROM clientes as c
WHERE c.email is not null
ORDER BY c.email;

-- =====================================================
-- Ex10 - 5 produtos mais caros.
-- =====================================================
SELECT
    prod.nome,
    prod.preco
FROM produtos as prod
ORDER BY preco DESC
LIMIT 5;

