import csv
import argparse



def load_data():
    global court_data_list
    court_data_list = []

    court_data_csv = open("Data/SCDB_2022_01_justiceCentered_Citation.csv", "r")
    court_data = csv.reader(court_data_csv, delimiter=',')
    court_data_list
    for row in court_data:
        court_data_list.append(row)
    court_data_csv.close()
    

if __name__ == "__main__":
    load_data()
    
    