import sys
import unittest
from unittest.mock import patch
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.recommenderapp.utils import create_account
from src.recommenderapp.app import app


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for WatchedHistory functionality.
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
            (12, 'Finding Nemo (2003)', 'tt0266543'),
            (13, 'Forrest Gump (1994)', 'tt0109830'),
            (14, 'American Beauty (1999)', 'tt0169547'),
            (15, 'Citizen Kane (1941)', 'tt0033467'),
            (16, 'Dancer in the Dark (2000)', 'tt0168629');
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

    @patch("src.recommenderapp.app.user", new=("user1", 1))
    def test_add_to_watched_history(self):
        """
        Test that a user can add a movie to their watched history.
        """
        create_account(self.db, "user1@test.com", "user1", "password123")
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user2", 2))
    def test_add_duplicate_to_watched_history(self):
        """
        Test that a user cannot add the same movie to their watched history more
        """
        create_account(self.db, "user2@test.com", "user2", "password123")
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "info")

    @patch("src.recommenderapp.app.user", new=("user3", 3))
    def test_get_watched_history(self):
        """
        Test that a user can get their watched history.
        """
        create_account(self.db, "user3@test.com", "user3", "password123")
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

    @patch("src.recommenderapp.app.user", new=("user4", 4))
    def test_remove_from_watched_history(self):
        """
        Test that a user can remove a movie from their watched
        """
        create_account(self.db, "user4@test.com", "user4", "password123")
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user5", 5))
    def test_empty_watched_history(self):
        """
        Test that a user can get their watched history even if they have not added any movies.
        """
        create_account(self.db, "user5@test.com", "user5", "password123")
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

