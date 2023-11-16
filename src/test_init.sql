CREATE DATABASE IF NOT EXISTS testDB;

-- Switch to the testDB database
USE testDB;

-- Create the Users table
CREATE TABLE IF NOT EXISTS Users (
  idUsers INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(45) NOT NULL,
  email VARCHAR(45) NOT NULL,
  password VARCHAR(45) NOT NULL,
  PRIMARY KEY (idUsers),
  UNIQUE INDEX username_UNIQUE (username ASC),
  UNIQUE INDEX email_UNIQUE (email ASC)
) ENGINE = InnoDB;

-- Create the Movies table
CREATE TABLE IF NOT EXISTS Movies (
  idMovies INT NOT NULL AUTO_INCREMENT,
  name VARCHAR(45) NOT NULL,
  imdb_id VARCHAR(45) NOT NULL,
  PRIMARY KEY (idMovies),
  UNIQUE INDEX imdb_id_UNIQUE (imdb_id ASC)
) ENGINE = InnoDB;

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
    REFERENCES Users (idUsers)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT movie_id
    FOREIGN KEY (movie_id)
    REFERENCES Movies (idMovies)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
) ENGINE = InnoDB;