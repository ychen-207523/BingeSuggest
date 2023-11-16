"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""

import sys
import unittest
import warnings
import os
from pathlib import Path
import mysql.connector
import pandas as pd
sys.path.append(str(Path(__file__).resolve().parents[1]))
#pylint: disable=wrong-import-position
from src.recommenderapp.utils import create_colored_tags, \
    beautify_feedback_data, create_movie_genres, send_email_to_user, createAccount, logintoAccount
#pylint: enable=wrong-import-position

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for utility functions
    """

    def test_beautify_feedback_data(self):
        """
        Test case 1
        """
        data = {'Movie 1': 'Yet to watch',
                'Movie 2': 'Like', 'Movie 3': 'Dislike'}
        result = beautify_feedback_data(data)
        expected_result = {"Liked": ['Movie 2'], "Disliked": [
            'Movie 3'], "Yet to Watch": ['Movie 1']}

        self.assertTrue(result == expected_result)

    def test_create_colored_tags(self):
        """
        Test case 2
        """
        expected_result = '<span style="background-color: #FF1493; color: #FFFFFF; \
            padding: 5px; border-radius: 5px;">Musical</span>'
        result = create_colored_tags(['Musical'])
        self.assertTrue(result == expected_result)

    def test_create_movie_genres(self):
        """
        Test case 3
        """
        expected_result = {'Toy Story (1995)': ['Animation', 'Comedy', 'Family'], \
                           'Jumanji (1995)': [
            'Adventure', 'Fantasy', 'Family']}

        data = [["862", "Toy Story (1995)", "Animation|Comedy|Family", \
                 "tt0114709", " ", "/rhIRbceoE9lR4veEXuwCC2wARtG.jpg", "81"], \
                ["8844", "Jumanji (1995)", "Adventure|Fantasy|Family", "tt0113497", " ", \
                  "/vzmL6fP7aPKNKPRTFnZmiUfciyV.jpg", "104"]]

        movie_genre_df = pd.DataFrame(data, columns=[
            'movieId', 'title', 'genres', 'imdb_id', 'overview', 'poster_path', 'runtime'])

        result = create_movie_genres(movie_genre_df)
        self.assertTrue(result == expected_result)

    def test_send_email_to_user(self):
        """
        Test case 4
        """
        data = {"Liked": ['Toy Story (1995)'], "Disliked": [
            'Cutthroat Island (1995)'], "Yet to Watch": ['Assassins (1995)']}
        with self.assertRaises(Exception):
            send_email_to_user("wrong_email", beautify_feedback_data(data))
    
    def test_accounts(self):
        """
        Test case 5
        """
        db = mysql.connector.connect(user='root', password=os.getenv('DB_PASSWORD'),
                                host='127.0.0.1')
        self.setUpMockDB(db)
        createAccount(db, "test@test.com", "testUser", "testPassword")
        expectedUserName="testUser"
        expectedEmail = "test@test.com"
        expectedPassword="testPassword"
        executor = db.cursor()
        executor.execute("SELECT * FROM  testdb.users;")
        dbResult = executor.fetchall()
        self.assertEqual(expectedUserName, dbResult[0][1])
        self.assertEqual(expectedEmail, dbResult[0][2])
        self.assertEqual(expectedPassword, dbResult[0][3])
        id = logintoAccount(db, "testUser", "testPassword")
        expectedId = 1
        self.assertEqual(expectedId, id)
        fail = logintoAccount(db, "testUser", "wrongPassword")
        self.assertIsNone(fail)
        db.close()
    

    def setUpMockDB(self, db):
        exector = db.cursor()
        exector.execute("DROP DATABASE IF EXISTS testDB;")
        exector.execute("CREATE DATABASE testDB;")
        exector.execute("USE testDB;")
        exector.execute("""
                        CREATE TABLE IF NOT EXISTS Users (
                        idUsers INT NOT NULL AUTO_INCREMENT,
                        username VARCHAR(45) NOT NULL,
                        email VARCHAR(45) NOT NULL,
                        password VARCHAR(45) NOT NULL,
                        PRIMARY KEY (idUsers),
                        UNIQUE INDEX username_UNIQUE (username ASC),
                        UNIQUE INDEX email_UNIQUE (email ASC)
                        ) ENGINE = InnoDB;
                        """)
        exector.execute("""
                        CREATE TABLE IF NOT EXISTS Movies (
                        idMovies INT NOT NULL AUTO_INCREMENT,
                        name VARCHAR(45) NOT NULL,
                        imdb_id VARCHAR(45) NOT NULL,
                        PRIMARY KEY (idMovies),
                        UNIQUE INDEX imdb_id_UNIQUE (imdb_id ASC)
                        ) ENGINE = InnoDB;
                        """)
        exector.execute("""
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
                        """)




if __name__ == "__main__":
    unittest.main()
