import unittest
import subprocess
from ProductionCode.datasource import DataSource

class TestFeatures(unittest.TestCase):  
    def setUp(self):
        """
        Load data as test setup
        """
        global test
        test = DataSource()
        
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
        vote_list = test.case_justice_votes("329 U.S. 1")
        expected_list = [('HHBurton', 'Dissent'), ('RHJackson', 'Voted with majority'),
                         ('WODouglas', 'Voted with majority'), ('FFrankfurter', 'Special concurrence'),
                         ('SFReed', 'Voted with majority'), ('HLBlack', 'Voted with majority'),
                         ('WBRutledge', 'Voted with majority'), ('FMurphy', 'Voted with majority'), 
                         ('FMVinson', 'Voted with majority')]
        self.assertEqual(vote_list,expected_list)
        
        
    def test_case_justice_votes_2(self):
        """
        Second test for the case_justice_votes feature
        """
        vote_list = test.case_justice_votes("329 U.S. 143")
        expected_list = [('HHBurton', 'Voted with majority'), ('RHJackson', 'Voted with majority'),
                         ('WODouglas', 'Voted with majority'), ('FFrankfurter', 'Voted with majority'),
                         ('SFReed', 'Voted with majority'), ('HLBlack', 'Voted with majority'),
                         ('WBRutledge', 'Voted with majority'), ('FMurphy', 'Voted with majority'),
                         ('FMVinson', 'Voted with majority')]
        self.assertEqual(vote_list,expected_list)
            
            
    def test_invalid_id_justice_votes(self):
        """
        Test the edge cases for calling case_justice_votes with an invalid ID
        """
        self.assertRaises(LookupError, test.case_justice_votes, "tests")
    
    def test_no_id_justice_votes(self):
        """
        Test the edge cases for calling case_justice_votes with no input
        """
        self.assertRaises(TypeError, test.case_justice_votes)
    
    def test_case_name_lookup(self):
        """
        Test the case_name_lookup feature
        """
        case_name = test.case_name_lookup("329 U.S. 40")
        expected_name = "UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL."
        self.assertEqual(case_name,expected_name)
        
        
    def test_invalid_id_name_lookup(self):
        """
        Test edge case for calling case_name_lookup with an invalid ID input
        """
        self.assertRaises(LookupError, test.case_name_lookup, "asdf")
           
           
    def test_no_input_name_lookup(self):
        """
        Test edge case for calling case_name_lookup with no input
        """
        self.assertRaises(TypeError, test.case_name_lookup)
        
    def test_case_identifiers(self):
        """
        Test the case identifier lookup feature for valid input
        """
        case_ids = test.case_identifier_lookup("329 U.S. 40")
        expected_ids = {"U.S. Reporter": "329 U.S. 40", "Supreme Court Reporter": "67 S. Ct. 167",
                        "Lawyers' Edition Reports": "91 L. Ed. 29", "LEXIS": "1946 U.S. LEXIS 1696",
                        "Case Name": "UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL."}
        
        self.assertEqual(case_ids, expected_ids)
        
    def test_invalid_id_case_identifiers(self):
        """
        Test that case identifier lookup feature throws error for invalid output
        """
        self.assertRaises(LookupError, test.case_identifier_lookup, "ddddddd")
        
    def test_no_input_case_identifiers(self):
        """
        Test that case identifier lookup feature throws error when no input given
        """
        self.assertRaises(TypeError, test.case_identifier_lookup)
        
    def test_all_justice_votes(self):
        """
        Test the all justice votes feature for valid input
        """
        all_votes = test.all_justice_votes("HHBurton")
        one_expected_vote = ("AYRSHIRE COLLIERIES CORP. ET AL. v. UNITED STATES ET AL.","1")
        self.assertIn(one_expected_vote, all_votes)

    def test_invalid_id_all_justice_votes(self):
        """
        Test that case identifier lookup feature throws error for invalid output
        """
        self.assertRaises(LookupError, test.all_justice_votes, "ddfsfsfsfsfdd")
        
    def test_no_input_all_justice_votes(self):
        """
        Test that case identifier lookup feature throws error when no input given
        """
        self.assertRaises(TypeError, test.all_justice_votes)

    def test_cli_name_lookup(self):
        """
        Test the command line for case_name_lookup method
        """
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                                   "--find_name", "--us_citation",
                                   "329 U.S. 40"])
        self.assertEqual(cli_out["out"].strip(),"UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL.")
            
    
    def test_cli_justice_votes(self):
        """
        Test the command line for justice_votes method
        """
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                                   "--find_justice_votes", "--us_citation",
                                   "329 U.S. 1"])
        expected_output = '''HHBurton - Dissent
RHJackson - Voted with majority
WODouglas - Voted with majority
FFrankfurter - Special concurrence
SFReed - Voted with majority
HLBlack - Voted with majority
WBRutledge - Voted with majority
FMurphy - Voted with majority
FMVinson - Voted with majority'''

        self.assertEqual(cli_out["out"].strip(),expected_output)
        
    def test_cli_case_identifiers(self):
        """
        Test the command line for case_identifier_lookup method
        """
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                                   "--find_all_identifiers", "--us_citation",
                                   "329 U.S. 40"])
        expected_output = '''U.S. Reporter: 329 U.S. 40
Supreme Court Reporter: 67 S. Ct. 167
Lawyers' Edition Reports: 91 L. Ed. 29
LEXIS: 1946 U.S. LEXIS 1696
Case Name: UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL.'''

        self.assertEqual(cli_out["out"].strip(),expected_output)
        
    def test_cli_all_justice_votes(self):
        """
        Test the command line for all_justice_votes method
        """
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                                   "--find_all_justice_votes", "--justice",
                                   "HHBurton"])
        expected_output = '''SOCIETE INTERNATIONALE POUR PARTICIPATIONS INDUSTRIELLES ET COMMERCIALES, S. A., v. ROGERS, ATTORNEY GENERAL, SUCCESSOR TO THE ALIEN PROPERTY CUSTODIAN, et al. - Voted with majority
ESKRIDGE v. WASHINGTON STATE BOARD OF PRISON TERMS AND PAROLES - Voted with majority
MCALLISTER v. MAGNOLIA PETROLEUM CO. - Voted with majority
HANSON, EXECUTRIX, et al. v. DENCKLA et al. - Dissent
MCKINNEY v. MISSOURI-KANSAS-TEXAS RAILROAD CO. et al. - Voted with majority
IVANHOE IRRIGATION DISTRICT et al. v. MCCRACKEN et al. - Voted with majority
MILLER v. UNITED STATES - Dissent
CITY OF TACOMA v. TAXPAYERS OF TACOMA et al. - Voted with majority
TRIPLETT v. IOWA. - Voted with majority
NATIONAL LABOR RELATIONS BOARD v. MILK DRIVERS AND DAIRY EMPLOYEES LOCAL UNIONS NOS. 338 AND 680, INTERNATIONAL BROTHERHOOD OF TEAMSTERS, CHAUFFEURS, WAREHOUSEMEN AND HELPERS OF AMERICA, AFL-CIO - Voted with majority
WIENER v. UNITED STATES - Voted with majority
NATIONAL LABOR RELATIONS BOARD v. UNITED STEELWORKERS OF AMERICA, CIO, et al. - Voted with majority
KNAPP v. SCHWEITZER, JUDGE OF THE COURT OF GENERAL SESSIONS, et al. - Voted with majority'''

        self.assertIn(expected_output, cli_out["out"].strip())
        
           
    def test_cli_invalid_id_justice_votes(self):
        """
        Test the edge case on command line for justice_votes method with invalid input
        """
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                              "--find_justice_votes", "--us_citation",
                              "Not existing id"])
                              
        self.assertIn("LookupError",cli_out["err"])
        
        
    def test_cli_invalid_id_name_lookup(self):
        """
        Test the edge case of command line name_lookup method with invalid input
        """        
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                              "--find_name", "--us_citation",
                              "INVALID"])
                          
        self.assertIn("LookupError",cli_out["err"])
        
    def test_cli_invalid_id_case_identifiers(self):
        """
        Test the edge case on command line for case_identifier_lookup method with invalid input
        """
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                              "--find_all_identifiers", "--us_citation",
                              "Not existing id"])
                              
        self.assertIn("LookupError",cli_out["err"])
        
        
    def test_cli_invalid_id_all_justice_votes(self):
        """
        Test the edge case of command line all_justice_votes method with invalid input
        """        
        cli_out = self.cli_helper(["python3", "-u", "cl.py",
                              "--find_all_justice_votes", "--justice",
                              "INVALID"])
                          
        self.assertIn("LookupError",cli_out["err"])
        
            
if __name__ == '__main__':
    unittest.main()