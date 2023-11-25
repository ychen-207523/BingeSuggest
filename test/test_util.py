"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
# pylint: disable=wrong-import-position
# pylint: disable=wrong-import-order
# pylint: disable=import-error
import sys
import unittest
import warnings
import os
import hashlib
import flask
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))
# pylint: disable=wrong-import-position
from src.recommenderapp.utils import (
    create_colored_tags,
    beautify_feedback_data,
    create_movie_genres,
    send_email_to_user,
    create_account,
    login_to_account,
    get_wall_posts,
    get_username,
)

# pylint: enable=wrong-import-position

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for utility functions
    """

    def setUp(self):
        print("\nrunning setup method")
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password=os.getenv("DB_PASSWORD"), host="127.0.0.1"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        executor.execute("DELETE FROM users WHERE username = 'testUser'")
        executor.execute("DELETE FROM Ratings WHERE idRatings > 0")
        db.commit()

    def test_beautify_feedback_data(self):
        """
        Test case 1
        """
        data = {"Movie 1": "Yet to watch", "Movie 2": "Like", "Movie 3": "Dislike"}
        result = beautify_feedback_data(data)
        expected_result = {
            "Liked": ["Movie 2"],
            "Disliked": ["Movie 3"],
            "Yet to Watch": ["Movie 1"],
        }

        self.assertTrue(result == expected_result)

    def test_create_colored_tags(self):
        """
        Test case 2
        """
        expected_result = '<span style="background-color: #FF1493; color: #FFFFFF; \
            padding: 5px; border-radius: 5px;">Musical</span>'
        result = create_colored_tags(["Musical"])
        self.assertTrue(result == expected_result)

    def test_create_movie_genres(self):
        """
        Test case 3
        """
        expected_result = {
            "Toy Story (1995)": ["Animation", "Comedy", "Family"],
            "Jumanji (1995)": ["Adventure", "Fantasy", "Family"],
        }

        data = [
            [
                "862",
                "Toy Story (1995)",
                "Animation|Comedy|Family",
                "tt0114709",
                " ",
                "/rhIRbceoE9lR4veEXuwCC2wARtG.jpg",
                "81",
            ],
            [
                "8844",
                "Jumanji (1995)",
                "Adventure|Fantasy|Family",
                "tt0113497",
                " ",
                "/vzmL6fP7aPKNKPRTFnZmiUfciyV.jpg",
                "104",
            ],
        ]

        movie_genre_df = pd.DataFrame(
            data,
            columns=[
                "movieId",
                "title",
                "genres",
                "imdb_id",
                "overview",
                "poster_path",
                "runtime",
            ],
        )

        result = create_movie_genres(movie_genre_df)
        self.assertTrue(result == expected_result)

    def test_send_email_to_user(self):
        """
        Test case 4
        """
        data = {
            "Liked": ["Toy Story (1995)"],
            "Disliked": ["Cutthroat Island (1995)"],
            "Yet to Watch": ["Assassins (1995)"],
        }
        with self.assertRaises(Exception):
            send_email_to_user("wrong_email", beautify_feedback_data(data))

    def test_accounts(self):
        """
        Test case 5
        """
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password=os.getenv("DB_PASSWORD"), host="127.0.0.1"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "test@test.com", "testUser", "testPassword")
        expected_username = "testUser"
        expected_email = "test@test.com"
        expected_password = "testPassword"
        new_pass = (expected_password + os.getenv("SALT") + expected_username).encode()
        # now hash it
        h = hashlib.sha256()
        h.update(new_pass)
        executor = db.cursor()
        executor.execute("SELECT * FROM users;")
        db_result = executor.fetchall()
        self.assertTrue(len(db_result) > 0)
        self.assertEqual(expected_username, db_result[0][1])
        self.assertEqual(expected_email, db_result[0][2])
        self.assertEqual(h.hexdigest(), db_result[0][3])
        fail = login_to_account(db, "testUser", "wrongPassword")
        self.assertIsNone(fail)
        db.close()

    def test_get_wall_posts(self):
        """
        Test case 6
        """
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password=os.getenv("DB_PASSWORD"), host="127.0.0.1"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        create_account(db, "test@test.com", "testUser", "testPassword")
        executor.execute("SELECT idUsers FROM users WHERE username='testUser'")
        db_result = executor.fetchall()
        user = db_result[0][0]
        executor.execute(
            "INSERT INTO Ratings(user_id, movie_id, score, review, time) \
                         VALUES (%s, %s, %s, %s, %s);",
            (int(user), int(11), int(4), "this is a great movie", "1970-01-01"),
        )
        db.commit()
        app = flask.Flask(__name__)
        a = ""
        with app.test_request_context("/"):
            a = get_wall_posts(db)
        self.assertEqual(a.json[0]["imdb_id"], "tt0076759")
        self.assertEqual(a.json[0]["name"], "Star Wars (1977)")
        self.assertEqual(a.json[0]["review"], "this is a great movie")
        self.assertEqual(a.json[0]["score"], 4)

    # def test_get_recent_movies(self):
    def test_get_username(self):
        """
        Test case 7
        """
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password=os.getenv("DB_PASSWORD"), host="127.0.0.1"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "test@test.com", "testUser", "testPassword")
        user = login_to_account(db, "testUser", "testPassword")
        app = flask.Flask(__name__)
        username = ""
        with app.test_request_context("/"):
            username = get_username(db, user).json
        self.assertEqual("testUser", username)

    # def test_get_friends(self):


if __name__ == "__main__":
    unittest.main()
