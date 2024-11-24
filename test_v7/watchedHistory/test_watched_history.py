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

    @classmethod
    def setUpClass(cls):
        """
        Set up the database and tables before any tests are run.
        """
        load_dotenv()
        cls.db = mysql.connector.connect(
            user="root", password="root", host="127.0.0.1", database="testDB"
        )
        cls.executor = cls.db.cursor()
        cls.reset_database()
        app.config["TESTING"] = True
        cls.client = app.test_client()

    @classmethod
    def reset_database(cls):
        """
        Resets the database by dropping and recreating necessary tables.
        """
        cls.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
        cls.executor.execute("DROP TABLE IF EXISTS WatchedHistory;")
        cls.executor.execute("DROP TABLE IF EXISTS Users;")
        cls.executor.execute("DROP TABLE IF EXISTS Movies;")
        cls.executor.execute("SET FOREIGN_KEY_CHECKS=1;")
        cls.executor.execute(
            """
            CREATE TABLE Users (
                idUsers INT NOT NULL AUTO_INCREMENT,
                username VARCHAR(45) NOT NULL,
                email VARCHAR(45) NOT NULL,
                password VARCHAR(64) NOT NULL,
                PRIMARY KEY (idUsers),
                UNIQUE INDEX username_UNIQUE (username ASC),
                UNIQUE INDEX email_UNIQUE (email ASC)
            );
            """
        )
        cls.executor.execute(
            """
            CREATE TABLE Movies (
                idMovies INT NOT NULL AUTO_INCREMENT,
                name VARCHAR(128) NOT NULL,
                imdb_id VARCHAR(45) NOT NULL,
                PRIMARY KEY (idMovies),
                UNIQUE INDEX imdb_id_UNIQUE (imdb_id ASC)
            );
            """
        )
        cls.executor.execute(
            """
            CREATE TABLE WatchedHistory (
                idWatchedHistory INT NOT NULL AUTO_INCREMENT,
                user_id INT NOT NULL,
                movie_id INT NOT NULL,
                watched_date DATETIME NOT NULL,
                PRIMARY KEY (idWatchedHistory),
                FOREIGN KEY (user_id) REFERENCES Users (idUsers) ON DELETE CASCADE,
                FOREIGN KEY (movie_id) REFERENCES Movies (idMovies) ON DELETE CASCADE
            );
            """
        )
        cls.db.commit()
        cls.executor.execute(
            """
            INSERT INTO Movies (idMovies, name, imdb_id) VALUES 
            (1, 'Star Wars (1977)', 'tt0076759'),
            (2, 'Finding Nemo (2003)', 'tt0266543');
            """
        )
        cls.db.commit()
    def setUp(self):
        """
        Clear data before each test.
        """
        self.executor.execute("DELETE FROM WatchedHistory;")
        self.executor.execute("DELETE FROM Users;")
        self.db.commit()

    def tearDown(self):
        """
        Close the database connection after each test.
        """
        if self.db.is_connected():
            self.db.close()

    @patch("src.recommenderapp.app.user", new=("user1", 1))
    def test_add_to_watched_history(self):
        """
        Test that a user can add a movie to their watched history.
        """
        create_account(self.db, "user1@test.com", "user1", "password123")
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

    @patch("src.recommenderapp.app.user", new=("user6", 6))
    def test_add_movie_not_in_database(self):
        """
        Test that a user cannot add a movie to their watched history if it is not in the database.
        """
        create_account(self.db, "user6@test.com", "user6", "password123")
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt9999999", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")

    @patch("src.recommenderapp.app.user", new=("user7", 7))
    def test_add_multiple_movies(self):
        """
        Test adding multiple movies to watched history.
        """
        create_account(self.db, "user7@test.com", "user7", "password123")
        movie_ids = ["tt0076759", "tt0266543"]
        for imdb_id in movie_ids:
            response = self.client.post(
                "/add_to_watched_history",
                data=json.dumps(
                    {"imdb_id": imdb_id, "watched_date": "2024-11-23 10:00:00"}
                ),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user8", 8))
    def test_remove_nonexistent_movie(self):
        """
        Test that a user cannot remove a movie from their watched history if it is not
        """
        create_account(self.db, "user8@test.com", "user8", "password123")
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({"imdb_id": "tt9999999"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")

    @patch("src.recommenderapp.app.user", new=("user9", 9))
    def test_watched_history_sorting(self):
        """
        Test that watched history is sorted by watched date
        """
        create_account(self.db, "user9@test.com", "user9", "password123")
        movies = [
            {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"},
            {"imdb_id": "tt0266543", "watched_date": "2024-11-23 11:00:00"},
        ]
        for movie in movies:
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps(movie),
                content_type="application/json",
            )
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)
        self.assertEqual(response.json[0]["movie_name"], "Finding Nemo (2003)")

    @patch("src.recommenderapp.app.user", new=("user10", 10))
    def test_remove_all_movies(self):
        """
        Test removing all movies from watched history.
        """
        create_account(self.db, "user10@test.com", "user10", "password123")
        movie_ids = ["tt0076759", "tt0266543"]
        for imdb_id in movie_ids:
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps(
                    {"imdb_id": imdb_id, "watched_date": "2024-11-23 10:00:00"}
                ),
                content_type="application/json",
            )
        for imdb_id in movie_ids:
            response = self.client.post(
                "/removeFromWatchedHistory",
                data=json.dumps({"imdb_id": imdb_id}),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["status"], "success")
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(len(response.json), 0)

    @patch("src.recommenderapp.app.user", new=("user11", 11))
    def test_add_movie_without_date(self):
        """
        Test adding a movie to watched history without specifying a watched date.
        """
        create_account(self.db, "user11@test.com", "user11", "password123")
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user12", 12))
    def test_add_movie_case_insensitive(self):
        """
        Test that the IMDb ID is case-insensitive when adding a movie to watched history.
        """
        create_account(self.db, "user12@test.com", "user12", "password123")
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "TT0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user13", 13))
    def test_duplicate_user_movie_pair(self):
        """
        Test that a user cannot add the same movie to their watched history more than once.
        """
        create_account(self.db, "user13@test.com", "user13", "password123")
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

    @patch("src.recommenderapp.app.user", new=("user14", 14))
    def test_get_history_no_movies(self):
        """
        Test that a user can get their watched history even if they have not added any movies.
        """
        create_account(self.db, "user14@test.com", "user14", "password123")
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 0)

    @patch("src.recommenderapp.app.user", new=("user15", 15))
    def test_remove_movie_not_in_history(self):
        """
        Test that a user cannot remove a movie from their watched history if it is not
        """
        create_account(self.db, "user15@test.com", "user15", "password123")
        response = self.client.post(
            "/removeFromWatchedHistory",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")

    @patch("src.recommenderapp.app.user", new=("user16", 16))
    def test_add_invalid_movie(self):
        """
        Test that a user cannot add an invalid movie to their watched history
        """
        create_account(self.db, "user16@test.com", "user16", "password123")
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "invalid", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json["status"], "error")

    @patch("src.recommenderapp.app.user", new=("user17", 17))
    def test_multiple_users_same_movie(self):
        """
        Test that multiple users can add the same movie to their watched history.
        """
        create_account(self.db, "user17@test.com", "user17", "password123")
        create_account(self.db, "user18@test.com", "user18", "password123")
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        with patch("src.recommenderapp.app.user", new=("user18", 18)):
            response = self.client.post(
                "/add_to_watched_history",
                data=json.dumps(
                    {"imdb_id": "tt0076759", "watched_date": "2024-11-23 11:00:00"}
                ),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user18", 18))
    def test_remove_movie_from_another_user_history(self):
        """
        Test that a user cannot remove a movie from another user's watched history.
        """
        create_account(self.db, "user18@test.com", "user18", "password123")
        create_account(self.db, "user19@test.com", "user19", "password123")

        # User18 adds a movie
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        # User19 tries to remove User18's movie
        with patch("src.recommenderapp.app.user", new=("user19", 19)):
            response = self.client.post(
                "/removeFromWatchedHistory",
                data=json.dumps({"imdb_id": "tt0076759"}),
                content_type="application/json",
            )
            self.assertEqual(response.status_code, 404)
            self.assertEqual(response.json["status"], "error")

    @patch("src.recommenderapp.app.user", new=("user19", 19))
    def test_add_movie_with_minimal_data(self):
        """
        Test adding a movie with only the IMDb ID, no additional data.
        """
        create_account(self.db, "user19@test.com", "user19", "password123")
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0266543"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["status"], "success")

    @patch("src.recommenderapp.app.user", new=("user20", 20))
    def test_get_watched_history_multiple_users(self):
        """
        Test retrieving watched history for multiple users independently.
        """
        create_account(self.db, "user20@test.com", "user20", "password123")
        create_account(self.db, "user21@test.com", "user21", "password123")

        # User20 adds a movie
        self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )

        # User21 adds a different movie
        with patch("src.recommenderapp.app.user", new=("user21", 21)):
            self.client.post(
                "/add_to_watched_history",
                data=json.dumps(
                    {"imdb_id": "tt0266543", "watched_date": "2024-11-23 11:00:00"}
                ),
                content_type="application/json",
            )

        # Validate User20's watched history
        response_user20 = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response_user20.status_code, 200)
        self.assertEqual(len(response_user20.json), 1)
        self.assertEqual(response_user20.json[0]["movie_name"], "Star Wars (1977)")

        # Validate User21's watched history
        with patch("src.recommenderapp.app.user", new=("user21", 21)):
            response_user21 = self.client.get("/getWatchedHistoryData")
            self.assertEqual(response_user21.status_code, 200)
            self.assertEqual(len(response_user21.json), 1)
            self.assertEqual(
                response_user21.json[0]["movie_name"], "Finding Nemo (2003)"
            )
