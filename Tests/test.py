import unittest
import subprocess
from ProductionCode.supreme_court import *

class TestFeatures(unittest.TestCase):  
    def setUp(self):
        """
        Load data as test setup
        """
        load_data()
        
    def cli_helper(self, args):
        """
        Helper method for running subprocess
        """
        command = subprocess.Popen(args,stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   encoding="utf8")
        cli_out = {"out": command.communicate()[0], 
                   "err": command.communicate()[1]}
        command.terminate() 
        return cli_out
        

    def test_case_justice_votes_1(self):
        """
        First test for the case_justice_votes feature
        """
        vote_list = case_justice_votes("329 U.S. 1")
        expected_list = [('HHBurton', '2'), ('RHJackson', '1'),
                         ('WODouglas', '1'), ('FFrankfurter', '4'),
                         ('SFReed', '1'), ('HLBlack', '1'),
                         ('WBRutledge', '1'), ('FMurphy', '1'), ('FMVinson', '1')]
        self.assertEqual(vote_list,expected_list)
        
        
    def test_case_justice_votes_2(self):
        """
        Second test for the case_justice_votes feature
        """
        vote_list = case_justice_votes("329 U.S. 143")
        expected_list = [('HHBurton', '1'), ('RHJackson', '1'),
                         ('WODouglas', '1'), ('FFrankfurter', '1'),
                         ('SFReed', '1'), ('HLBlack', '1'),
                         ('WBRutledge', '1'), ('FMurphy', '1'), ('FMVinson', '1')]
        self.assertEqual(vote_list,expected_list)
            
            
    def test_invalid_id_justice_votes(self):
        """
        Test the edge cases for calling case_justice_votes with an invalid ID
        """
        with self.assertRaises(LookupError):
            case_justice_votes("tests")

    
    def test_no_id_justice_votes(self):
        """
        Test the edge cases for calling case_justice_votes with no input
        """
        with self.assertRaises(TypeError):
            case_justice_votes()
    
    
    def test_case_name_lookup(self):
        """
        Test the case_name_lookup feature
        """
        case_name = case_name_lookup("329 U.S. 40")
        expected_name = "UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL."
        self.assertEqual(case_name,expected_name)
        
        
    def test_invalid_id_name_lookup(self):
        """
        Test edge case for calling case_name_lookup with an invalid ID input
        """
        with self.assertRaises(LookupError):
            case_name_lookup("asdf")
           
           
    def test_no_input_name_lookup(self):
        """
        Test edge case for calling case_name_lookup with no input
        """
        with self.assertRaises(TypeError):
            case_name_lookup()


    def test_cli_name_lookup(self):
        """
        Test the command line for case_name_lookup method
        """
        cli_out = self.cli_helper(["python3", "-u", "ProductionCode/supreme_court.py",
                              "--find_name", "--us_citation",
                              "329 U.S. 40"])
        self.assertEqual(cli_out["out"].strip(),"UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL.")
            
    
    def test_cli_justice_votes(self):
        """
        Test the command line for justice_votes method
        """
        cli_out = self.cli_helper(["python3", "-u", "ProductionCode/supreme_court.py",
                              "--find_justice_votes", "--us_citation",
                              "329 U.S. 1"])
        expected_output = '''HHBurton - 2
RHJackson - 1
WODouglas - 1
FFrankfurter - 4
SFReed - 1
HLBlack - 1
WBRutledge - 1
FMurphy - 1
FMVinson - 1'''

        self.assertIn(cli_out["out"].strip(),expected_output)
        
           
    def test_edge_cli_justice_votes(self):
        """
        Test the edge case on command line for justice_votes method with invalid input
        """
        cli_out = self.cli_helper(["python3", "-u", "ProductionCode/supreme_court.py",
                              "--find_justice_votes", "--us_citation",
                              "Not existing id"])
        self.assertIn("LookupError",cli_out["err"])
        
        
    def test_cli_invalid_id_name_lookup(self):
        """
        Test the edge case of command line name_lookup method with invalid input
        """        
        cli_out = self.cli_helper(["python3", "-u", "ProductionCode/supreme_court.py",
                              "--find_name", "--us_citation",
                              "INVALID"])
                          
        self.assertIn("LookupError",cli_out["err"])
    

                    
            
if __name__ == '__main__':
    unittest.main()