import csv
import argparse
import sys


def load_data():

    """
    Loads datasheet from the .csv file and saves it in a list of lists.
    Also creats a dictionary of header values corresponding to indicies in the list.
    """

    global court_data_list
    global indexer
    global vote_representation
    
    court_data_list = []

    court_data_csv = open("Data/SCDB_2022_01_justiceCentered_Citation.csv", "r", encoding="cp1252")
    court_data = csv.reader(court_data_csv, delimiter=',')
    for row in court_data:
        court_data_list.append(row) 
    court_data_csv.close()
    
    header = court_data_list[0]
    indexer = {}
    for i in range(len(header)):
        indexer[header[i]] = i
        
            
    vote_representation = {"1": "Voted with majority"
                           "2": "Dissent"
                           "3": "Regular Concurrence"
                           "4": "Special Concurrence"
                           "5": "Judgement of the Court"
                           "6": "Dissent from denial of certiorari or of affirmation appeal"
                           "7": "Jurisdictional dissent"
                           "8": "Participation in equally divided vote"}


def case_name_lookup(us_cite_id: str) -> str:

    """
    Takes U.S. Reporter Citation as input and returns the corresponding full case name.
    Raises LookupError if U.S. Reporter Citation is not valid/found.
    """

    case_name = None
    
    for row in court_data_list[1:]:
        if row[indexer["usCite"]] == us_cite_id:
            case_name = row[indexer["caseName"]]
            break
            
    if case_name == None:
        raise LookupError("U.S. Reporter Citation ID not found")
    else:
        return case_name

    
def case_justice_votes(us_cite_id: str) -> list:

    """
    Takes U.S. Reporter Citation as input and returns a list of tuples containing justice name and how they voted.
    Raises LookupError if U.S. Reporter Citation is not valid/found.
    """

    case_votes = []
    
    for row in court_data_list[1:]:
        if row[indexer["usCite"]] == us_cite_id:
            justice_name = row[indexer["justiceName"]]
            numerical_vote = row[indexer["vote"]]
            justice_vote = vote_representation[numerical_vote]
            case_votes.append((justice_name, justice_vote))
    
    if case_votes == []:
        raise LookupError("U.S. Reporter Citation ID not found")
    else:
        return case_votes


def case_identifier_lookup(us_cite_id: str) -> dict:

    """
    Takes U.S. Reporter Citation as input and returns a dictionary of all case identifiers
    Raises LookupError if U.S. Reporter Citation is not valid/found.
    """
    
    ids = {}
    
    for row in court_data_list[1:]:
        if row[indexer["usCite"]] == us_cite_id:
            ids["U.S. Reporter"] = us_cite_id
            ids["Supreme Court Reporter"] = row[indexer["sctCite"]]
            ids["Lawyers' Edition Reports"] = row[indexer["ledCite"]]
            ids["LEXIS"] = row[indexer["lexisCite"]]
            ids["Case Name"] = row[indexer["caseName"]]
            break
    
    if ids == {}:
        raise LookupError("U.S. Reporter Citation ID not found")
    else:
        return ids
 
 
def all_justice_votes(justice: str) -> list:

    """
    Takes justice name as input and returns a list of tuples containing case name and the justice's vote.
    Raises LookupError if justice name is not valid/found.
    """
    
    justice_votes = []
    
    for row in court_data_list[1:]:
        if row[indexer["justiceName"]] == justice:
            justice_votes.append((row[indexer["caseName"]], vote_representation[row[indexer["vote"]]]))
            
    if justice_votes == []:
        raise LookupError("Justice not found")  
    else:
        return justice_votes
        
