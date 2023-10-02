import unittest
from ProductionCode.supreme_court import *

class TestFeatures(unittest.TestCase):  
    def setUp(self):
        #Load data before any test start
        load_data()
        

    def test_case_justice_votes_1(self):
        #first test for the case_justice_votes feature
        vote_list = case_justice_votes("329 U.S. 1")
        expected_list = [('HHBurton', '2'), ('RHJackson', '1'),
                         ('WODouglas', '1'), ('FFrankfurter', '4'),
                         ('SFReed', '1'), ('HLBlack', '1'),
                         ('WBRutledge', '1'), ('FMurphy', '1'), ('FMVinson', '1')]
        self.assertEqual(vote_list,expected_list)
        
        
    def test_case_justice_votes_2(self):
        #second test for the case_justice_votes feature
        vote_list = case_justice_votes("329 U.S. 143")
        expected_list = [('HHBurton', '1'), ('RHJackson', '1'),
                         ('WODouglas', '1'), ('FFrankfurter', '1'),
                         ('SFReed', '1'), ('HLBlack', '1'),
                         ('WBRutledge', '1'), ('FMurphy', '1'), ('FMVinson', '1')]
        self.assertEqual(vote_list,expected_list)
            
            
    def test_no_id_justice_votes(self):
        #test the edge cases for case_justice_votes feature
        with self.assertRaises(LookupError):
            case_justice_votes("tests")

    
    def test_case_name_lookup(self):
        #test the case_name_lookup feature
        case_name = case_name_lookup("329 U.S. 40")
        expected_name = "UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL."
        self.assertEqual(case_name,expected_name)
        
        
    def test_no_id_name_lookup(self):
        #test edge case for the case_name_lookup feature
        with self.assertRaises(LookupError):
            case_name_lookup("asdf")
           
           
if __name__ == '__main__':
    unittest.main()