import sys
import unittest
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

        cls.executor.execute("""
            CREATE TABLE Users (
                idUsers INT NOT NULL AUTO_INCREMENT,
                username VARCHAR(45) NOT NULL,
                email VARCHAR(45) NOT NULL,
                password VARCHAR(64) NOT NULL,
                PRIMARY KEY (idUsers),
                UNIQUE INDEX username_UNIQUE (username ASC),
                UNIQUE INDEX email_UNIQUE (email ASC)
            );
        """)
        cls.executor.execute("""
            CREATE TABLE Movies (
                idMovies INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(128) NOT NULL,
                imdb_id VARCHAR(45) NOT NULL,
                PRIMARY KEY (idMovies),
                UNIQUE INDEX imdb_id_UNIQUE (imdb_id ASC)
            );
        """)
        cls.executor.execute("""
            CREATE TABLE WatchedHistory (
                idWatchedHistory INT NOT NULL AUTO_INCREMENT,
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                watched_date DATETIME NOT NULL,
                PRIMARY KEY (idWatchedHistory),
                FOREIGN KEY (user_id) REFERENCES Users (idUsers) ON DELETE CASCADE,
                FOREIGN KEY (movie_id) REFERENCES Movies (idMovies) ON DELETE CASCADE
            );
        """)
        cls.db.commit()

        cls.executor.execute("""
            INSERT INTO Movies (idMovies, name, imdb_id) VALUES 
            (11, 'Star Wars (1977)', 'tt0076759'),
            (12, 'Finding Nemo (2003)', 'tt0266543');
        """)
        cls.db.commit()

        app.config["TESTING"] = True
        cls.client = app.test_client()

    @classmethod
    def tearDownClass(cls):
        if cls.db.is_connected():
            cls.db.close()

    def setUp(self):
        """
        Create a unique user for each test and set the `user` context.
        """
        self.test_email = f"user_{self._testMethodName}@test.com"
        self.test_username = f"user_{self._testMethodName}"
        self.test_password = "password123"

        create_account(self.db, self.test_email, self.test_username, self.test_password)
        self.executor.execute("SELECT idUsers FROM Users WHERE username = %s;", (self.test_username,))
        user_id_row = self.executor.fetchone()
        self.user_id = user_id_row[0] if user_id_row else None

        if not self.user_id:
            raise ValueError(f"Failed to create or fetch user_id for {self.test_username}")

        global user
        user = (self.test_username, self.user_id)

    def test_add_to_watched_history(self):
        """Test adding a movie to watched history via API."""
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")
        self.executor.execute("SELECT * FROM WatchedHistory WHERE user_id = %s;", (self.user_id,))
        self.assertEqual(len(self.executor.fetchall()), 1)

    def test_add_duplicate_to_watched_history(self):
        """Test adding the same movie twice via API."""
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}),
            content_type="application/json",
        )
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}),
            content_type="application/json",
        )
        self.assertEqual(response.json["status"], "info")

    def test_get_watched_history(self):
        """Test retrieving watched history via API."""
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}),
            content_type="application/json",
        )
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 1)

    def test_add_movie_not_in_database(self):
        """Test adding a movie not in the database."""
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt9999999", "watched_date": "2024-11-23 10:00:00"}),
            content_type="application/json",
        )
        self.assertEqual(response.json["status"], "error")

    def test_remove_from_watched_history(self):
        """Test removing a movie from watched history."""
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}),
            content_type="application/json",
        )
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.json["status"], "success")
        self.executor.execute("SELECT * FROM WatchedHistory WHERE user_id = %s;", (self.user_id,))
        self.assertEqual(len(self.executor.fetchall()), 0)
