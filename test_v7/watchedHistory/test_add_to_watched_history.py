import sys
import unittest
import warnings
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv

sys.path.append(str(Path(__file__).resolve().parents[2]))
# pylint: disable=wrong-import-position
from src.recommenderapp.utils import add_to_watched_history, create_account

# pylint: enable=wrong-import-position
warnings.filterwarnings("ignore")


class TestAddToWatchedHistory(unittest.TestCase):
    """
    Test cases for adding movies to watched history.
    """

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
        self.executor.execute("DELETE FROM Movies;")
        self.executor.execute("SET FOREIGN_KEY_CHECKS=1;")
        self.db.commit()

        # Populate Movies table
        self.executor.execute(
            """
            INSERT INTO Movies (idMovies, name, imdb_id) VALUES
            (1, 'Star Wars (1977)', 'tt0076759'),
            (2, 'Finding Nemo (2003)', 'tt0266543');
            """
        )
        self.db.commit()

    def test_add_movie_success(self):
        """
        Test adding a movie successfully.
        """
        create_account(self.db, "user1@test.com", "user1", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = add_to_watched_history(self.db, user_id, "tt0076759", None)
        self.assertEqual(result, (True, "Movie added to watched history"))

    def test_add_movie_already_exists(self):
        """
        Test adding a movie that already exists in watched history.
        """
        create_account(self.db, "user2@test.com", "user2", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        add_to_watched_history(self.db, user_id, "tt0076759", None)
        result = add_to_watched_history(self.db, user_id, "tt0076759", None)
        self.assertEqual(result, (False, "Movie already in watched history"))

    def test_add_movie_not_in_database(self):
        """
        Test adding a movie that is not in the database.
        """
        create_account(self.db, "user3@test.com", "user3", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = add_to_watched_history(self.db, user_id, "tt9999999", None)
        self.assertEqual(result, (False, "Movie not found"))

    def test_add_movie_invalid_user(self):
        """
        Test adding a movie with an invalid user ID.
        """
        result = add_to_watched_history(self.db, 999, "tt0076759", None)
        self.assertEqual(result, (False, "User not found"))

    def test_add_movie_empty_imdb_id(self):
        """
        Test adding a movie with an empty IMDb ID.
        """
        create_account(self.db, "user4@test.com", "user4", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = add_to_watched_history(self.db, user_id, "", None)
        self.assertEqual(result, (False, "Movie not found"))

    def test_add_movie_no_user_provided(self):
        """
        Test adding a movie without providing a user ID.
        """
        result = add_to_watched_history(self.db, None, "tt0076759", None)
        self.assertEqual(result, (False, "User not found"))

    def test_add_movie_invalid_imdb_id(self):
        """
        Test adding a movie with an invalid IMDb ID.
        """
        create_account(self.db, "user5@test.com", "user5", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = add_to_watched_history(self.db, user_id, "invalid_id", None)
        self.assertEqual(result, (False, "Movie not found"))

    def test_add_movie_with_timestamp(self):
        """
        Test adding a movie with a provided timestamp.
        """
        create_account(self.db, "user6@test.com", "user6", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = add_to_watched_history(
            self.db, user_id, "tt0076759", "2024-11-23 10:00:00"
        )
        self.assertEqual(result, (True, "Movie added to watched history"))

    def test_add_movie_no_timestamp(self):
        """
        Test adding a movie without a timestamp.
        """
        create_account(self.db, "user7@test.com", "user7", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        result = add_to_watched_history(self.db, user_id, "tt0076759", None)
        self.assertEqual(result, (True, "Movie added to watched history"))

    def test_add_multiple_movies(self):
        """
        Test adding multiple movies to watched history.
        """
        create_account(self.db, "user8@test.com", "user8", "password123")
        self.executor.execute("SELECT idUsers FROM Users;")
        user_id = self.executor.fetchone()[0]
        movie_ids = ["tt0076759", "tt0266543"]
        for imdb_id in movie_ids:
            result = add_to_watched_history(self.db, user_id, imdb_id, None)
            self.assertEqual(result, (True, "Movie added to watched history"))


if __name__ == "__main__":
    unittest.main()
