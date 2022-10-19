-- Esse script vale para o MySQL 8.x. Se seu MySQL for 5.x, precisa executar essa linha comentada:
-- CREATE DATABASE IF NOT EXISTS gallery;
CREATE DATABASE IF NOT EXISTS gallery DEFAULT CHARACTER SET utf8mb4 DEFAULT COLLATE utf8mb4_0900_ai_ci;

USE gallery;

CREATE TABLE usuario (
  id_usuario int NOT NULL AUTO_INCREMENT,
  nome varchar(50) NOT NULL,
  sobrenome varchar(50) NOT NULL,
  apelido varchar(50) NOT NULL,
  email varchar(50) NOT NULL,
  senha varchar(50) NOT NULL,
  PRIMARY KEY (id_usuario),
  UNIQUE KEY apelido_UN (apelido),
  UNIQUE KEY email_UN (email)
);

CREATE TABLE arte (
  id_arte int NOT NULL AUTO_INCREMENT,
  titulo_arte varchar(50) NOT NULL,
  autor varchar(50) NOT NULL,
  tema varchar(50) NOT NULL,
  sobre varchar(50),
  PRIMARY KEY (id_arte)
);
