CREATE DATABASE proyectoIOTSM;

USE proyectoIOTSM;

CREATE TABLE superuser(
 idSUser INT AUTO_INCREMENT,
 name VARCHAR(75) NOT NULL,
 password VARCHAR(75) NOT NULL,
 
 CONSTRAINT pk_superuser_idSUser PRIMARY KEY(idSUser)
);

CREATE TABLE user(
 idUser INT AUTO_INCREMENT,
 idSU INT NOT NULL,
 name VARCHAR(75) NOT NULL,
 password VARCHAR(75) NOT NULL,
 
 CONSTRAINT pk_user_idUser PRIMARY KEY(idUser)
);

CREATE TABLE permiso(
 id INT AUTO_INCREMENT,
 idU INT NOT NULL,
 name VARCHAR(75) NOT NULL,
 acceso INT NULL,

 CONSTRAINT pk_user_idUser PRIMARY KEY(id)
 );

CREATE TABLE bitacora(
 id INT AUTO_INCREMENT,
 idU INT NOT NULL,

 fecha VARCHAR(20) NOT NULL,
 name VARCHAR(75) NOT NULL,
 agregar INT NULL,
 eliminar INT NULL,
 CONSTRAINT pk_user_idUser PRIMARY KEY(id)
);

SELECT * FROM `user`;