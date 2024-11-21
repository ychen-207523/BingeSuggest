"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
import unittest
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

    def test_add_multiple_movies_for_single_user(self):
        """
        Test adding multiple movies to watched history for a single user.
        """
        movies = [
            {
                "imdb_id": "tt0076759",
                "movie_name": "Star Wars: Episode IV - A New Hope",
                "watched_date": "2024-11-16 14:00:00",
            },
            {
                "imdb_id": "tt0080684",
                "movie_name": "Star Wars: Episode V - The Empire Strikes Back",
                "watched_date": "2024-11-17 15:00:00",
            },
            {
                "imdb_id": "tt0086190",
                "movie_name": "Star Wars: Episode VI - Return of the Jedi",
                "watched_date": "2024-11-18 16:00:00",
            },
        ]

        for movie in movies:
            response = self.client.post(
                "/add_to_watched_history",
                data=json.dumps(movie),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["status"], "success")

        # Fetch all movies for the user
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(movies))
        for movie in movies:
            self.assertIn(movie["movie_name"], [m["movie_name"] for m in response.json])

    def test_add_multiple_movies_for_different_users(self):
        """
        Test adding movies to watched history for different users.
        """
        movies_user_1 = [
            {
                "user_id": 1,
                "imdb_id": "tt0076759",
                "movie_name": "Star Wars: Episode IV - A New Hope",
                "watched_date": "2024-11-16 14:00:00",
            },
            {
                "user_id": 1,
                "imdb_id": "tt0080684",
                "movie_name": "Star Wars: Episode V - The Empire Strikes Back",
                "watched_date": "2024-11-17 15:00:00",
            },
        ]
        movies_user_2 = [
            {
                "user_id": 2,
                "imdb_id": "tt0086190",
                "movie_name": "Star Wars: Episode VI - Return of the Jedi",
                "watched_date": "2024-11-18 16:00:00",
            },
        ]

        # Add movies for User 1
        for movie in movies_user_1:
            response = self.client.post(
                "/add_to_watched_history",
                data=json.dumps(movie),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["status"], "success")

        # Add movies for User 2
        for movie in movies_user_2:
            response = self.client.post(
                "/add_to_watched_history",
                data=json.dumps(movie),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["status"], "success")

        # Verify movies for User 1
        response = self.client.get("/getWatchedHistoryData?user_id=1")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(movies_user_1))

        # Verify movies for User 2
        response = self.client.get("/getWatchedHistoryData?user_id=2")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(movies_user_2))

    def test_add_duplicate_movies(self):
        """
        Test that duplicate movies cannot be added to the watched history.
        """
        movie = {
            "imdb_id": "tt0076759",
            "movie_name": "Star Wars: Episode IV - A New Hope",
            "watched_date": "2024-11-16 14:00:00",
        }

        # Add the movie once
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(movie),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

        # Attempt to add the same movie again
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(movie),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json["status"], "error")
        self.assertIn("already exists", response.json["message"])

    def test_delete_existing_movie(self):
        """
        Test deleting an existing movie from watched history.
        """
        data = {"imdb_id": "tt0076759"}
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        response = self.client.post(
            "/delete_from_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    def test_delete_nonexistent_movie(self):
        """
        Test deleting a nonexistent movie from watched history.
        """
        data = {"imdb_id": "nonexistent_id"}
        response = self.client.post(
            "/delete_from_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")
