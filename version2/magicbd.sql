DROP TABLE IF EXISTS Carta_Pool;
DROP TABLE IF EXISTS Carta_Elegido;
DROP TABLE IF EXISTS Pool;
DROP TABLE IF EXISTS Elegido;
DROP TABLE IF EXISTS Registro;
DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Sinergias;
DROP TABLE IF EXISTS Carta;
DROP TABLE IF EXISTS Coleccion;

ALTER DATABASE magicbd CHARACTER SET utf8 COLLATE utf8_unicode_ci;

CREATE TABLE Coleccion(
  nombre VARCHAR (25) UNIQUE NOT NULL,
  codigo VARCHAR(3) PRIMARY KEY,
  bloque VARCHAR (25)
);

CREATE TABLE Carta(
  nombre VARCHAR(25) NOT NULL,
  nombre_original VARCHAR(30) NOT NULL,
  coleccion VARCHAR(3) NOT NULL,
  color VARCHAR (1) NOT NULL,
  coste_mana TEXT NOT NULL,
  rareza VARCHAR(1) NOT NULL,
  nota_fireball REAL NOT NULL,
  coste_medio REAL,
  tipo text NOT NULL,
  texto text NOT NULL,
  FOREIGN KEY (coleccion) references Coleccion(codigo),
  PRIMARY KEY (nombre, coleccion)
);

CREATE TABLE Sinergias(
  carta1 VARCHAR(25) NOT NULL,
  carta2 VARCHAR(25) NOT NULL,
  nota REAL NOT NULL,
  FOREIGN KEY (carta1) references Carta(nombre),
  FOREIGN KEY (carta2) references Carta(nombre),
  PRIMARY KEY (carta1, carta2)
);

  CREATE TABLE Usuario(
    username VARCHAR(25) NOT NULL PRIMARY KEY,
    password TEXT NOT NULL
  );
CREATE TABLE Registro(
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  usuario VARCHAR(25) NOT NULL,
  FOREIGN KEY (usuario) references Usuario(username)
);

CREATE TABLE Pool(
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  registro INTEGER NOT NULL,
  FOREIGN KEY (registro) references Registro(id)
);

CREATE TABLE Elegido(
  id INTEGER AUTO_INCREMENT PRIMARY KEY,
  registro INTEGER NOT NULL,
  FOREIGN KEY (registro) references Registro(id)
);

CREATE TABLE Carta_Pool(
  carta VARCHAR(25) NOT NULL,
  id_pool INTEGER NOT NULL,
  FOREIGN KEY (carta) references Carta(nombre),
  FOREIGN KEY (id_pool) references Pool(id),
  PRIMARY KEY (carta, id_pool)
);

CREATE TABLE Carta_Elegido(
  carta VARCHAR(25) NOT NULL,
  id_elegido INTEGER NOT NULL,
  FOREIGN KEY (carta) references Carta(nombre),
  FOREIGN KEY (id_elegido) references Elegido(id),
  PRIMARY KEY (carta, id_elegido)
);

ALTER TABLE Carta CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Sinergias CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Usuario CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Registro CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Pool CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Elegido CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Carta_Pool CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
ALTER TABLE Carta_Elegido CONVERT TO CHARACTER SET utf8 COLLATE utf8_unicode_ci;
