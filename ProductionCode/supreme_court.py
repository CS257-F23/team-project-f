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


def case_name_lookup(us_cite_id: str) -> str:

    """
    Takes U.S. Citation as input and returns the corresponding full case name.
    Raises LookupError if U.S. Citation is not valid/found.
    """

    case_name = None
    
    for row in court_data_list[1:]:
        if row[indexer["usCite"]] == us_cite_id:
            case_name = row[indexer["caseName"]]
            
    if case_name == None:
        raise LookupError("U.S. Citation ID not found")
    else:
        return case_name

    
def case_justice_votes(us_cite_id: str) -> list:

    """
    Takes U.S. Citation as input and returns a list of tuples containing justice name and how they voted.
    Raises LookupError if U.S. Citation is not valid/found.
    """

    case_votes = []
    
    for row in court_data_list[1:]:
        if row[indexer["usCite"]] == us_cite_id:
            justice_name = row[indexer["justiceName"]]
            justice_vote = row[indexer["vote"]]
            case_votes.append((justice_name, justice_vote))
    
    if case_votes == []:
        raise LookupError("U.S. Citation ID not found")
    else:
        return case_votes


def argument_logic(find_name: bool, find_justice_votes: bool, us_cite_id: str):

    """
    Handles cli argument logic and calls corresponding functions.
    """

    if find_name and us_cite_id:
        print(case_name_lookup(us_cite_id))
        
    if find_justice_votes and us_cite_id:
        for justice in case_justice_votes(us_cite_id):
            print(" - ".join(justice))
            

if __name__ == "__main__":

    """
    Handles command-line interface usage of the application.
    """
    
    parser = argparse.ArgumentParser(description='Dataset Lookup',
                                     epilog='Example: python3 supreme_court.py --find_name --us_citation "329 U.S. 143"')
    
    parser.add_argument('--find_name', action='store_true',
                        help='Finds the full name of a case')
                        
    parser.add_argument('--find_justice_votes', action='store_true',
                        help='Finds the votes for each justice of a case')
                        
    parser.add_argument('--us_citation', type=str,
                        required=('--find_name' in sys.argv or '--find_justice_votes' in sys.argv),
                        help='U.S. Citation ID; required  if options that involve lookups by case are used')
                        
    args = parser.parse_args(args=(sys.argv[1:] or ['-h']))
    
    load_data()
    
    argument_logic(args.find_name, args.find_justice_votes, args.us_citation)
        
