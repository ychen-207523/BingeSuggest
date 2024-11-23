import sys
import unittest
import warnings
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position
from src.recommenderapp.utils import create_account
from src.recommenderapp.app import app

# pylint: enable=wrong-import-position
warnings.filterwarnings("ignore")


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for WatchedHistory functionality.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the database and create tables for all tests.
        """
        print("\nRunning SetupClass Method")
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

        # Insert movies into the Movies table
        cls.executor.execute(
            """
            INSERT INTO Movies (idMovies, name, imdb_id) VALUES 
            (2, 'Ariel (1988)', 'tt0094675'),
            (3, 'Shadows in Paradise (1986)', 'tt0092149'),
            (5, 'Four Rooms (1995)', 'tt0113101'),
            (6, 'Judgment Night (1993)', 'tt0107286'),
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

    @classmethod
    def tearDownClass(cls):
        """
        Close the database connection after all tests.
        """
        print("\nRunning TearDownClass Method")
        if cls.db.is_connected():
            cls.db.close()

    def setUp(self):
        """
        Create a unique user for each test.
        """
        print("\nRunning Setup Method")
        self.test_email = f"testuser{self._testMethodName}@test.com"
        self.test_username = f"testuser{self._testMethodName}"
        self.test_password = "password123"
        create_account(self.db, self.test_email, self.test_username, self.test_password)

        self.executor.execute(
            "SELECT idUsers FROM Users WHERE username = %s;", (self.test_username,)
        )
        self.user_id = self.executor.fetchone()[0]

    def test_add_single_movie_to_watched_history(self):
        """Add a single movie to the watched history."""
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_add_duplicate_movie_to_watched_history(self):
        """Ensure adding duplicate movie is handled correctly."""
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
        self.assertEqual(response.json["status"], "info")

    def test_get_watched_history(self):
        """Retrieve watched history."""
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        response = self.client.get("/getWatchedHistoryData")
        self.assertGreater(len(response.json), 0)
        self.assertEqual(response.json[0]["movie_name"], "Star Wars (1977)")

    def test_multiple_movies_in_watched_history(self):
        """Add multiple movies and ensure they're recorded correctly."""
        movie_ids = ["tt0076759", "tt0094675", "tt0092149"]
        for imdb_id in movie_ids:
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps(
                    {"imdb_id": imdb_id, "watched_date": "2024-11-23 10:00:00"}
                ),
                content_type="application/json",
            )
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(len(response.json), len(movie_ids))

    def test_empty_watched_history(self):
        """Ensure watched history is empty initially."""
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(len(response.json), 0)

    def test_add_movie_not_in_database(self):
        """Test adding a movie that doesn't exist in the Movies table."""
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt9999999", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.json["status"], "error")

    def test_add_multiple_movies_by_different_users(self):
        """Ensure different users' watched histories are handled separately."""
        create_account(self.db, "user1@test.com", "user1", "pass1")
        create_account(self.db, "user2@test.com", "user2", "pass2")
        self.executor.execute(
            "SELECT idUsers FROM Users WHERE username = %s;", ("user1",)
        )
        user1_id = self.executor.fetchone()[0]
        self.executor.execute(
            "SELECT idUsers FROM Users WHERE username = %s;", ("user2",)
        )
        user2_id = self.executor.fetchone()[0]

        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0094675", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
