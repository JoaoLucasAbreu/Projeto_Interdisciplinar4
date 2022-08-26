create database if not exists inter4;

create table voo (
idVoo int NOT NULL,
duracao int NOT NULL,
dataVoo datetime not null,
primary key(idVoo)
);

create table passagem(
idPassagem int not null,
companhia varchar(20) not null,
dataVisualizacao date not null,
precoPesquisa number(5,2) not null,
precoDesc number(5,2) null,
tpVoo varchar(15) not null,
idVoo_FK int not null,
primary key(idPassagem),
FOREIGN KEY (idVoo_FK) REFERENCES voo(idVoo)
);