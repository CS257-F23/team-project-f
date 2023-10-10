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
        self.assertEqual(result, "ROE et al. v. WADE, DISTRICT ATTORNEY OF DALLAS COUNTY") 


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
        self.assertIn(b"Usage Instructions", response.data)
        

    def test_display_supreme_court_data_find_name_valid(self):
        
        """
        Test that the app route returns the correct information for the find name function.
        """
    
        response = self.app.get('/find_name/410%20U.S.%20113')
        self.assertIn(b"ROE et al. v. WADE, DISTRICT ATTORNEY OF DALLAS COUNTY", response.data) 


    def test_display_supreme_court_data_find_name_invalid(self):
    
        """
        Test that the app route returns an error for invalid case name for the find name function.
        """
    
        response = self.app.get('/find_name/invalid_case_id')
        self.assertIn(b"Invalid U.S. Citation ID", response.data)


    def test_display_supreme_court_data_find_justice_votes_valid(self):

        """
        Test that the app route returns the correct information for the find justice votes function.
        """
    
        response = self.app.get('/find_justice_votes/410%20U.S.%20113')
        self.assertIn(b'WODouglas - 3<br>PStewart - 3<br>TMarshall - 1<br>WJBrennan - 1<br>BRWhite - 2<br>WEBurger - 3<br>HABlackmun - 1<br>LFPowell - 1<br>WHRehnquist - 2<br>', response.data) 

    def test_display_supreme_court_data_find_justice_votes_invalid(self):
    
        """
        Test that the app route returns an error for invalid case name for the find justice votes function.
        """
    
        response = self.app.get('/find_justice_votes/invalid_case_id')
        self.assertIn(b"Invalid U.S. Citation ID", response.data)

    def test_page_not_found(self):
    
        """
        Test that an error message is displayed for error 404.
        """
    
        response = self.app.get('/nonexistent_route')
        self.assertIn(b"Page not found.", response.data)

if __name__ == '__main__':

    unittest.main()