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

    def __init__(self, methodName: str = "runTest"):
        super().__init__(methodName)
        self.client = None

    def setUp(self):
        print("\nRunning Setup Method")
        load_dotenv()
        db = mysql.connector.connect(
            user="root", password="CHENyunfei@207523", host="127.0.0.1", port="3307"
        )
        executor = db.cursor()
        executor.execute("USE testDB;")
        executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        executor.execute("DELETE FROM Users")
        executor.execute("DELETE FROM Ratings")
        executor.execute("DELETE FROM Friends")
        executor.execute("DELETE FROM WatchedHistory")
        db.commit()

    def test_add_to_watched_history(self):
        """
        Test that a user can add a movie to their watched history.
        """
        load_dotenv()
        db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
        executor = db.cursor()
        executor.execute("USE testDB;")
        create_account(db, "placeholder@test.com", "newUser", "newPass")
        executor = db.cursor()
        executor.execute("SELECT * FROM Users;")
        db_result = executor.fetchall()
        user_id = db_result[0][0]
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
