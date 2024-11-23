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

    def setUp(self):
        """
        Set up the database and create a fresh user for each test.
        """
        print("\nRunning Setup Method")
        load_dotenv()

        # Connect to the test database
        self.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1", database="testDB"
        )
        self.executor = self.db.cursor()

        # Reset the tables for a clean state
        self.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.executor.execute("DELETE FROM WatchedHistory;")
        self.executor.execute("DELETE FROM Users;")
        self.executor.execute("DELETE FROM Movies;")
        self.db.commit()

        # Create a new account for each test
        self.test_email = "testuser@test.com"
        self.test_username = "testuser"
        self.test_password = "password123"
        create_account(self.db, self.test_email, self.test_username, self.test_password)

        # Fetch the created user's ID
        self.executor.execute(
            "SELECT idUsers FROM Users WHERE username = %s;", (self.test_username,)
        )
        self.user_id = self.executor.fetchone()[0]

        # Set up the Flask test client
        app.config["TESTING"] = True
        self.client = app.test_client()

        # Simulate a logged-in user
        global user
        user = (self.test_username, self.user_id)

    def tearDown(self):
        """
        Close the database connection after each test.
        """
        print("\nRunning TearDown Method")
        if self.db.is_connected():
            self.db.close()

    def test_add_to_watched_history(self):
        """
        Test adding a movie to the watched history.
        """
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

        # Verify the database entry
        self.executor.execute(
            "SELECT * FROM WatchedHistory WHERE user_id = %s AND movie_id = %s;",
            (self.user_id, 11),
        )
        result = self.executor.fetchone()
        self.assertIsNotNone(result, "Movie was not added to watched history.")

    def test_add_duplicate_to_watched_history(self):
        """
        Test adding the same movie twice to the watched history.
        """
        # Add the movie once
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        # Attempt to add the same movie again
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "info")

    def test_get_watched_history(self):
        """
        Test retrieving watched history.
        """
        # Add a movie to watched history
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        # Retrieve watched history
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)
        self.assertEqual(response.json[0]["movie_name"], "Star Wars (1977)")
