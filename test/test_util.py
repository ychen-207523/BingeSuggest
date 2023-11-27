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
import bcrypt
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
    get_recent_movies,
    add_friend,
    get_friends,
    submit_review,
    get_recent_friend_movies,
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
        executor.execute("DELETE FROM Users")
        executor.execute("DELETE FROM Ratings")
        executor.execute("DELETE FROM Friends")
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
        expected_password = ("testPassword").encode("utf-8")
        executor = db.cursor()
        executor.execute("SELECT * FROM Users;")
        db_result = executor.fetchall()
        actual_password = (db_result[0][3]).encode("utf-8")
        self.assertTrue(len(db_result) > 0)
        self.assertEqual(expected_username, db_result[0][1])
        self.assertEqual(expected_email, db_result[0][2])
        self.assertTrue(bcrypt.checkpw(expected_password, actual_password))
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
        executor.execute("SELECT idUsers FROM Users WHERE username='testUser'")
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

    def test_get_recent_movies(self):
        """
        Test case 8
        """
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password=os.getenv("DB_PASSWORD"), host="127.0.0.1"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "test@test.com", "testUser", "testPassword")
        user = login_to_account(db, "testUser", "testPassword")

        movies_to_review = [
            (2, 3, "1970-01-06"),
            (3, 4, "1970-01-05"),
            (5, 5, "1970-01-04"),
            (6, 2, "1970-01-03"),
            (11, 1, "1970-01-02"),
            (12, 3, "1970-01-01"),
        ]
        for movie in movies_to_review:
            executor.execute(
                "INSERT INTO Ratings(user_id, movie_id, score, review, time) \
                             VALUES (%s, %s, %s, %s, %s);",
                (
                    int(user),
                    int(movie[0]),
                    int(movie[1]),
                    "this is a great movie",
                    movie[2],
                ),
            )
        db.commit()
        app = flask.Flask(__name__)
        recent_movies = []
        with app.test_request_context("/"):
            recent_movies = get_recent_movies(db, user)
        self.assertEqual(5, len(recent_movies.json))
        for i, movie in enumerate(recent_movies.json):
            self.assertEqual(movie["score"], movies_to_review[i][1])

    def test_friends(self):
        """
        Test case 9
        """
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password=os.getenv("DB_PASSWORD"), host="127.0.0.1"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "test@test.com", "testUser", "testPassword")
        user = login_to_account(db, "testUser", "testPassword")
        executor.execute(
            "INSERT INTO Users(username, email, password) VALUES \
                          ('testFriend', 'friend@test.com', 'testPassword')"
        )
        executor.execute(
            "INSERT INTO Users(username, email, password) VALUES \
                         ('testFriend2', 'friend2@test.com', 'testPassword')"
        )
        app = flask.Flask(__name__)

        result = ""
        with app.test_request_context("/"):
            add_friend(db, "testFriend", user)
            add_friend(db, "testFriend2", user)
            db.commit()

            result = get_friends(db, user)

        friends = []
        friends.append(result.json[0][0])
        friends.append(result.json[1][0])
        self.assertIn("testFriend", friends)
        self.assertIn("testFriend2", friends)

        executor.execute("SELECT idUsers FROM Users WHERE username = 'testFriend'")
        friend = executor.fetchall()[0][0]
        movies_to_review = [
            (2, 3, "1970-01-06"),
            (3, 4, "1970-01-05"),
            (5, 5, "1970-01-04"),
            (6, 2, "1970-01-03"),
            (11, 1, "1970-01-02"),
            (12, 3, "1970-01-01"),
        ]
        for movie in movies_to_review:
            executor.execute(
                "INSERT INTO Ratings(user_id, movie_id, score, review, time) \
                             VALUES (%s, %s, %s, %s, %s);",
                (
                    int(friend),
                    int(movie[0]),
                    int(movie[1]),
                    "this is a great movie",
                    movie[2],
                ),
            )
        db.commit()
        app = flask.Flask(__name__)
        result = []
        with app.test_request_context("/"):
            result = get_recent_friend_movies(db, "testFriend")
        self.assertEqual(5, len(result.json))
        for i, movie in enumerate(result.json):
            self.assertEqual(movie["score"], movies_to_review[i][1])

    def test_submit_review(self):
        """
        Test case 10
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

        result = ""
        with app.test_request_context("/"):
            submit_review(db, user, "Forrest Gump (1994)", 9, "testReview")
            db.commit()

            executor.execute("SELECT score FROM Ratings WHERE movie_id = 13")
            result = executor.fetchall()[0][0]
            self.assertEqual(9, int(result))


if __name__ == "__main__":
    unittest.main()
