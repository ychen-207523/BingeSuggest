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
        response = self.client.get('/getWatchedHistoryData')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [])
