CREATE DATABASE IF NOT EXISTS testDB;

-- Switch to the testDB database
USE testDB;

-- Create the Users table
CREATE TABLE IF NOT EXISTS users (
  idUsers INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  password VARCHAR(64) NOT NULL,
  PRIMARY KEY (idUsers),
  UNIQUE INDEX username_UNIQUE (username ASC),
  UNIQUE INDEX email_UNIQUE (email ASC)
);

-- Create the Movies table
CREATE TABLE IF NOT EXISTS Movies (
  idMovies INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  imdb_id VARCHAR(45) NOT NULL,
  PRIMARY KEY (idMovies),
  UNIQUE INDEX imdb_id_UNIQUE (imdb_id ASC)
);

-- Create the Ratings table
CREATE TABLE IF NOT EXISTS Ratings (
  idRatings INT NOT NULL AUTO_INCREMENT,
  user_id INT NOT NULL,
  movie_id INT NOT NULL,
  score INT NOT NULL,
  review VARCHAR(45) NULL,
  time DATETIME NOT NULL,
  PRIMARY KEY (idRatings),
  INDEX user_id_idx (user_id ASC),
  INDEX movie_id_idx (movie_id ASC),
  CONSTRAINT user_id
    FOREIGN KEY (user_id)
    REFERENCES users (idUsers)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT movie_id
    FOREIGN KEY (movie_id)
    REFERENCES Movies (idMovies)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
);

INSERT INTO movies (idMovies, name, imdb_id) VALUES (2, 'Ariel (1988)', 'tt0094675');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (3, 'Shadows in Paradise (1986)', 'tt0092149');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (5, 'Four Rooms (1995)', 'tt0113101');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (6, 'Judgment Night (1993)', 'tt0107286');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (11, 'Star Wars (1977)', 'tt0076759');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (12, 'Finding Nemo (2003)', 'tt0266543');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (13, 'Forrest Gump (1994)', 'tt0109830');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (14, 'American Beauty (1999)', 'tt0169547');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (15, 'Citizen Kane (1941)', 'tt0033467');
INSERT INTO movies (idMovies, name, imdb_id) VALUES (16, 'Dancer in the Dark (2000)', 'tt0168629');
