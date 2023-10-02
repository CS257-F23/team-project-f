import csv
import argparse
import sys

def load_data():
    global court_data_list
    global indexer
    
    court_data_list = []

    court_data_csv = open("Data/SCDB_2022_01_justiceCentered_Citation.csv", "r")
    court_data = csv.reader(court_data_csv, delimiter=',')
    for row in court_data:
        court_data_list.append(row)
    court_data_csv.close()
    
    header = court_data_list[0]
    indexer = {}
    for i in range(len(header)):
        indexer[header[i]] = i


def case_name_lookup(us_cite_id: str) -> str:

    case_name = None
    
    for row in court_data_list[1:]:
        if row[indexer["usCite"]] == us_cite_id:
            case_name = row[indexer["caseName"]]
            
    if case_name == None:
        raise LookupError("U.S. Citation ID not found")
    else:
        return case_name

    
def case_justice_votes(us_cite_id: str) -> list:

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
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Dataset Lookup')
    parser.add_argument('--find_name', action='store_true',
                        help='Finds the full name of a case')
                        
    parser.add_argument('--find_justice_votes', action='store_true',
                        help='Finds the votes for each justice of a case')
                        
    parser.add_argument('--us_citation', type=str,
                        required=('--find_name' in sys.argv or '--find_justice_votes' in sys.argv),
                        help='U.S. Citation ID; required  if options that involve lookups by case are used')
                        
    args = parser.parse_args()
    
    load_data()
    
    if args.find_name and args.us_citation:
        print(case_name_lookup(args.us_citation))
    elif args.find_justice_votes and args.us_citation:
        for justice in case_justice_votes(args.us_citation):
            print(" - ".join(justice))
        
