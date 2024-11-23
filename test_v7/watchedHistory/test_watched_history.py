import sys
import unittest
from pathlib import Path
import warnings
import json
from flask import g
from dotenv import load_dotenv
from src.recommenderapp.app import app

sys.path.append(str(Path(__file__).resolve().parents[2]))

warnings.filterwarnings("ignore")


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for watched history management using Flask test client.
    """

    def setUp(self):
        load_dotenv()
        self.client = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        g.db = self._get_test_db()
        executor = g.db.cursor()
        executor.execute("USE testDB;")
        executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        executor.execute("DELETE FROM WatchedHistory")
        executor.execute("DELETE FROM Users")
        executor.execute("DELETE FROM Movies")
        g.db.commit()

    def _get_test_db(self):
        import mysql.connector
        return mysql.connector.connect(
            user="root", password="root", host="127.0.0.1"
        )

    def tearDown(self):
        g.db.close()
        self.app_context.pop()

    def create_test_user(self, email="test@example.com"):
        cursor = g.db.cursor()
        cursor.execute(
            "INSERT INTO Users (email, username, password) VALUES (%s, %s, %s);",
            (email, "testuser", "password"),
        )
        g.db.commit()
        cursor.execute("SELECT LAST_INSERT_ID();")
        return cursor.fetchone()[0]

    def test_add_movie_valid_data(self):
        """
        Test adding a movie to the watched history
        """
        self.create_test_user()
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({
                "movieName": "Star Wars (1977)",
                "imdb_id": "tt0076759",
                "watched_date": "2024-11-16 14:44:31",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json()["status"])

    def test_add_movie_without_date(self):
        """
        Test adding a movie to the watched history without a date
        """
        self.create_test_user()
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({
                "movieName": "Star Wars (1977)",
                "imdb_id": "tt0076759",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json()["status"])

    def test_get_empty_watched_history(self):
        """
        Test getting the watched history for a user with no movies watched
        """
        self.create_test_user()
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), [])

    def test_add_duplicate_movie(self):
        """
        Test adding a movie to the watched history that is already present
        """
        self.create_test_user()
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({
                "movieName": "Star Wars (1977)",
                "imdb_id": "tt0076759",
            }),
            content_type="application/json",
        )
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({
                "movieName": "Star Wars (1977)",
                "imdb_id": "tt0076759",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("info", response.get_json()["status"])

    def test_remove_movie_from_watched_history(self):
        """
        Test removing a movie from the user's watched history
        """
        self.create_test_user()
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({
                "movieName": "Star Wars (1977)",
                "imdb_id": "tt0076759",
            }),
            content_type="application/json",
        )
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({
                "imdb_id": "tt0076759",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("success", response.get_json()["status"])

    def test_remove_nonexistent_movie(self):
        """
        Test removing a movie that is not in the user's watched history
        """
        self.create_test_user()
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({
                "imdb_id": "tt0000000",
            }),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.get_json()["status"])

    def test_get_watched_history_with_entries(self):
        """
        Test getting the watched history for a user with movies
        """
        self.create_test_user()
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps({
                "movieName": "Star Wars (1977)",
                "imdb_id": "tt0076759",
                "watched_date": "2024-11-16 14:44:31",
            }),
            content_type="application/json",
        )
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.get_json()), 1)

if __name__ == "__main__":
    unittest.main()
