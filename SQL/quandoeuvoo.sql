CREATE DATABASE IF NOT EXISTS quando_eu_voo DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE quando_eu_voo;

-- DROP TABLE IF EXISTS voo;
CREATE TABLE voo (
  idVoo int NOT NULL AUTO_INCREMENT,
  origem VARCHAR(30) NOT NULL,
  destino VARCHAR(30) NOT NULL,
  PRIMARY KEY (idVoo)
);

-- DROP TABLE IF EXISTS passagem;
CREATE TABLE passagem (
  idPassagem int NOT NULL AUTO_INCREMENT,
  idVoo int NOT NULL,
  companhia varchar(10) NOT NULL,
  media decimal(9,2) NOT NULL,
  dataVoo datetime NOT NULL,
  dataPesquisa datetime NOT NULL,
  PRIMARY KEY (idPassagem),
  KEY passagem_idvoo_FK_IX (idVoo),
  CONSTRAINT passagem_idvoo_FK FOREIGN KEY (idVoo) REFERENCES voo (idVoo) ON DELETE CASCADE ON UPDATE RESTRICT
);


-- DROP TABLE IF EXISTS tp_passagem;
CREATE TABLE tp_passagem (
  idTpPassagem int NOT NULL AUTO_INCREMENT,
  idPassagem int NOT NULL,
  hSaida char(5) NOT NULL,
  hChegada char(5) NOT NULL,
  duracao char(5) NOT NULL,
  diasPraFrente tinyint NOT NUll,
  preco decimal(9,2) NOT NULL,
  PRIMARY KEY (idTpPassagem),
  KEY passagem_idtppassagem_FK_IX (idPassagem),
  CONSTRAINT passagem_idtppassagem_FK FOREIGN KEY (idPassagem) REFERENCES passagem (idPassagem) ON DELETE CASCADE ON UPDATE RESTRICT
);

