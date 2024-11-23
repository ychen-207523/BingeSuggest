"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
import unittest
import mysql.connector
import json
from dotenv import load_dotenv
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.recommenderapp.app import app
from src.recommenderapp.utils import create_account

class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for Watched History functionality.
    """

    def setUp(self):
        """
        Prepare the test database and create necessary initial data.
        """
        print("\nRunning Setup Method")
        load_dotenv()

        # Connect to the test database
        self.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1", database="testDB"
        )
        self.executor = self.db.cursor()

        # Clear relevant tables to ensure a clean state
        self.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.executor.execute("DELETE FROM WatchedHistory;")
        self.executor.execute("DELETE FROM Users;")
        self.executor.execute("DELETE FROM Movies;")
        self.executor.execute("SET FOREIGN_KEY_CHECKS=1;")
        self.db.commit()

        create_account(self.db, "testuser@test.com", "testuser", "password123")

        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'testuser';")
        self.user_id = self.executor.fetchone()[0]

        global user
        user = ("testuser", self.user_id)

        print(f"Created test user with ID {self.user_id}")

        self.db.commit()

    def tearDown(self):
        """
        Clean up the test environment after each test.
        """
        print("\nRunning TearDown Method")
        cursor = self.db.cursor()
        cursor.execute("DELETE FROM WatchedHistory;")
        self.db.commit()
        self.db.close()

    def test_add_to_watched_history(self):
        """
        Test adding a movie to the watched history.
        """
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_get_watched_history(self):
        """
        Test retrieving watched history.
        """
        # Add a movie to watched history
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )

        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)
        self.assertEqual(response.json[0]["movie_name"], "Star Wars (1977)")


if __name__ == "__main__":
    unittest.main()
