import unittest
from flask import Flask
from ProductionCode.supreme_court import *
from app import *

class TestSupremeCourtApp(unittest.TestCase):

    def setUp(self):
    
        """
        Set up test: load dataset and flask app.
        """
    
        load_data()
        self.app = app.test_client()


    def test_display_find_name_valid(self):
    
        """
        Test correct display value for find name function.
        """
    
        result = display_find_name("410 U.S. 113")
        self.assertIn("ROE et al. v. WADE, DISTRICT ATTORNEY OF DALLAS COUNTY", result) 


    def test_display_find_name_invalid(self):
    
        """
        Test display value for invalid find name input.
        """
    
        result = display_find_name("invalid_case_id")
        self.assertEqual(result, "Invalid U.S. Citation ID")


    def test_display_find_justice_votes_valid(self):
    
        """
        Test correct display value for find justice votes function.
        """
    
        result = display_find_justice_votes("410 U.S. 113")
        expected_output = 'WODouglas - 3<br>PStewart - 3<br>TMarshall - 1<br>WJBrennan - 1<br>BRWhite - 2<br>WEBurger - 3<br>HABlackmun - 1<br>LFPowell - 1<br>WHRehnquist - 2<br>'
        self.assertIn(expected_output, result)


    def test_display_find_justice_votes_invalid(self):
    
        """
        Test display value for invalid find justice votes input.
        """
    
        result = display_find_justice_votes("invalid_case_id")
        self.assertEqual(result, "Invalid U.S. Citation ID")


    def test_homepage(self):
    
        """
        Test that necessary information is on the homepage.
        """
        
        response = self.app.get('/')
        self.assertIn(b"Supreme Court Data", response.data)
        

    def test_display_supreme_court_data_find_name_valid(self):
        
        """
        Test that the app route returns the correct information for the find name function.
        """
    
        response = self.app.get('/case_name?search=329+U.S.+40')
        self.assertIn(b"UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL.", response.data) 


    def test_display_supreme_court_data_find_name_invalid(self):
    
        """
        Test that the app route returns an error for invalid case name for the find name function.
        """
    
        response = self.app.get('/case_name?search=invalid_case_id')
        self.assertIn(b"Invalid U.S. Citation ID", response.data)


    def test_display_supreme_court_data_find_justice_votes_valid(self):

        """
        Test that the app route returns the correct information for the find justice votes function.
        """
    
        response = self.app.get('/justice_votes?search=410+U.S.+113')
        self.assertIn(b'WODouglas - 3<br>PStewart - 3<br>TMarshall - 1<br>WJBrennan - 1<br>BRWhite - 2<br>WEBurger - 3<br>HABlackmun - 1<br>LFPowell - 1<br>WHRehnquist - 2<br>', response.data) 

    def test_display_supreme_court_data_find_justice_votes_invalid(self):
    
        """
        Test that the app route returns an error for invalid case name for the find justice votes function.
        """
    
        response = self.app.get('/justice_votes?search=invalid_case_id')
        self.assertIn(b"Invalid U.S. Citation ID", response.data)

    def display_test_case_identifiers_valid(self):
        """
        Test that the app route returns the correct message for the case identifier function.
        """
    
        response = self.app.get('case_identifiers?search=329+U.S.+40')
        
        # Assert that all expected texts are included
        self.assertIn(b"U.S. Reporter: 329 U.S. 40", response.data)
        self.assertIn(b"Supreme Court Reporter: 67 S. Ct. 167", response.data)
        self.assertIn(b"Lawyers' Edition Reports: 91 L. Ed. 29", response.data)
        self.assertIn(b"LEXIS: 1946 U.S. LEXIS 1696", response.data)
        self.assertIn(b"Case Name: UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL.", response.data)
        
    def display_test_case_identifiers_invalid(self):
        """
        Test that the app route returns an error for invalid case name for the find justice votes function.
        """
    
        response = self.app.get('case_identifiers?search=invalid')
        
        self.assertIn(b"Invalid U.S. Citation ID",response)
        
    
    def test_page_not_found(self):
    
        """
        Test that an error message is displayed for error 404.
        """
    
        response = self.app.get('/nonexistent_route')
        self.assertIn(b"Page not found.", response.data)

if __name__ == '__main__':

    unittest.main()