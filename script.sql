create database if not exists inter4;

use inter4;

create table if not exists voo (
    idVoo INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    origem TEXT NOT NULL,
    destino TEXT NOT NULL
)

create table if not exists passagem(
    idPassagem INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    idVoo INTEGER NOT NULL,
    companhia TEXT NOT NULL,
    media DOUBLE(5,2) NOT NULL,
    dataVoo DATE not null,
    dataPesquisa DATE not null,
    FOREIGN KEY(idVoo) REFERENCES voo(idVoo)
)

create table if not exists tp_passagem(
    idTpPassagem INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    idPassagem INTEGER NOT NULL,
    hSaida TEXT NOT NULL,
    hChegada TEXT NOT NULL,
    duracao TEXT NOT NULL,
    preco DOUBLE(5,2) NOT NULL,
    FOREIGN KEY(idPassagem) REFERENCES passagem (idPassagem)
)





