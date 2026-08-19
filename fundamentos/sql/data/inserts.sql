-- =====================================================
-- ARQUIVO: inserts
-- OBJETIVO: Inserção de dados nas tabelas
-- =====================================================

-- =====================================================
-- TABELA: CLIENTES
-- =====================================================
INSERT INTO clientes (nome, email) VALUES 
('Ricardo Oliveira', 'ricardo.oli@email.com'),
('Mariana Souza', 'mari.souza@email.com'),
('Carlos Alberto', 'carlos.beto@email.com'),
('Ana Beatriz', 'ana.bia@email.com'),
('Lucas Mendes', 'lucas.m@email.com');

INSERT INTO clientes (nome, email) VALUES
('Fernanda Lima', 'fernanda@email.com'),
('João Pedro', 'joao@email.com'),
('Patricia Gomes', 'patricia@email.com');

INSERT INTO clientes (nome, email) VALUES 
('Renata Vasconcellos', 'renata.vasco@email.com'), 
('Bruno Henrique', 'bruno.h@email.com'),           
('Camila Pitanga', 'camila.p@email.com'),          
('Diego Tardelli', 'diego.t@email.com'),           
('Elena Gilbert', 'elena.g@email.com'),             
('Felipe Melo', 'felipe.melo@email.com'),         
('Gabriela Prioli', 'gabriela.p@email.com');     

select * from clientes;

-- =====================================================
-- TABELA: PRODUTOS
-- =====================================================
INSERT INTO produtos (nome, preco) VALUES
('Fone de Ouvido Bluetooth', 189.90),
('Teclado Mecânico RGB', 350.00),
('Monitor Gamer 24"', 1250.00),
('Cadeira Ergonômica', 890.00),
('Smartphone 128GB', 1950.00);

INSERT INTO produtos (nome, preco) VALUES
('Webcam Full HD', 299.90),
('Mouse Vertical', 159.90);

INSERT INTO produtos (nome, preco) VALUES
('Mouse Pad Deskmat XXL', 89.90),
('Microfone Condensador USB', 450.00),
('Braço Articulado para Monitor', 220.00),
('Roteador Wi-Fi 6 Mesh', 599.00),
('SSD NVMe 1TB HighSpeed', 420.00),
('Memória RAM DDR4 16GB', 310.00),
('Placa de Vídeo RTX 4060', 2450.00),
('Fonte Nominal 650W 80 Plus', 389.90),
('Gabinete Mid Tower Vidro', 340.00),
('Water Cooler 240mm RGB', 499.00),
('Hub USB-C 7 em 1', 179.90),
('Suporte Notebook Alumínio', 120.00),
('Fita LED Smart Wi-Fi', 79.90);

select * from produtos;

-- =====================================================
-- TABELA: PEDIDOS
-- =====================================================
INSERT INTO pedidos (id_cliente, data_pedido, status) VALUES 
-- Outubro 2023
(1, '2023-10-01', 'Confirmado'),
(2, '2023-10-02', 'Confirmado'),
(1, '2023-10-03', 'Cancelado'),
(3, '2023-10-05', 'Confirmado'),
(2, '2023-10-07', 'Bloqueado'), 
(4, '2023-10-10', 'Confirmado'),
(5, '2023-10-12', 'Cancelado'),
(1, '2023-10-15', 'Confirmado');

INSERT INTO pedidos (id_cliente, data_pedido, status) VALUES
-- Novembro 2023
(2, '2023-11-03', 'Confirmado'),
(3, '2023-11-08', 'Confirmado'),
(5, '2023-11-15', 'Cancelado'),
(1, '2023-11-20', 'Confirmado'),
-- Dezembro 2023
(4, '2023-12-02', 'Confirmado'),
(2, '2023-12-10', 'Bloqueado'),
(3, '2023-12-18', 'Confirmado'),
(5, '2023-12-22', 'Confirmado'),
-- Janeiro 2024
(1, '2024-01-05', 'Confirmado'),
(4, '2024-01-11', 'Cancelado'),
(2, '2024-01-19', 'Confirmado'),
(3, '2024-01-25', 'Confirmado');

INSERT INTO pedidos (id_cliente, data_pedido, status) VALUES 
-- Fevereiro e Março 2024
(6, '2024-02-02', 'Confirmado'),  
(7, '2024-02-10', 'Confirmado'),  
(1, '2024-02-15', 'Confirmado'),  
(9, '2024-02-22', 'Cancelado'),  
(10, '2024-03-01', 'Confirmado'), 
(2, '2024-03-12', 'Confirmado'),  
(11, '2024-03-15', 'Bloqueado'),  
(12, '2024-03-28', 'Confirmado'),

-- Abril, Maio e Junho 
(3, '2024-04-05', 'Confirmado'),  
(13, '2024-04-18', 'Confirmado'), 
(14, '2024-04-20', 'Cancelado'),  
(9, '2024-05-02', 'Confirmado'),   
(6, '2024-05-15', 'Confirmado'),  
(15, '2024-05-25', 'Confirmado'), 
(1, '2024-06-03', 'Confirmado'),  
(4, '2024-06-12', 'Confirmado'),  
(12, '2024-06-22', 'Cancelado'),  

-- Julho, Agosto e Setembro 
(7, '2024-07-01', 'Confirmado'),  
(9, '2024-07-14', 'Confirmado'), 
(2, '2024-08-05', 'Confirmado'),  
(10, '2024-08-19', 'Confirmado'), 
(13, '2024-08-25', 'Bloqueado'), 
(15, '2024-09-02', 'Confirmado'), 
(5, '2024-09-18', 'Confirmado'), 
(11, '2024-09-30', 'Confirmado'), 

-- Outubro, Novembro e Dezembro 2024
(1, '2024-10-05', 'Confirmado'),  
(6, '2024-10-20', 'Confirmado'),  
(9, '2024-11-01', 'Confirmado'),  
(14, '2024-11-10', 'Cancelado'),  
(2, '2024-11-25', 'Confirmado'),  
(10, '2024-11-26', 'Confirmado'), 
(15, '2024-11-27', 'Confirmado'), 
(3, '2024-11-28', 'Confirmado'), 
(7, '2024-12-05', 'Confirmado'),  
(9, '2024-12-12', 'Confirmado'),  
(12, '2024-12-15', 'Confirmado'), 
(13, '2024-12-18', 'Confirmado'), 
(1, '2024-12-20', 'Confirmado'), 
(4, '2024-12-22', 'Cancelado'),   
(11, '2024-12-23', 'Confirmado'); 

select * from pedidos;

-- =====================================================
-- TABELA: ITENS_PEDIDO
-- =====================================================
INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES 
(1, 1, 2, 189.90), 
(1, 2, 1, 350.00), 
(1, 3, 1, 1250.00),
(2, 3, 1, 1250.00),
(2, 2, 3, 350.00),
(3, 1, 1, 189.90),
(4, 4, 1, 890.00), 
(4, 5, 2, 1950.00),
(5, 2, 2, 350.00),
(5, 5, 2, 1950.00),
(6, 3, 1, 1250.00), 
(6, 1, 3, 189.90),
(7, 4, 1, 890.00),
(8, 5, 1, 1950.00), 
(8, 1, 4, 189.90);

INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
(9, 1, 1, 189.90),
(9, 5, 1, 1950.00),
(10, 3, 2, 1250.00),
(11, 2, 1, 350.00),
(12, 4, 1, 890.00),
(12, 1, 2, 189.90),
(13, 5, 1, 1950.00),
(14, 2, 2, 350.00),
(15, 3, 1, 1250.00),
(15, 4, 1, 890.00),
(16, 1, 5, 189.90),
(17, 5, 2, 1950.00),
(18, 4, 1, 890.00),
(19, 2, 3, 350.00),
(19, 3, 1, 1250.00),
(20, 1, 2, 189.90),
(20, 5, 1, 1950.00);

INSERT INTO itens_pedido (id_pedido, id_produto, quantidade, preco_unitario) VALUES
-- Pedidos de Fevereiro / Março 
(21, 6, 1, 299.90), 
(21, 8, 1, 89.90),
(22, 12, 2, 420.00), 
(22, 13, 4, 310.00),
(23, 14, 1, 2450.00),
(24, 7, 2, 159.90),
(25, 5, 1, 1950.00), 
(25, 9, 1, 450.00),
(26, 10, 1, 220.00), 
(26, 1, 1, 189.90),
(27, 4, 1, 890.00),
(28, 11, 1, 599.00), 
(28, 18, 1, 120.00),

-- Pedidos de Média Temporada (Abril a Junho)
(29, 2, 1, 350.00), 
(29, 19, 2, 79.90),
(30, 15, 1, 389.90), 
(30, 16, 1, 340.00),
(31, 3, 1, 1250.00),
(32, 14, 1, 2450.00), 
(32, 12, 2, 420.00), 
(32, 13, 2, 310.00),
(33, 17, 1, 499.00),
(34, 1, 1, 189.90), 
(34, 7, 1, 159.90),
(35, 4, 2, 890.00),
(36, 5, 1, 1950.00),
(37, 6, 1, 299.90),

-- Pedidos do Meio do Ano
(38, 14, 1, 2450.00), 
(38, 15, 1, 389.90),
(39, 2, 2, 350.00), 
(39, 8, 3, 89.90),
(40, 3, 1, 1250.00),
(41, 14, 2, 2450.00),
(42, 5, 1, 1950.00),
(43, 12, 2, 420.00),
(44, 13, 2, 310.00), 
(44, 1, 1, 189.90),
(45, 9, 1, 450.00), 
(45, 10, 1, 220.00),

-- Pedidos de Alta Sazonalidade 
(46, 6, 2, 299.90), 
(46, 18, 2, 120.00),
(47, 3, 1, 1250.00), 
(47, 2, 1, 350.00),
(48, 14, 1, 2450.00), 
(48, 12, 4, 420.00),
(49, 5, 2, 1950.00),
(50, 4, 1, 890.00), 
(50, 14, 1, 2450.00), 
(50, 1, 2, 189.90),
(51, 3, 2, 1250.00), 
(51, 17, 1, 499.00),
(52, 5, 1, 1950.00), 
(52, 6, 1, 299.90),
(53, 11, 2, 599.00), 
(53, 12, 2, 420.00),
(54, 14, 1, 2450.00), 
(54, 13, 2, 310.00),
(55, 15, 1, 389.90), 
(55, 16, 1, 340.00), 
(55, 17, 1, 499.00),
(56, 1, 1, 189.90), 
(56, 2, 1, 350.00), 
(56, 8, 1, 89.90),
(57, 4, 1, 890.00),
(58, 5, 1, 1950.00), 
(58, 14, 1, 2450.00), 
(59, 3, 1, 1250.00),
(60, 9, 2, 450.00), 
(60, 10, 2, 220.00), 
(60, 19, 3, 79.90);
select * from itens_pedido;