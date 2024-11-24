import sys
import unittest
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.recommenderapp.utils import (
    create_account,
    add_to_watched_history,
    remove_from_watched_history_util,
)


class TestRemoveFromWatchedHistory(unittest.TestCase):
    def setUp(self):
        """
        Set up test database before each test.
        """
        print("\nrunning setup method")
        load_dotenv()
        self.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1"
        )
        self.executor = self.db.cursor()
        self.executor.execute("USE testDB;")
        self.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.executor.execute("DELETE FROM Users;")
        self.executor.execute("DELETE FROM WatchedHistory;")
        self.db.commit()

    def test_remove_movie_success(self):
        """
        Test removing a movie successfully from watched history.
        """
        create_account(self.db, "user1@test.com", "user1", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        result = remove_from_watched_history_util(self.db, user_id, "tt0076759")
        self.assertEqual(result, (True, "Movie removed from watched history"))

    def test_remove_nonexistent_movie(self):
        """
        Test removing a movie that is not in watched history.
        """
        create_account(self.db, "user2@test.com", "user2", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = remove_from_watched_history_util(self.db, user_id, "tt0266543")
        self.assertEqual(result, (False, "Movie not in watched history"))

    def test_remove_movie_not_in_database(self):
        """
        Test removing a movie that does not exist in the database.
        """
        create_account(self.db, "user3@test.com", "user3", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = remove_from_watched_history_util(self.db, user_id, "tt0000000")
        self.assertEqual(result, (False, "Movie not found"))

    def test_remove_movie_invalid_user(self):
        """
        Test removing a movie with an invalid user ID.
        """
        create_account(self.db, "user4@test.com", "user4", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        result = remove_from_watched_history_util(self.db, 999, "tt0076759")
        self.assertEqual(result, (False, "Movie not in watched history"))

    def test_remove_movie_no_user_provided(self):
        """
        Test removing a movie without providing a user ID.
        """
        create_account(self.db, "user5@test.com", "user5", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        result = remove_from_watched_history_util(self.db, None, "tt0076759")
        self.assertEqual(result, (False, "Movie not in watched history"))

    def test_remove_movie_empty_imdb_id(self):
        """
        Test removing a movie with an empty IMDb ID.
        """
        create_account(self.db, "user6@test.com", "user6", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = remove_from_watched_history_util(self.db, user_id, "")
        self.assertEqual(result, (False, "Movie not found"))

    def test_remove_movie_invalid_imdb_id(self):
        """
        Test removing a movie with an invalid IMDb ID.
        """
        create_account(self.db, "user7@test.com", "user7", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = remove_from_watched_history_util(self.db, user_id, "invalid_id")
        self.assertEqual(result, (False, "Movie not found"))

    def test_remove_movie_from_different_user(self):
        """
        Test removing a movie added by a different user.
        """
        create_account(self.db, "user8@test.com", "user8", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user1_id = self.executor.fetchone()[0]
        create_account(self.db, "user9@test.com", "user9", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user2_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user1_id, "tt0076759", None)
        result = remove_from_watched_history_util(self.db, user2_id, "tt0076759")
        self.assertEqual(result, (False, "Movie not in watched history"))

    def test_remove_movie_no_timestamp(self):
        """
        Test removing a movie without a timestamp provided.
        """
        create_account(self.db, "user10@test.com", "user10", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0168629", None)
        result = remove_from_watched_history_util(self.db, user_id, "tt0168629")
        self.assertEqual(result, (True, "Movie removed from watched history"))

    def test_remove_movie_with_multiple_movies(self):
        """
        Test removing a movie when the user has multiple movies in watched history.
        """
        create_account(self.db, "user11@test.com", "user11", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        add_to_watched_history(self.db, user_id, "tt0266543", None)
        result = remove_from_watched_history_util(self.db, user_id, "tt0076759")
        self.assertEqual(result, (True, "Movie removed from watched history"))


if __name__ == "__main__":
    unittest.main()
