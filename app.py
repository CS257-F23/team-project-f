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

    search_query = request.args.get('search')
    dropdown = create_case_id_dropdown()
    
    if search_query == None or search_query == "":
        case_name_text = "Select case ID from the dropdown menu"
        contextual_info = "This page allows you to check the case name of a case"
    else:
        case_name_text = display_find_name(search_query)     
        contextual_info = "The name of the case you selected is:"
    
    return render_template('case_name_displayer.html', case_name_text=case_name_text, 
                           dropdown=dropdown,contextual_info=contextual_info)
        
        
@app.route('/justice_votes', methods=['GET'], strict_slashes=False)
def justice_votes_displayer_page():
    
    '''
    Displays justice votes search page.
    '''

    search_query = request.args.get('search')
    dropdown = create_case_id_dropdown()
    
    if search_query == None or search_query == "":
        case_name_text = "Select case ID from the dropdown menu"    
        contextual_info = "This page allows you to see the votes of justices of a certain case"     
    else:
        case_name_text = display_find_justice_votes(search_query)    
        contextual_info = "On the left is the name of the justice, and on the right is what their vote was."

    return render_template('case_justice_vote_displayer.html', case_name_text=case_name_text, 
                            dropdown=dropdown,contextual_info=contextual_info)
                           
                           
@app.route('/case_identifiers', methods=['GET'], strict_slashes=False)
def case_identifiers_displayer_page():

    '''
    Displays case identifiers search page.
    '''
    
    search_query = request.args.get('search')
    

    dropdown = create_case_id_dropdown()  
    
    if search_query == None or search_query == "":
        case_name_text = "Select case ID from the dropdown menu" 
        contextual_info = "This page allows you to see all of the other Identifiers of the case, use them to find this case in case you are using other databases"
                
    else:
        case_name_text = display_find_case_ids(search_query)   
        contextual_info = "The identifiers are shown as follows"

    return render_template('case_identifier_displayer.html', case_name_text=case_name_text, 
                            dropdown=dropdown,contextual_info=contextual_info)
                           
                           
@app.route('/all_justice_votes', methods=['GET'], strict_slashes=False)
def all_justice_votes_displayer_page():

    '''
    Displays all justice votes search page.
    '''
    
    search_query = request.args.get('search')
    
    dropdown = create_justice_name_dropdown()
    
    if search_query == None or search_query == "":
        case_name_text = "Select justice name from the dropdown menu" 
        contextual_info = "This page allows you to see all the votes of a justice"        
    else:    
        case_name_text = display_find_all_justice_votes(search_query)   
        contextual_info = "On the left is the name of the justice, and on the right is what their vote was."

    return render_template('all_votes_justice_displayer.html', case_name_text=case_name_text, 
                             dropdown=dropdown,contextual_info=contextual_info)

    
@app.errorhandler(404)
def page_not_found(e):

    """
    Displays error message for error 404.
    """

    return render_template('404.html')
                           
@app.route('/vote_explanation',strict_slashes=False)
def vote_explanation_displayer():

    """
    Displays the explanation for vote decisions
    """

    return render_template('vote_explanation.html')
    

@app.route('/identifiers_explanation',strict_slashes=False)
def identifiers_explanation_displayer():

    """
    Displays the explanation for different identifiers
    """

    return render_template('identifiers_explanation.html')


@app.errorhandler(500)
def internal_server_error(e):

    """
    Displays error message for error 500.
    """

    return "Internal server error."


if __name__ == '__main__':

    app.run(host="stearns.mathcs.carleton.edu",port=5120)

