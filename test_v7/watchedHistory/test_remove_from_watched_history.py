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
        print("\nRunning setup method")
        load_dotenv()
        self.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1"
        )
        self.executor = self.db.cursor()
        self.executor.execute("USE testDB;")
        self.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        self.executor.execute("DELETE FROM Users")
        self.executor.execute("DELETE FROM WatchedHistory")
        self.executor.execute("DELETE FROM Movies")
        self.executor.execute(
            """
            INSERT INTO Movies (idMovies, name, imdb_id) VALUES 
            (11, 'Star Wars (1977)', 'tt0076759'),
            (12, 'Finding Nemo (2003)', 'tt0266543');
            """
        )
        self.db.commit()

    def test_remove_existing_movie(self):
        """Test removing a movie from watched history."""
        create_account(self.db, "abc@test.com", "user1", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user1';")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        self.assertTrue(remove_from_watched_history_util(self.db, user_id, "tt0076759"))

    def test_remove_nonexistent_movie(self):
        """Test removing a movie that is not in watched history."""
        create_account(self.db, "abc@test.com", "user2", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user2';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(
            remove_from_watched_history_util(self.db, user_id, "tt0076759")
        )

    def test_remove_movie_not_in_database(self):
        """Test removing a movie that is not in the database."""
        create_account(self.db, "abc@test.com", "user3", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user3';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(
            remove_from_watched_history_util(self.db, user_id, "tt9999999")
        )

    def test_remove_movie_invalid_user(self):
        """Test removing a movie with an invalid user ID."""
        self.assertFalse(remove_from_watched_history_util(self.db, 999, "tt0076759"))

    def test_remove_movie_empty_imdb_id(self):
        """Test removing a movie with an empty IMDb ID."""
        create_account(self.db, "abc@test.com", "user4", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user4';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(remove_from_watched_history_util(self.db, user_id, ""))

    def test_remove_multiple_movies(self):
        """Test removing multiple movies."""
        create_account(self.db, "abc@test.com", "user5", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user5';")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        add_to_watched_history(self.db, user_id, "tt0266543", None)
        self.assertTrue(remove_from_watched_history_util(self.db, user_id, "tt0076759"))
        self.assertTrue(remove_from_watched_history_util(self.db, user_id, "tt0266543"))

    def test_remove_movie_invalid_imdb_id(self):
        """Test removing a movie with an invalid IMDb ID."""
        create_account(self.db, "abc@test.com", "user6", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user6';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(
            remove_from_watched_history_util(self.db, user_id, "invalid_id")
        )

    def test_remove_movie_no_user_provided(self):
        """Test removing a movie without providing a user ID."""
        self.assertFalse(remove_from_watched_history_util(self.db, None, "tt0076759"))

    def test_remove_movie_not_in_watched_history(self):
        """Test removing a movie not in watched history."""
        create_account(self.db, "abc@test.com", "user7", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user7';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(
            remove_from_watched_history_util(self.db, user_id, "tt0266543")
        )

    def test_remove_movie_with_future_date(self):
        """Test removing a movie with a future watched date."""
        create_account(self.db, "abc@test.com", "user8", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user8';")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", "2025-11-23 10:00:00")
        self.assertTrue(remove_from_watched_history_util(self.db, user_id, "tt0076759"))


if __name__ == "__main__":
    unittest.main()
