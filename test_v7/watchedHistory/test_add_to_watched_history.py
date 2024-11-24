import sys
import unittest
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[2]))
from src.recommenderapp.utils import (
    create_account,
    add_to_watched_history,
)


class TestAddToWatchedHistory(unittest.TestCase):
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

    def test_add_movie_success(self):
        """Test successfully adding a movie to watched history."""
        create_account(self.db, "abc@test.com", "user1", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user1';")
        user_id = self.executor.fetchone()[0]
        self.assertTrue(add_to_watched_history(self.db, user_id, "tt0076759", None))

    def test_add_movie_already_exists(self):
        """Test adding a movie that already exists in watched history."""
        create_account(self.db, "abc@test.com", "user2", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user2';")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        self.assertFalse(add_to_watched_history(self.db, user_id, "tt0076759", None))

    def test_add_movie_not_in_database(self):
        """Test adding a movie that is not in the database."""
        create_account(self.db, "abc@test.com", "user3", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user3';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(add_to_watched_history(self.db, user_id, "tt9999999", None))

    def test_add_movie_no_date_provided(self):
        """Test adding a movie without providing a watched date."""
        create_account(self.db, "abc@test.com", "user4", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user4';")
        user_id = self.executor.fetchone()[0]
        self.assertTrue(add_to_watched_history(self.db, user_id, "tt0076759", None))

    def test_add_multiple_movies(self):
        """Test adding multiple movies to watched history."""
        create_account(self.db, "abc@test.com", "user5", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user5';")
        user_id = self.executor.fetchone()[0]
        self.assertTrue(add_to_watched_history(self.db, user_id, "tt0076759", None))
        self.assertTrue(add_to_watched_history(self.db, user_id, "tt0266543", None))

    def test_add_movie_invalid_user(self):
        """Test adding a movie with an invalid user ID."""
        self.assertFalse(add_to_watched_history(self.db, 999, "tt0076759", None))

    def test_add_movie_invalid_imdb_id(self):
        """Test adding a movie with an invalid IMDb ID."""
        create_account(self.db, "abc@test.com", "user6", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user6';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(add_to_watched_history(self.db, user_id, "invalid_id", None))

    def test_add_movie_with_future_date(self):
        """Test adding a movie with a future watched date."""
        create_account(self.db, "abc@test.com", "user7", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user7';")
        user_id = self.executor.fetchone()[0]
        self.assertTrue(
            add_to_watched_history(self.db, user_id, "tt0076759", "2025-11-23 10:00:00")
        )

    def test_add_movie_empty_imdb_id(self):
        """Test adding a movie with an empty IMDb ID."""
        create_account(self.db, "abc@test.com", "user8", "password123")
        self.executor.execute("SELECT idUsers FROM Users WHERE username = 'user8';")
        user_id = self.executor.fetchone()[0]
        self.assertFalse(add_to_watched_history(self.db, user_id, "", None))

    def test_add_movie_no_user_provided(self):
        """Test adding a movie without providing a user ID."""
        self.assertFalse(add_to_watched_history(self.db, None, "tt0076759", None))


if __name__ == "__main__":
    unittest.main()
