import unittest
from flask import Flask
from ProductionCode.datasource import DataSource
from app import *

class TestSupremeCourtApp(unittest.TestCase):

    def setUp(self):
    
        """
        Set up test: load dataset and flask app.
        """
        global test
    
        self.app = app.test_client()
        test = DataSource()

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
        expected_output = 'WODouglas - Regular concurrence\nPStewart - Regular concurrence\nTMarshall - Voted with majority\nWJBrennan - Voted with majority\nBRWhite - Dissent\nWEBurger - Regular concurrence\nHABlackmun - Voted with majority\nLFPowell - Voted with majority\nWHRehnquist - Dissent'
        self.assertIn(expected_output, result)


    def test_display_find_justice_votes_invalid(self):
    
        """
        Test display value for invalid find justice votes input.
        """
    
        result = display_find_justice_votes("invalid_case_id")
        self.assertEqual(result, "Invalid U.S. Citation ID")
        
        
    def test_display_case_identifier_valid(self):
    
        """
        Test correct display value for case identifier function.
        """
    
        result = display_find_case_ids("410 U.S. 113")
        self.assertIn("ROE et al. v. WADE, DISTRICT ATTORNEY OF DALLAS COUNTY", result) 


    def test_display_case_identifier_invalid(self):
    
        """
        Test display value for invalid case identifier input.
        """
    
        result = display_find_case_ids("invalid_case_id")
        self.assertEqual(result, "Invalid U.S. Citation ID")
        
    def test_display_all_justice_votes_valid(self):
    
        """
        Test correct display value for find name function.
        """
    
        result = display_find_all_justice_votes("RHJackson")
        self.assertIn("UNITED STATES DEPARTMENT OF AGRICULTURE, EMERGENCY CROP AND FEED LOANS v. REMUND, ADMINISTRATOR - Voted with majority", result) 


    def test_display_all_justice_votes_invalid(self):
    
        """
        Test display value for invalid find name input.
        """
    
        result = display_find_all_justice_votes("invalid_name")
        self.assertEqual(result, "Invalid Justice Name")

    
    def test_create_case_id_dropdown(self):
    
        """
        Test correct case ID dropdown creation.
        """
        
        one_expected_id = "329 U.S. 69"
        self.assertIn(one_expected_id, create_case_id_dropdown())
    
    def test_create_justice_name_dropdown(self):
    
        """
        Test correct justice name dropdown creation.
        """
        
        one_expected_name = "HHBurton"
        self.assertIn(one_expected_name, create_justice_name_dropdown())

    def test_homepage(self):
    
        """
        Test correct homepage output.
        """
        
        response = self.app.get('/')
        self.assertIn(b"Supreme Court Data", response.data)
        

    def test_route_find_name_valid(self):
        
        """
        Test that the app route returns the correct information for the find name function.
        """
    
        response = self.app.get('/case_name?search=329+U.S.+40')
        self.assertIn(b"UNITED STATES v. ALCEA BAND OF TILLAMOOKS ET AL.", response.data) 


    def test_route_find_name_invalid(self):
    
        """
        Test that the app route returns an error for invalid case name for the find name function.
        """
    
        response = self.app.get('/case_name?search=invalid_case_id')
        self.assertIn(b"Invalid U.S. Citation ID", response.data)


    def test_route_find_justice_votes_valid(self):

        """
        Test that the app route returns the correct information for the find justice votes function.
        """
    
        response = self.app.get('/justice_votes?search=410+U.S.+113')
        self.assertIn(b'WODouglas - Regular concurrence\nPStewart - Regular concurrence\nTMarshall - Voted with majority\nWJBrennan - Voted with majority\nBRWhite - Dissent\nWEBurger - Regular concurrence\nHABlackmun - Voted with majority\nLFPowell - Voted with majority\nWHRehnquist - Dissent', response.data) 

    def test_route_find_justice_votes_invalid(self):
    
        """
        Test that the app route returns an error for invalid case name for the find justice votes function.
        """
    
        response = self.app.get('/justice_votes?search=invalid_case_id')
        self.assertIn(b"Invalid U.S. Citation ID", response.data)

    def test_route_case_identifiers_valid(self):
        """
        Test that the app route returns the correct message for the case identifier function.
        """
    
        response = self.app.get('case_identifiers?search=329+U.S.+40')
        
        self.assertIn(b"U.S. Reporter: 329 U.S. 40", response.data)

        
    def test_route_case_identifiers_invalid(self):
        """
        Test that the app route returns an error for invalid case name for the case identifier function.
        """
    
        response = self.app.get('case_identifiers?search=invalid')
        
        self.assertIn(b"Invalid U.S. Citation ID",response.data)
        
    def test_route_all_justice_votes_valid(self):
        """
        Test that the app route returns the correct message for the all votes for justice function.
        """
    
        response = self.app.get('/all_justice_votes?search=HHBurton')
        self.assertIn(b"HALLIBURTON OIL WELL CEMENTING CO. v. WALKER et al., DOING BUSINESS AS DEPTHOGRAPH CO. - Dissent",response.data)
    
    def test_route_all_justice_votes_invalid(self):
        """
        Test that the app route returns the error message for the all votes for justice function if input is invalid.
        """
    
        response = self.app.get('/all_justice_votes?search=invalid')
        self.assertIn(b'Invalid Justice Name',response.data)
    
    def test_display_all_justice_votes_selection(self):
        """
        Test that the app route returns instructions for empty input for the all justice votes function.
        """
    
        response = self.app.get('/all_justice_votes?search=')
        self.assertIn(b'Select justice name from the dropdown menu',response.data)
        
    def test_route_case_identifiers_selection(self):
        """
        Test that the app route returns instructions for empty input for the case identifier function.
        """
    
        response = self.app.get('case_identifiers?search=')
        
        self.assertIn(b"Select case ID from the dropdown menu",response.data)
        
    def test_route_find_justice_votes_selection(self):
    
        """
        Test that the app route returns an error for empty input for the find justice votes function.
        """
    
        response = self.app.get('/justice_votes?search=')
        self.assertIn(b"Select case ID from the dropdown menu", response.data)
        
    def test_route_find_name_selection(self):
    
        """
        Test that the app route returns an error for empty input for the find name function.
        """
    
        response = self.app.get('/case_name?search=')
        self.assertIn(b"Select case ID from the dropdown menu", response.data)
    
    
    def test_route_voting_info(self):
    
        """
        Test that the page that displays voting info contains correct information
        """
        
        response = self.app.get('/vote_explanation')
        self.assertIn(b'Voted with Majority:', response.data)
    
    def test_page_not_found(self):
        """
        Test that an error message is displayed for error 404.
        """
    
        response = self.app.get('/nonexistent_route')
        self.assertIn(b'Page not found. Please follow the buttons on the homepage by clicking the header.', response.data)
        
    
if __name__ == '__main__':

    unittest.main()