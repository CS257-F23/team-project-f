from flask import Flask, render_template, request, abort
from ProductionCode.supreme_court import *
from ProductionCode.datasource import DataSource

app = Flask(__name__)
dataset = DataSource()


@app.route('/')
def homepage():

    """
    Displays homepage for the website.
    """

    return render_template('homepage.html')
    
    
def display_find_name(case_id: str) -> str:

    """
    Calls function from ProductionCode to find and return name of case. Displays error message if an invalid ID was given.
    """
    
    try:
        name = dataset.case_name_lookup(case_id)
        
    except LookupError:
        return "Invalid U.S. Citation ID"
        
    else:
        return name
        

def display_find_justice_votes(case_id: str) -> str:

    """
    Calls function from ProductionCode to find, format, and return justice voting data. Displays error message if an invalid ID was given.
    """
    
    try:
        votes = dataset.case_justice_votes(case_id)
        
    except LookupError:
        return "Invalid U.S. Citation ID"
        
    else:
        display_votes = ""
        for justice in votes:
            display_votes += str(justice[0]) + " - " + str(justice[1])
            display_votes += "\n"
        return display_votes[:-1]
        
        
def display_find_case_ids(case_id: str) -> str:

    """
    Calls function from ProductionCode to find, format, and return case ID data. Displays error message if an invalid ID was given.
    """
    
    try:
        ids = dataset.case_identifier_lookup(case_id)
        
    except LookupError:
        return "Invalid U.S. Citation ID"
        
    else:
        display_ids = ""
        for key, value in ids.items():
            display_ids += key+": "+value+"\n"
        return display_ids[:-1]
        
        
def display_find_all_justice_votes(justice: str) -> str:

    """
    Calls function from ProductionCode to find, format, and return all justice voting data. Displays error message if an invalid ID was given.
    """

    try:
        votes = dataset.all_justice_votes(justice)
        
    except LookupError:
        return "Invalid Justice Name"
    
    else:
        display_votes = ""
        for case in votes:
            display_votes += str(case[0]) + " - " + str(case[1])
            display_votes += "\n"
        return display_votes[:-1]


def create_case_id_dropdown() -> list:

    """
    Creates and returns list of all case ids for dropdown menu
    """

    ids = dataset.get_case_id_form()
    return ids


def create_justice_name_dropdown() -> list:

    """
    Creates and returns list of all justice names for dropdown menu
    """

    names = dataset.get_justice_name_form()
    return names


@app.route('/case_name', methods=['GET'], strict_slashes=False)
def came_name_displayer_page():

    '''
    Displays case name search page.
    '''

    func_text = "Find Case Name by Case ID"
    func_url = "/case_name"
    query_text = "Enter Case ID"
    search_query = request.args.get('search')
    dropdown = create_case_id_dropdown()
    
    if search_query == None or search_query == "":
        case_name_text = "Select case ID from the dropdown menu"
    else:
        case_name_text = display_find_name(search_query)     
    
    return render_template('case_name_displayer.html', case_name_text=case_name_text, 
                           function_text=func_text, function_url=func_url,
                           query_text=query_text,dropdown=dropdown)
        
        
@app.route('/justice_votes', methods=['GET'], strict_slashes=False)
def justice_votes_displayer_page():
    
    '''
    Displays justice votes search page.
    '''
    
    func_text = "Find Justice Votes by Case ID"
    func_url = "/justice_votes"
    query_text = "Enter Case ID"
    search_query = request.args.get('search')
    dropdown = create_case_id_dropdown()
    
    if search_query == None or search_query == "":
        case_name_text = "Select case ID from the dropdown menu"         
    else:
        case_name_text = display_find_justice_votes(search_query)    

    return render_template('case_name_displayer.html', case_name_text=case_name_text, 
                           function_text=func_text, function_url=func_url,
                           query_text=query_text,dropdown=dropdown)
                           
                           
@app.route('/case_identifiers', methods=['GET'], strict_slashes=False)
def case_identifiers_displayer_page():

    '''
    Displays case identifiers search page.
    '''
    
    search_query = request.args.get('search')
    
    func_text = "Find Case Identifiers by Case ID"
    func_url = "/case_identifiers"
    query_text = "Enter Case ID"
    dropdown = create_case_id_dropdown()  
    
    if search_query == None or search_query == "":
        case_name_text = "Select case ID from the dropdown menu"         
    else:
        case_name_text = display_find_case_ids(search_query)   

    return render_template('case_name_displayer.html', case_name_text=case_name_text, 
                           function_text=func_text, function_url=func_url,
                           query_text=query_text,dropdown=dropdown)
                           
                           
@app.route('/all_justice_votes', methods=['GET'], strict_slashes=False)
def all_justice_votes_displayer_page():

    '''
    Displays all justice votes search page.
    '''
    
    search_query = request.args.get('search')
    
    func_text = "Find All Justice Votes by Justice Name"
    func_url = "/all_justice_votes"
    query_text = "Enter Justice Name"
    dropdown = create_justice_name_dropdown()
    
    if search_query == None or search_query == "":
        case_name_text = "Select justice name from the dropdown menu"         
    else:    
        case_name_text = display_find_all_justice_votes(search_query)   

    return render_template('case_name_displayer.html', case_name_text=case_name_text, 
                           function_text=func_text, function_url=func_url,
                           query_text=query_text, dropdown=dropdown)

    
@app.errorhandler(404)
def page_not_found(e):

    """
    Displays error message for error 404.
    """

    return render_template('404.html')
                           
    

@app.errorhandler(500)
def internal_server_error(e):

    """
    Displays error message for error 500.
    """

    return "Internal server error."


if __name__ == '__main__':

    app.run(host="stearns.mathcs.carleton.edu",port=5220)

