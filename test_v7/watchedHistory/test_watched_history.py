"""
Copyright (c) 2023 Aditya Pai, Ananya Mantravadi, Rishi Singhal, Samarth Shetty
This code is licensed under MIT license (see LICENSE for details)

@author: PopcornPicks
"""
import unittest
import mysql.connector
import json
from dotenv import load_dotenv
from app import app


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for watched history functionality
    """

    def setUp(self):
        """
        Setup method to prepare the test database and Flask test client.
        """
        print("\nRunning Setup Method")
        load_dotenv()
        self.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1"
        )
        self.executor = self.db.cursor()
        self.executor.execute("USE testDB;")
        self.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.executor.execute("DELETE FROM WatchedHistory")
        self.executor.execute("DELETE FROM Users")
        self.executor.execute("DELETE FROM Movies")
        self.db.commit()

        # Set up Flask test client
        app.config["TESTING"] = True
        self.client = app.test_client()

    def tearDown(self):
        """
        Cleanup method after each test.
        """
        self.db.close()

    def test_get_empty_watched_history(self):
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_get_watched_history_with_entries(self):
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
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertGreater(len(response.json), 0)

    def test_add_movie_with_valid_data(self):
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
        data = {"imdb_id": "tt0076759"}
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_add_multiple_movies_for_single_user(self):
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
        ]
        for movie in movies:
            response = self.client.post(
                "/add_to_watched_history",
                data=json.dumps(movie),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), len(movies))

    def test_add_duplicate_movies(self):
        movie = {
            "imdb_id": "tt0076759",
            "movie_name": "Star Wars: Episode IV - A New Hope",
            "watched_date": "2024-11-16 14:00:00",
        }
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(movie),
            content_type="application/json",
        )
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(movie),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_existing_movie(self):
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

    def test_delete_nonexistent_movie(self):
        data = {"imdb_id": "nonexistent_id"}
        response = self.client.post(
            "/delete_from_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_prevent_duplicate_entries(self):
        data = {
            "imdb_id": "tt0076759",
            "movie_name": "Star Wars: Episode IV - A New Hope",
            "watched_date": "2024-11-16 14:44:31",
        }
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "info")

    def test_watched_history_format(self):
        response = self.client.get("/getWatchedHistoryData")
        if response.json:
            for movie in response.json:
                self.assertIn("movie_name", movie)
                self.assertIn("imdb_id", movie)
                self.assertIn("watched_date", movie)

    def test_invalid_add_request(self):
        response = self.client.post(
            "/add_to_watched_history",
            data="Invalid Data",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_delete_request(self):
        response = self.client.post(
            "/delete_from_watched_history",
            data="Invalid Data",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_watched_history_limit(self):
        for i in range(15):
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps({"imdb_id": f"tt00{i}", "movie_name": f"Movie {i}"}),
                content_type="application/json",
            )
        response = self.client.get("/getWatchedHistoryData?limit=10")
        self.assertEqual(len(response.json), 10)

    def test_delete_all_entries(self):
        for i in range(5):
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps({"imdb_id": f"tt00{i}", "movie_name": f"Movie {i}"}),
                content_type="application/json",
            )
        response = self.client.post(
            "/delete_all_watched_history", content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.json, [])

    def test_empty_after_deletion(self):
        self.client.post("/delete_all_watched_history", content_type="application/json")
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])

    def test_add_movie_without_imdb_id(self):
        data = {"movie_name": "Some Movie"}
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_add_movie_without_movie_name(self):
        data = {"imdb_id": "tt0076759"}
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_invalid_limit_on_fetch(self):
        """
        Test fetching watched history with an invalid limit parameter.
        """
        response = self.client.get("/getWatchedHistoryData?limit=invalid")
        self.assertEqual(response.status_code, 400)
        self.assertIn("Invalid limit", response.json["message"])

    def test_sorted_watched_history(self):
        """
        Test fetching watched history sorted by watched date.
        """
        movies = [
            {
                "imdb_id": "tt0076759",
                "movie_name": "Movie A",
                "watched_date": "2024-11-15 10:00:00",
            },
            {
                "imdb_id": "tt0080684",
                "movie_name": "Movie B",
                "watched_date": "2024-11-16 10:00:00",
            },
        ]
        for movie in movies:
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps(movie),
                content_type="application/json",
            )
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [movie["movie_name"] for movie in response.json],
            ["Movie A", "Movie B"],
        )


if __name__ == "__main__":
    unittest.main()
