import csv
import argparse

def load_data():
    global court_data_list
    court_data_list = []

    court_data_csv = open("Data/SCDB_2022_01_justiceCentered_Citation.csv", "r")
    court_data = csv.reader(court_data_csv, delimiter=',')
    for row in court_data:
        court_data_list.append(row)
    court_data_csv.close()

def case_name_lookup(id: str) -> str:
    # Assuming that the headers are present in the CSV
    # and finding the index of the columns by name
    header = court_data_list[0]
    usCite_index = header.index("usCite")
    caseName_index = header.index("caseName")
    
    # Iterating through the dataset to find the matching usCite
    for row in court_data_list[1:]:
        if row[usCite_index] == id:
            return row[caseName_index]  # Returning the corresponding caseName
    return "Case not found"  # Return None if no match is found

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Look up case name by case ID')
    parser.add_argument('--find_name', action='store_true')
    parser.add_argument('--us_citation', type=str, help='US Citation ID')
    args = parser.parse_args()
    
    load_data()
    
    if args.find_name and args.us_citation:
        print(case_name_lookup(args.us_citation))
