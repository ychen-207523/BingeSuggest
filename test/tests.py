from item_based import recommendForNewUser
import unittest
import warnings
warnings.filterwarnings("ignore")
class Tests(unittest.TestCase):
    def testToyStory(self):
        ts = [
            {'title':'Toy Story (1995)', 'rating':5.0},
         ] 
        recommendations = recommendForNewUser(ts)
        self.assertTrue("Toy Story 3 (2010)" in recommendations)

    def testKunfuPanda(self):
        ts = [
            {'title':'Kung Fu Panda (2008)', 'rating':5.0},
         ] 
        recommendations = recommendForNewUser(ts)
        self.assertTrue("Toy Story (1995)" in recommendations)

    def testHorrorWithCartoon(self):
        ts = [
            {'title':'Strangers, The (2008)', 'rating':5.0},
         ] 
        recommendations = recommendForNewUser(ts)
        self.assertTrue(("Toy Story (1995)" in recommendations) == False)

    def testIronMan(self):
        ts = [
            {'title':'Iron Man (2008)', 'rating':5.0},
         ] 
        recommendations = recommendForNewUser(ts)
        self.assertTrue(("Avengers: Infinity War - Part I (2018)" in recommendations))


if __name__ == "__main__":
    unittest.main()
