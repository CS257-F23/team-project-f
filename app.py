from flask import Flask, render_template, request
from ProductionCode.supreme_court import *

app = Flask(__name__)


@app.route('/')
def homepage():
    # Define intermediate variables
    title = "Supreme Court Data"
    welcome_message = "Welcome to Supreme Court Database"
    website_description = "The features of this website are listed below."
    Find_case_name = "Find Case Name for Case"
    Find_justice_vote = "Find Justice Votes for Case"
    Find_case_identifier = "Find all Identifiers for Case"
    About = "About Us"
    About_message = "This is Group Deliverable 3 for Team F"
    Developers = "Team F"
    # Render the HTML template
    return render_template('homepage.html', title=title,
                           welcome_message=welcome_message,
                           website_description=website_description,
                           Find_case_name=Find_case_name,
                           Find_justice_vote=Find_justice_vote,
                           Find_case_identifier=Find_case_identifier,
                           About = About,
                           About_message=About_message,
                           Developers=Developers)
    
    
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
            display_votes += "\n"
        return display_votes[:-1]
        
        
def display_find_case_ids(case_id):

    """
    Calls function from ProductionCode to find, format, and return case ID data. Displays error message if an invalid ID was given.
    """
    
    try:
        ids = case_identifier_lookup(case_id)
        
    except LookupError:
        return "Invalid U.S. Citation ID"
        
    else:
        display_ids = ""
        for key, value in ids.items():
            display_ids += key+": "+value+"\n"
        return display_ids[:-1]

@app.route('/<function>', methods=['GET'], strict_slashes=False)
def came_name_displayer_page(function):

    '''
    Split page for case_name_finder feature with input case id
    '''
    
    search_query = request.args.get('search')
    func_text = ("Find "+(function.replace('_', ' ')).title()+" by Case ID")
    func_url = "/"+function
    
    if function != "case_name" and function != "justice_votes" and function != "case_identifiers":
        return "404"
    
    if search_query == "" or search_query == None:
        case_name_text="e.g., 329 U.S. 40"
    elif function == "case_name":
        case_name_text = display_find_name(search_query)
    elif function == "justice_votes":
        case_name_text = display_find_justice_votes(search_query)
    elif function == "case_identifiers":
        case_name_text = display_find_case_ids(search_query)
    
    return render_template('case_name_displayer.html', case_name_text=case_name_text, function_text=func_text, function_url=func_url)
    
@app.route('/<function>/<case_id>', strict_slashes=False)
def display_supreme_court_data(function, case_id):

    """
    Calls appropriate functions to display information based on URL. Displays error message if funtion does not exist.
    """

    if function == "case_name":
        if case_id == '' or case_id == None:
            return render_template('case_name_displayer.html',
                                   case_name_text = "e.g. 329 U.S. 40")
        
        
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

