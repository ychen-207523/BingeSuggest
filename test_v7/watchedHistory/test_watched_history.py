import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position
from src.recommenderapp.utils import create_account
from src.recommenderapp.app import app


class TestWatchedHistoryAPI(unittest.TestCase):
    """
    Test cases for WatchedHistory API functionality.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the database and tables before any tests are run.
        """
        load_dotenv()
        cls.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1", database="testDB"
        )
        cls.executor = cls.db.cursor()
        cls.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cls.executor.execute("DROP TABLE IF EXISTS WatchedHistory;")
        cls.executor.execute("DROP TABLE IF EXISTS Users;")
        cls.executor.execute("DROP TABLE IF EXISTS Movies;")
        cls.executor.execute("SET FOREIGN_KEY_CHECKS=1;")

        cls.executor.execute(
            """
            CREATE TABLE Users (
                idUsers INT NOT NULL AUTO_INCREMENT,
                username VARCHAR(45) NOT NULL,
                email VARCHAR(45) NOT NULL,
                password VARCHAR(64) NOT NULL,
                PRIMARY KEY (idUsers),
                UNIQUE INDEX username_UNIQUE (username ASC),
                UNIQUE INDEX email_UNIQUE (email ASC)
            );
        """
        )
        cls.executor.execute(
            """
            CREATE TABLE Movies (
                idMovies INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(128) NOT NULL,
                imdb_id VARCHAR(45) NOT NULL,
                PRIMARY KEY (idMovies),
                UNIQUE INDEX imdb_id_UNIQUE (imdb_id ASC)
            );
        """
        )
        cls.executor.execute(
            """
            CREATE TABLE WatchedHistory (
                idWatchedHistory INT NOT NULL AUTO_INCREMENT,
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                watched_date DATETIME NOT NULL,
                PRIMARY KEY (idWatchedHistory),
                FOREIGN KEY (user_id) REFERENCES Users (idUsers) ON DELETE CASCADE,
                FOREIGN KEY (movie_id) REFERENCES Movies (idMovies) ON DELETE CASCADE
            );
        """
        )
        cls.db.commit()

        cls.executor.execute(
            """
            INSERT INTO Movies (idMovies, name, imdb_id) VALUES 
            (11, 'Star Wars (1977)', 'tt0076759'),
            (12, 'Finding Nemo (2003)', 'tt0266543');
        """
        )
        cls.db.commit()

        app.config["TESTING"] = True
        cls.client = app.test_client()

    def setUp(self):
        """
        Set up the database connection before each test.
        """
        self.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1", database="testDB"
        )
        self.executor = self.db.cursor()

    def tearDown(self):
        """
        Close the database connection after each test.
        """
        if self.db.is_connected():
            self.db.close()

    @patch("src.recommenderapp.app.user", new=("tester2", 1))
    def test_add_duplicate_to_watched_history(self):
        """
        Test adding the same movie twice to watched history.
        """
        # Create a new user
        create_account(self.db, "tester2@test.com", "tester2", "password123")

        # Add the movie to watched history
        response1 = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json["status"], "success")

        # Attempt to add the same movie again
        response2 = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json["status"], "info")

    @patch("src.recommenderapp.app.user", new=("tester3", 2))
    def test_add_to_watched_history(self):
        """
        Test adding a single movie to watched history.
        """
        create_account(self.db, "tester3@test.com", "tester3", "password123")

        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0266543", "watched_date": "2024-11-23 12:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("tester4", 3))
    def test_get_watched_history(self):
        """
        Test retrieving watched history.
        """
        create_account(self.db, "tester4@test.com", "tester4", "password123")

        # Add a movie to watched history
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)
        self.assertEqual(response.json[0]["movie_name"], "Star Wars (1977)")

    @patch("src.recommenderapp.app.user", new=("tester5", 4))
    def test_remove_from_watched_history(self):
        """
        Test removing a movie from watched history.
        """
        create_account(self.db, "tester5@test.com", "tester5", "password123")

        # Add a movie to watched history
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        # Remove the movie
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
