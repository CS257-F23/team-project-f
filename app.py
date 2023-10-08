from flask import Flask
from ProductionCode.supreme_court import *

app = Flask(__name__)

@app.route('/')
def homepage():

    """
    Displays instructions on the homepage.
    """

    message = "Usage: http://[hostname]:[port]/[function]/[U.S. Citation ID]<br>\
               Available Functions: 'find_name', 'find_justice_votes'<br>\
               <br>\
               find_name: Displays the full name of a Supreme Court case.<br>\
               find_justice_votes: Displays the votes from each justice in a Supreme Court case.<br>\
               <br>\
               Examples: http://127.0.0.1:5000/find_name/410%20U.S.%20113,\
               http://127.0.0.1:5000/find_justice_votes/410 U.S. 113"
               

    return message
    
    
def display_find_name(case_id):

    """
    Calls function from ProductionCode to find and return name of case. Displays error message if an invalid ID was given.
    """
    
    try:
        name = case_name_lookup(case_id)
        
    except LookupError:
        return "Invalid U.S. Citation ID"
        
    else:
        return name
        

def display_find_justice_votes(case_id):

    """
    Calls function from ProductionCode to find, format, and return justice voting data. Displays error message if an invalid ID was given.
    """
    
    try:
        votes = case_justice_votes(case_id)
        
    except LookupError:
        return "Invalid U.S. Citation ID"
        
    else:
        display_votes = ""
        for justice in votes:
            display_votes += " - ".join(justice)
            display_votes += "<br>"
        return display_votes

    
@app.route('/<function>/<case_id>', strict_slashes=False)
def display_supreme_court_data(function, case_id):

    """
    Calls appropriate functions to display information based on URL. Displays error message if funtion does not exist.
    """

    if function == "find_name":
        return display_find_name(case_id)
        
    elif function == "find_justice_votes":
        return display_find_justice_votes(case_id)
        
    else:
        return "Invalid function."
        
    
@app.errorhandler(404)
def page_not_found(e):

    """
    Displays error message for error 404.
    """

    return "Page not found. Please revisit the homepage to view instructions for using this website."
    

@app.errorhandler(500)
def internal_server_error(e):

    """
    Displays error message for error 500.
    """

    return "Internal server error."


if __name__ == '__main__':

    load_data()
    app.run()

