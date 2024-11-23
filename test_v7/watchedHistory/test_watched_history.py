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
        # Generate test-specific user info with length constraints
        self.test_email = f"user{self._testMethodName[:30]}@test.com"
        self.test_username = f"u{self._testMethodName[:35]}"
        self.test_password = "password123"

        create_account(self.db, self.test_email, self.test_username, self.test_password)

        # Fetch user_id
        self.executor.execute(
            "SELECT idUsers FROM Users WHERE username = %s;", (self.test_username,)
        )
        user_id_row = self.executor.fetchone()
        self.user_id = user_id_row[0] if user_id_row else None

        # Validate user_id
        if not self.user_id:
            raise ValueError(
                f"Failed to create or fetch user_id for {self.test_username}"
            )

        global user
        user = (self.test_username, self.user_id)
        print(f"Set user context: {user}")

    def test_user_creation_and_watched_history(self):
        create_account(self.db, "debug@test.com", "debug_user", "password123")
        self.db.commit()

        self.executor.execute("SELECT * FROM Users WHERE username = 'debug_user';")
        print("Users Table:", self.executor.fetchall())
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        self.executor.execute("SELECT * FROM WatchedHistory;")
        print("WatchedHistory Table:", self.executor.fetchall())
