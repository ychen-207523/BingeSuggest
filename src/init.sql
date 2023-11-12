CREATE TABLE IF NOT EXISTS `PopcornPicksDB`.`Users` (
  `idUsers` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idUsers`),
  UNIQUE INDEX `idUsers_UNIQUE` (`idUsers` ASC) VISIBLE,
  UNIQUE INDEX `username_UNIQUE` (`username` ASC) VISIBLE,
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE)
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `PopcornPicksDB`.`Movies` (
  `idMovies` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(45) NOT NULL,
  `imdb_id` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idMovies`),
  UNIQUE INDEX `idMovies_UNIQUE` (`idMovies` ASC) VISIBLE,
  UNIQUE INDEX `imdb_id_UNIQUE` (`imdb_id` ASC) VISIBLE)
ENGINE = InnoDB

CREATE TABLE IF NOT EXISTS `PopcornPicksDB`.`Ratings` (
  `idRatings` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `movie_id` INT NOT NULL,
  `score` INT NOT NULL,
  `review` VARCHAR(45) NULL,
  PRIMARY KEY (`idRatings`),
  UNIQUE INDEX `idRatings_UNIQUE` (`idRatings` ASC) VISIBLE,
  INDEX `user_id_idx` (`user_id` ASC) VISIBLE,
  INDEX `movie_id_idx` (`movie_id` ASC) VISIBLE,
  CONSTRAINT `user_id`
    FOREIGN KEY (`user_id`)
    REFERENCES `PopcornPicksDB`.`Users` (`idUsers`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `movie_id`
    FOREIGN KEY (`movie_id`)
    REFERENCES `PopcornPicksDB`.`Movies` (`idMovies`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB