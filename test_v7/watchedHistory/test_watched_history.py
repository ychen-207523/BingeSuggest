"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
import sys
import unittest
import warnings
from pathlib import Path
import mysql.connector
import json
from dotenv import load_dotenv


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for actor based recommender system
    """

    def setUp(self):
        print("\nRunning Setup Method")
        load_dotenv()
        db = mysql.connector.connect(user="root", password="root", host="127.0.0.1")
        executor = db.cursor()
        executor.execute("USE testDB;")
        executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        executor.execute("DELETE FROM Users")
        executor.execute("DELETE FROM Ratings")
        executor.execute("DELETE FROM Friends")
        executor.execute("DELETE FROM Watchlist")
        db.commit()

    def test_get_empty_watched_history(self):
        """
        Test fetching watched history when it's empty.
        """
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_watched_history_with_entries(self):
        """
        Test fetching watched history when it has entries.
        """
        # Add a movie to watched history
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {
                    "imdb_id": "tt0076759",
                    "movie_name": "Star Wars: Episode IV - A New Hope",
                    "watched_date": "2024-11-16 14:44:31",
                }
            ),
            content_type="application/json",
        )

        # Fetch watched history
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)
        self.assertIn("movie_name", response.json[0])

    def test_add_movie_with_valid_data(self):
        """
        Test adding a movie with valid data to watched history.
        """
        data = {
            "imdb_id": "tt0076759",
            "movie_name": "Star Wars: Episode IV - A New Hope",
            "watched_date": "2024-11-16 14:44:31",
        }
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_add_movie_without_date(self):
        """
        Test adding a movie without providing a watched date.
        """
        data = {
            "imdb_id": "tt0076759",
            "movie_name": "Star Wars: Episode IV - A New Hope",
        }
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_add_movie_with_missing_fields(self):
        """
        Test adding a movie with missing fields.
        """
        data = {"imdb_id": "tt0076759"}
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("status", response.json)
        self.assertEqual(response.json["status"], "error")
