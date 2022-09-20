create database if not exists inter4;

use inter4;

create table voo (
idVoo int NOT NULL,
origem varchar(3) NOT NULL,
destino varchar(3) not null,
primary key(idVoo)
);

create table passagem(
idPassagem int not null,
companhia varchar(20) not null,
dataVisualizacao date not null,
dataVoo datetime not null,
preco double(5,2) null,
tpPreco double(5,2) not null,
tpVoo varchar(15) not null,
hrChegada datetime not null,
hrSaida datetime not null,
duracao time not null,
idVoo_FK int not null,
primary key(idPassagem),
FOREIGN KEY (idVoo_FK) REFERENCES voo(idVoo)
);




