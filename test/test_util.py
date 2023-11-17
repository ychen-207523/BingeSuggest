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
        db = mysql.connector.connect(user='root', password='testrootpass',
                                host='127.0.0.1')
        executor = db.cursor()
        executor.execute("USE testDB;")
        createAccount(db, "test@test.com", "testUser", "testPassword")
        expectedUserName="testUser"
        expectedEmail = "test@test.com"
        expectedPassword="testPassword"
        executor = db.cursor()
        executor.execute("SELECT * FROM users;")
        dbResult = executor.fetchall()
        self.assertTrue(len(dbResult) > 0)
        self.assertEqual(expectedUserName, dbResult[0][1])
        self.assertEqual(expectedEmail, dbResult[0][2])
        self.assertEqual(expectedPassword, dbResult[0][3])
        id = logintoAccount(db, "testUser", "testPassword")
        expectedId = 1
        self.assertEqual(expectedId, id)
        fail = logintoAccount(db, "testUser", "wrongPassword")
        self.assertIsNone(fail)
        db.close()




if __name__ == "__main__":
    unittest.main()
