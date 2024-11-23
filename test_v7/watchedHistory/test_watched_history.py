import sys
import unittest
import warnings
from pathlib import Path
import mysql.connector
from dotenv import load_dotenv
import json

sys.path.append(str(Path(__file__).resolve().parents[2]))

# pylint: disable=wrong-import-position
from src.recommenderapp.utils import create_account
from src.recommenderapp.app import app

# pylint: enable=wrong-import-position

warnings.filterwarnings("ignore")


class TestWatchedHistory(unittest.TestCase):
    """
    Test cases for WatchedHistory functionality.
    """

    def setUp(self):
        """
        Set up the database and create a fresh user for each test.
        """
        print("\nRunning Setup Method for a Test")
        load_dotenv()

        sql_file_path = Path(__file__).resolve().parents[2] / "test_initial.sql"

        try:
            self.db = mysql.connector.connect(
                user="root", password="root", host="127.0.0.1"
            )
            self.executor = self.db.cursor()
        except mysql.connector.Error as err:
            self.fail(f"Error connecting to MySQL: {err}")

        try:
            with open(sql_file_path, "r") as f:
                sql_commands = f.read()

            for result in self.executor.execute(sql_commands, multi=True):
                pass  # Execute all statements

            self.db.commit()
            print("Database setup completed successfully.")
        except FileNotFoundError:
            self.fail(f"SQL file not found at path: {sql_file_path}")
        except mysql.connector.Error as err:
            self.fail(f"Error executing SQL script: {err}")

        try:
            self.db.close()
            self.db = mysql.connector.connect(
                user="root", password="root", host="127.0.0.1", database="testDB"
            )
            self.executor = self.db.cursor()
        except mysql.connector.Error as err:
            self.fail(f"Error connecting to testDB: {err}")

        try:
            self.executor.execute("SET FOREIGN_KEY_CHECKS=0;")
            self.executor.execute("DELETE FROM WatchedHistory;")
            self.executor.execute("DELETE FROM Watchlist;")
            self.executor.execute("DELETE FROM Ratings;")
            self.executor.execute("DELETE FROM Friends;")
            self.executor.execute("DELETE FROM Users;")
            self.db.commit()
            self.executor.execute("SET FOREIGN_KEY_CHECKS=1;")
            self.db.commit()
            print("Tables reset successfully.")
        except mysql.connector.Error as err:
            self.fail(f"Error resetting tables: {err}")

        self.test_email = "testuser@test.com"
        self.test_username = "testuser"
        self.test_password = "password123"
        try:
            create_account(
                self.db, self.test_email, self.test_username, self.test_password
            )
            print("Test user created successfully.")
        except Exception as err:
            self.fail(f"Error creating test account: {err}")

        try:
            self.executor.execute(
                "SELECT idUsers FROM Users WHERE username = %s;", (self.test_username,)
            )
            result = self.executor.fetchone()
            if result:
                self.user_id = result[0]
            else:
                self.user_id = None
                self.fail("Failed to create test user.")
        except mysql.connector.Error as err:
            self.fail(f"Error fetching user ID: {err}")

        app.config["TESTING"] = True
        self.client = app.test_client()

        global user
        user = (self.test_username, self.user_id)

    def tearDown(self):
        """
        Tear down after each test.
        """
        try:
            if self.db.is_connected():
                self.db.rollback()
                self.executor.close()
                self.db.close()
                print("Database connection closed successfully.")
        except AttributeError:
            pass

    def test_add_to_watched_history(self):
        """
        Test adding a movie to the watched history.
        """
        response = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json.get("status"), "success")
        print("Add to watched history response:", response.json)

        # Verify the database entry
        try:
            self.executor.execute(
                "SELECT * FROM WatchedHistory WHERE user_id = %s AND movie_id = %s;",
                (self.user_id, 11),
            )
            result = self.executor.fetchone()
            self.assertIsNotNone(result, "Movie was not added to watched history.")
            print("WatchedHistory entry verified successfully.")
        except mysql.connector.Error as err:
            self.fail(f"Error verifying watched history: {err}")

    def test_add_duplicate_to_watched_history(self):
        """
        Test adding the same movie twice to the watched history.
        """
        # Add the movie once
        response1 = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json.get("status"), "success")
        print("First add to watched history response:", response1.json)

        # Attempt to add the same movie again
        response2 = self.client.post(
            "/add_to_watched_history",
            data=json.dumps({"imdb_id": "tt0076759"}),
            content_type="application/json",
        )
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response2.json.get("status"), "info")
        print("Duplicate add to watched history response:", response2.json)

    def test_get_watched_history(self):
        """
        Test retrieving watched history.
        """
        # Add a movie to watched history
        response1 = self.client.post(
            "/add_to_watched_history",
            data=json.dumps(
                {"imdb_id": "tt0076759", "watched_date": "2024-11-23 10:00:00"}
            ),
            content_type="application/json",
        )
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response1.json.get("status"), "success")
        print("Add to watched history response:", response1.json)

        # Retrieve watched history
        response = self.client.get("/getWatchedHistoryData")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)
        self.assertGreater(len(response.json), 0)
        self.assertEqual(response.json[0].get("movie_name"), "Star Wars (1977)")
        print("Get watched history response:", response.json)


if __name__ == "__main__":
    unittest.main()
