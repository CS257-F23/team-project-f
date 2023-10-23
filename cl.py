import csv
import argparse
import sys
from ProductionCode.supreme_court import *


def argument_logic(find_name: bool, find_justice_votes: bool, find_all_identifiers: bool, find_all_justice_votes: bool,
                   us_cite_id: str, justice: str):

    """
    Handles cli argument logic and calls corresponding functions.
    """

    if find_name and us_cite_id:
        print(case_name_lookup(us_cite_id))
        
    if find_justice_votes and us_cite_id:
        for justice in case_justice_votes(us_cite_id):
            print(" - ".join(justice))
            
    if find_all_identifiers and us_cite_id:
        for key, value in case_identifier_lookup(us_cite_id).items():
            print(key + ": " + value)
            
    if find_all_justice_votes and justice:
        for case in all_justice_votes(justice):
            print(" - ".join(case))
            

if __name__ == "__main__":

    """
    Handles command-line interface usage of the application.
    """
    
    parser = argparse.ArgumentParser(description='Dataset Lookup',
                                     epilog='Example: python3 cl.py --find_name --us_citation "329 U.S. 143"')
    
    parser.add_argument('--find_name', action='store_true',
                        help='Finds the full name of a case')
                        
    parser.add_argument('--find_justice_votes', action='store_true',
                        help='Finds the votes for each justice of a case')
                        
    parser.add_argument('--find_all_identifiers', action='store_true',
                        help='Finds all identifiers of a case')
    
    parser.add_argument('--find_all_justice_votes', action='store_true',
                        help='Finds all votes for every case a justice has voted on')
                        
    parser.add_argument('--us_citation', type=str,
                        required=('--find_name' in sys.argv or '--find_justice_votes' in sys.argv or '--find_all_identifiers' in sys.argv),
                        help='U.S. Reporter Citation ID; required if options that involve case lookups are used')
                        
    parser.add_argument('--justice', type=str,
                        required=('--find_all_justice_votes' in sys.argv),
                        help='Justice name; formatted as [first initial][middle initial (if present)][last name] e.g. "HHBurton";\
                        required if options that involve justice lookup are used')
                        
    args = parser.parse_args(args=(sys.argv[1:] or ['-h']))
    
    load_data()
    
    argument_logic(args.find_name, args.find_justice_votes, args.find_all_identifiers, args.find_all_justice_votes,
                   args.us_citation, args.justice)