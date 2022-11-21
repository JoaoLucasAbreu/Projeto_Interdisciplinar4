CREATE DATABASE IF NOT EXISTS quando_eu_voo DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;
USE quando_eu_voo;

-- DROP TABLE IF EXISTS perfil;
CREATE TABLE perfil (
  id int NOT NULL AUTO_INCREMENT,
  nome varchar(50) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY nome_UN (nome)
);

-- Manter sincronizado com enums/perfil.ts e models/perfil.ts
INSERT INTO perfil (nome) VALUES ('Administrador'), ('Comum');

-- DROP TABLE IF EXISTS usuario;
CREATE TABLE usuario (
  id int NOT NULL AUTO_INCREMENT,
  email varchar(100) NOT NULL,
  nome varchar(100) NOT NULL,
  idperfil int NOT NULL,
  senha varchar(100) NOT NULL,
  token char(32) DEFAULT NULL,
  exclusao datetime NULL,
  criacao datetime NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY usuario_email_UN (email),
  KEY usuario_exclusao_IX (exclusao),
  KEY usuario_idperfil_FK_IX (idperfil),
  CONSTRAINT usuario_idperfil_FK FOREIGN KEY (idperfil) REFERENCES perfil (id) ON DELETE RESTRICT ON UPDATE RESTRICT
);

INSERT INTO usuario (email, nome, idperfil, senha, token, criacao) VALUES ('admin@espm.br', 'Administrador', 1, 'NsSzgX9AXd2G85aiCOrUwAFkiEHrHYljYWpJBCfqOvKr:WD+jsEW/Dswcivs42EZBZREfm+4WaPcZHRPG5LJpD8yr', NULL, NOW());

-- DROP TABLE IF EXISTS voo;
CREATE TABLE voo (
  idVoo int NOT NULL AUTO_INCREMENT,
  origem VARCHAR(40) NOT NULL,
  destino VARCHAR(40) NOT NULL,
  destinoSigla VARCHAR(3) NOT NULL,
  regiao VARCHAR(40) NOT NULL,
  PRIMARY KEY (idVoo)
);

-- DROP TABLE IF EXISTS passagem;
CREATE TABLE passagem (
  idPassagem int NOT NULL AUTO_INCREMENT,
  idVoo int NOT NULL,
  companhia varchar(10) NOT NULL,
  media decimal(9,2) NOT NULL,
  dataVoo date NOT NULL,
  dataPesquisa date NOT NULL,
  PRIMARY KEY (idPassagem),
  KEY passagem_idvoo_FK_IX (idVoo),
  CONSTRAINT passagem_idvoo_FK FOREIGN KEY (idVoo) REFERENCES voo (idVoo) ON DELETE CASCADE ON UPDATE RESTRICT
);


-- DROP TABLE IF EXISTS tp_passagem;
CREATE TABLE tp_passagem (
  idTpPassagem int NOT NULL AUTO_INCREMENT,
  tipoPassagem varchar(10) NOT NULL,
  idPassagem int NOT NULL,
  hSaida char(5) NOT NULL,
  hChegada char(5) NOT NULL,
  duracao char(5) NOT NULL,
  preco decimal(9,2) NOT NULL,
  PRIMARY KEY (idTpPassagem),
  KEY passagem_idtppassagem_FK_IX (idPassagem),
  CONSTRAINT passagem_idtppassagem_FK FOREIGN KEY (idPassagem) REFERENCES passagem (idPassagem) ON DELETE CASCADE ON UPDATE RESTRICT
);

INSERT INTO `voo` VALUES 
(1,'São Paulo, GRU - Brasil','Rio Branco, RBR - Brasil','RBR', 'N'),
(2,'São Paulo, GRU - Brasil','Maceió, MCZ - Brasil','MCZ', 'NE'),
(3,'São Paulo, GRU - Brasil','Manaus, MAO - Brasil','MAO', 'N'),
(4,'São Paulo, GRU - Brasil','Salvador da Bahia, SSA - Brasil','SSA', 'NE'),
(5,'São Paulo, GRU - Brasil','Fortaleza, FOR - Brasil','FOR', 'NE'),
(6,'São Paulo, GRU - Brasil','Brasília, BSB - Brasil','BSB', 'CO'),
(7,'São Paulo, GRU - Brasil','Vitória, VIX - Brasil','VIX', 'SE'),
(8,'São Paulo, GRU - Brasil','Goiânia, GYN - Brasil','GYN', 'CO'),
(9,'São Paulo, GRU - Brasil','São Luís, SLZ - Brasil','SLZ', 'NE'),
(10,'São Paulo, GRU - Brasil','Cuiabá, CGB - Brasil','CGB', 'CO'),
(11,'São Paulo, GRU - Brasil','Campo Grande, CGR - Brasil','CGR', 'CO'),
(12,'São Paulo, GRU - Brasil','Belo Horizonte, CNF - Brasil','CNF', 'SE'),
(13,'São Paulo, GRU - Brasil','Belém, BEL - Brasil','BEL', 'N'),
(14,'São Paulo, GRU - Brasil','João Pessoa, JPA - Brasil','JPA', 'NE'),
(15,'São Paulo, GRU - Brasil','Curitiba, CWB - Brasil','CWB', 'S'),
(16,'São Paulo, GRU - Brasil','Recife, REC - Brasil','REC', 'NE'),
(17,'São Paulo, GRU - Brasil','Teresina, THE - Brasil','THE', 'NE'),
(18,'São Paulo, GRU - Brasil','Rio de Janeiro, SDU - Brasil','SDU', 'SE'),
(19,'São Paulo, GRU - Brasil','Natal, NAT - Brasil','NAT', 'NE'),
(20,'São Paulo, GRU - Brasil','Porto Alegre, POA - Brasil','POA', 'S'),
(21,'São Paulo, GRU - Brasil','Florianópolis, FLN - Brasil','FLN', 'S'),
(22,'São Paulo, GRU - Brasil','Aracaju, AJU - Brasil','AJU', 'NE'),
(23,'São Paulo, GRU - Brasil','Palmas, PMW - Brasil','PMW', 'N');
