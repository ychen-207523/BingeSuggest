"""
Test suite for recommender system
"""

import sys
import unittest
import warnings
sys.path.append("../")
from src.prediction_scripts.item_based import recommend_for_new_user

warnings.filterwarnings("ignore")


class Tests(unittest.TestCase):
    """
    Test cases for recommender system
    """

    def test_toy_story(self):
        """
        Test case 1
        """
        ts = [
            {"title": "Toy Story (1995)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue("Toy Story 3 (2010)" in recommendations)

    def test_kunfu_panda(self):
        """
        Test case 2
        """
        ts = [
            {"title": "Kung Fu Panda (2008)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue("Toy Story (1995)" in recommendations)

    def test_horror_with_cartoon(self):
        """
        Test case 3
        """
        ts = [
            {"title": "Strangers, The (2008)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Toy Story (1995)" in recommendations) is False)

    def test_iron_man(self):
        """
        Test case 4
        """
        ts = [
            {"title": "Iron Man (2008)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Avengers: Infinity War - Part I (2018)" in recommendations))

    def test_robo_cop(self):
        """
        Test case 5
        """
        ts = [
            {"title": "RoboCop (1987)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("RoboCop 2 (1990)" in recommendations))

    def test_nolan(self):
        """
        Test case 6
        """
        ts = [
            {"title": "Inception (2010)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Dark Knight, The (2008)" in recommendations))

    def test_dc(self):
        """
        Test case 7
        """
        ts = [
            {"title": "Man of Steel (2013)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(
            ("Batman v Superman: Dawn of Justice (2016)" in recommendations)
        )

    def test_armageddon(self):
        """
        Test case 8
        """
        ts = [
            {"title": "Armageddon (1998)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("2012 (2009)" in recommendations))

    def test_lethal_weapon(self):
        """
        Test case 9
        """
        ts = [
            {"title": "Lethal Weapon (1987)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Lethal Weapon 3 (1992)" in recommendations))

    def test_dark_action(self):
        """
        Test case 10
        """
        ts = [
            {"title": "Batman: The Killing Joke (2016)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Punisher: War Zone (2008)" in recommendations))

    def test_dark(self):
        """
        Test case 11
        """
        ts = [
            {"title": "Puppet Master (1989)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Black Mirror: White Christmas (2014)" in recommendations))

    def test_horror_comedy(self):
        """
        Test case 12
        """
        ts = [
            {"title": "Scary Movie (2000)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("I Sell the Dead (2008)" in recommendations))

    def test_super_heroes(self):
        """
        Test case 13
        """
        ts = [
            {"title": "Spider-Man (2002)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Iron Man 2 (2010)" in recommendations))

    def test_cartoon(self):
        """
        Test case 14
        """
        ts = [
            {"title": "Moana (2016)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Monsters, Inc. (2001)" in recommendations))

    def test_multiple_movies(self):
        """
        Test case 15
        """
        ts = [
            {"title": "Harry Potter and the Goblet of Fire (2005)", "rating": 5.0},
            {"title": "Twilight Saga: New Moon, The (2009)", "rating": 5.0},
        ]
        recommendations = recommend_for_new_user(ts)
        self.assertTrue(("Twilight (2008)" in recommendations))


if __name__ == "__main__":
    unittest.main()
