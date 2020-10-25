import unittest
import warnings
import sys
sys.path.append('../')
from Code.recommenderapp.search import Search

warnings.filterwarnings("ignore")

class Tests(unittest.TestCase):
    def testSearch(self):
        search_word = "toy"
        search = Search()
        filtered_dict = search.resultsTop10(search_word)
        expected_resp = ['Toy Story (1995)', 'Toys (1992)', 'Toy Story 2 (1999)', 'Toy, The (1982)', 'Toy Soldiers (1991)', 'Toy Story 3 (2010)', 'Babes in Toyland (1961)', 'Babes in Toyland (1934)']
        self.assertTrue(filtered_dict==expected_resp)


if __name__ == "__main__":
    unittest.main()