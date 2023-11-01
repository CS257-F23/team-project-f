from flask import Flask, render_template, request, abort
from ProductionCode.supreme_court import *

app = Flask(__name__)


@app.route('/')
def homepage():
    # Define intermediate variables
    title = "Homepage"
    welcome_message = "Welcome to Supreme Court Database"
    website_description = "The features of this website are listed below."
    Find_case_name = "Find case name for case"
    Find_justice_vote = "Find justice votes for case"
    Find_case_identifier = "Find all identifiers for case"
    Find_all_justice_votes = "Find all votes for one justice"
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
                           Find_all_justice_votes=Find_all_justice_votes,
                           About=About,
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
        
        
def display_find_all_justice_votes(justice):

    try:
        votes = all_justice_votes(justice)
        
    except LookupError:
        return "Invalid Justice Name"
    
    else:
        display_votes = ""
        for case in votes:
            display_votes += " - ".join(case)
            display_votes += "\n"
        return display_votes[:-1]

@app.route('/<function>', methods=['GET'], strict_slashes=False)
def came_name_displayer_page(function):

    '''
    Split page for case_name_finder feature with input case id
    '''
        
    if function not in ("case_name","justice_votes","case_identifiers","all_justice_votes"):
        abort(404)
        
    title = "Homepage"
    Developers = "Team F"
    Find_case_name = "Find case name for case"
    Find_justice_vote = "Find justice votes for case"
    Find_case_identifier = "Find all identifiers for case"
    Find_all_justice_votes = "Find all votes for one justice"
    search_query = request.args.get('search')
    func_url = "/"+function
    search_term = " by Case ID"
    query_text = "Enter Case ID"
    
    if function == "all_justice_votes":
        search_term = " by Justice Name"
        query_text = "Enter Justice Name"

    func_text = ("Find "+(function.replace('_', ' ')).title()+search_term)

    
    if search_query == "" or search_query == None:
        case_name_text="Case name example: 329 U.S. 40\nJustice name example: HHBurton"
    elif function == "case_name":
        case_name_text = display_find_name(search_query)
    elif function == "justice_votes":
        case_name_text = display_find_justice_votes(search_query)
    elif function == "case_identifiers":
        case_name_text = display_find_case_ids(search_query)
    elif function == "all_justice_votes":
        case_name_text = display_find_all_justice_votes(search_query)
    
    return render_template('case_name_displayer.html', case_name_text=case_name_text, 
                           function_text=func_text, function_url=func_url,
                           title=title, Developers=Developers, query_text=query_text,
                           Find_case_name=Find_case_name,
                           Find_justice_vote=Find_justice_vote,
                           Find_case_identifier=Find_case_identifier,
                           Find_all_justice_votes=Find_all_justice_votes)
        
    
@app.errorhandler(404)
def page_not_found(e):

    """
    Displays error message for error 404.
    """
    
    title = "Supreme Court Data"
    Developers = "Team F"
    Find_case_name = "Find case name for case"
    Find_justice_vote = "Find justice votes for case"
    Find_case_identifier = "Find all identifiers for case"
    Find_all_justice_votes = "Find all votes for one justice"
    not_found_msg = "Page not found. Please follow the buttons on the homepage by clicking the header."
    
    return render_template('404.html', title=title, Developers=Developers, not_found_msg=not_found_msg,
                           Find_case_name=Find_case_name,
                           Find_justice_vote=Find_justice_vote,
                           Find_case_identifier=Find_case_identifier,
                           Find_all_justice_votes=Find_all_justice_votes)
    

@app.errorhandler(500)
def internal_server_error(e):

    """
    Displays error message for error 500.
    """

    return "Internal server error."


if __name__ == '__main__':

    load_data()
    app.run()

