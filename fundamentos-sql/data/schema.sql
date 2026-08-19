CREATE DATABASE e_commerce
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_general_ci;

USE e_commerce;

CREATE TABLE clientes(
	id_cliente int auto_increment primary key,
    nome varchar(50) not null,
    email varchar(200) unique not null
);

CREATE TABLE produtos(
	id_produto int auto_increment primary key,
    nome varchar(100) not null,
    preco decimal(10,2) not null check (preco >= 0)
);

CREATE TABLE pedidos(
	id_pedido int auto_increment primary key,
    id_cliente int not null unique,
    data_pedido date not null,
    status enum('Confirmado', 'Cancelado', 'Bloqueado') not null,
    foreign key (id_cliente) references clientes(id_cliente) ON DELETE RESTRICT
);

CREATE TABLE itens_pedido(
    id_item int auto_increment primary key,
    id_pedido int not null,
    id_produto int not null,
	UNIQUE (id_pedido, id_produto), 
    quantidade int not null check (quantidade > 0),
    preco_unitario decimal(10,2) not null check (preco_unitario >= 0),
    foreign key (id_pedido) references pedidos(id_pedido) ON DELETE RESTRICT,
    foreign key (id_produto) references produtos(id_produto) ON DELETE RESTRICT
);


