import sys
import unittest
import warnings
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.recommenderapp.app import (
    add_movie_to_watched_history,
    remove_from_watched_history,
    get_watched_history,
)

warnings.filterwarnings("ignore")


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for watched history management.
    """

    def setUp(self):
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

    def tearDown(self):
        self.db.close()

    def create_test_user(self, email="test@example.com"):
        self.executor.execute(
            "INSERT INTO Users (email, username, password) VALUES (%s, %s, %s);",
            (email, "testuser", "password"),
        )
        self.db.commit()
        self.executor.execute("SELECT LAST_INSERT_ID();")
        return self.executor.fetchone()[0]

    def create_test_movie(self, imdb_id, name="Some Movie"):
        self.executor.execute(
            "INSERT INTO Movies (imdb_id, name) VALUES (%s, %s);", (imdb_id, name)
        )
        self.db.commit()
        self.executor.execute("SELECT LAST_INSERT_ID();")
        return self.executor.fetchone()[0]

    def test_add_movie_valid_data(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        result = add_movie_to_watched_history(
            self.db,
            user_id,
            "tt0076759",
            "Star Wars: A New Hope",
            "2024-11-16 14:44:31",
        )
        self.assertTrue(result)

    def test_add_movie_without_date(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        result = add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars: A New Hope"
        )
        self.assertTrue(result)

    def test_get_empty_watched_history(self):
        user_id = self.create_test_user()
        result = get_watched_history(self.db, user_id)
        self.assertEqual(result, [])

    def test_add_duplicate_movie(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars: A New Hope"
        )
        result = add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars: A New Hope"
        )
        self.assertFalse(result)

    def test_remove_movie_from_watched_history(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars: A New Hope"
        )
        result = remove_from_watched_history(self.db, user_id, "tt0076759")
        self.assertTrue(result)

    def test_remove_nonexistent_movie(self):
        user_id = self.create_test_user()
        result = remove_from_watched_history(self.db, user_id, "tt0000000")
        self.assertFalse(result)

    def test_get_watched_history_with_entries(self):
        user_id = self.create_test_user()
        self.create_test_movie("tt0076759", "Star Wars")
        add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars", "2024-11-16 14:44:31"
        )
        watched_history = get_watched_history(self.db, user_id)
        self.assertEqual(len(watched_history), 1)

    def test_add_movie_invalid_imdb_id(self):
        user_id = self.create_test_user()
        result = add_movie_to_watched_history(self.db, user_id, "", "Invalid Movie")
        self.assertFalse(result)

    def test_add_movie_invalid_user(self):
        movie_id = self.create_test_movie("tt0076759")
        result = add_movie_to_watched_history(self.db, -1, "tt0076759", "Star Wars")
        self.assertFalse(result)

    def test_remove_movie_invalid_imdb_id(self):
        user_id = self.create_test_user()
        result = remove_from_watched_history(self.db, user_id, "")
        self.assertFalse(result)

    def test_add_multiple_movies(self):
        user_id = self.create_test_user()
        self.create_test_movie("tt0076759", "Star Wars")
        self.create_test_movie("tt0080684", "The Empire Strikes Back")
        add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars", "2024-11-16 14:00:00"
        )
        add_movie_to_watched_history(
            self.db,
            user_id,
            "tt0080684",
            "The Empire Strikes Back",
            "2024-11-17 14:00:00",
        )
        watched_history = get_watched_history(self.db, user_id)
        self.assertEqual(len(watched_history), 2)

    def test_fetch_limited_entries(self):
        user_id = self.create_test_user()
        for i in range(5):
            self.create_test_movie(f"tt007675{i}", f"Movie {i}")
            add_movie_to_watched_history(self.db, user_id, f"tt007675{i}", f"Movie {i}")
        watched_history = get_watched_history(self.db, user_id, limit=3)
        self.assertEqual(len(watched_history), 3)

    def test_add_movie_after_removal(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        add_movie_to_watched_history(self.db, user_id, "tt0076759", "Star Wars")
        remove_from_watched_history(self.db, user_id, "tt0076759")
        result = add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars"
        )
        self.assertTrue(result)

    def test_get_watched_history_format(self):
        user_id = self.create_test_user()
        self.create_test_movie("tt0076759", "Star Wars")
        add_movie_to_watched_history(self.db, user_id, "tt0076759", "Star Wars")
        watched_history = get_watched_history(self.db, user_id)
        self.assertIn("movie_name", watched_history[0])
        self.assertIn("imdb_id", watched_history[0])
        self.assertIn("watched_date", watched_history[0])

    def test_remove_movie_not_in_history(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        result = remove_from_watched_history(self.db, user_id, "tt0076759")
        self.assertFalse(result)

    def test_add_movie_with_future_date(self):
        user_id = self.create_test_user()
        self.create_test_movie("tt0076759", "Star Wars")
        result = add_movie_to_watched_history(
            self.db, user_id, "tt0076759", "Star Wars", "2025-01-01 00:00:00"
        )
        self.assertFalse(result)

    def test_add_movie_without_movie_name(self):
        user_id = self.create_test_user()
        movie_id = self.create_test_movie("tt0076759")
        result = add_movie_to_watched_history(self.db, user_id, "tt0076759", None)
        self.assertFalse(result)

    def test_remove_movie_different_user(self):
        user_id_1 = self.create_test_user("user1@example.com")
        user_id_2 = self.create_test_user("user2@example.com")
        self.create_test_movie("tt0076759", "Star Wars")
        add_movie_to_watched_history(self.db, user_id_1, "tt0076759", "Star Wars")
        result = remove_from_watched_history(self.db, user_id_2, "tt0076759")
        self.assertFalse(result)

    def test_get_history_after_deleting_some_movies(self):
        user_id = self.create_test_user()
        self.create_test_movie("tt0076759", "Star Wars")
        self.create_test_movie("tt0080684", "The Empire Strikes Back")
        add_movie_to_watched_history(self.db, user_id, "tt0076759", "Star Wars")
        add_movie_to_watched_history(self.db, "tt0080684", "The Empire Strikes Back")
        remove_from_watched_history(self.db, user_id, "tt0076759")
        watched_history = get_watched_history(self.db, user_id)
        self.assertEqual(len(watched_history), 1)

    def test_add_multiple_movies_for_different_users(self):
        user_id_1 = self.create_test_user("user1@example.com")
        user_id_2 = self.create_test_user("user2@example.com")
        self.create_test_movie("tt0076759", "Star Wars")
        self.create_test_movie("tt0080684", "The Empire Strikes Back")
        add_movie_to_watched_history(self.db, user_id_1, "tt0076759", "Star Wars")
        add_movie_to_watched_history(
            self.db, user_id_2, "tt0080684", "The Empire Strikes Back"
        )
        history_user_1 = get_watched_history(self.db, user_id_1)
        history_user_2 = get_watched_history(self.db, user_id_2)
        self.assertEqual(len(history_user_1), 1)
        self.assertEqual(len(history_user_2), 1)


if __name__ == "__main__":
    unittest.main()
