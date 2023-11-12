import psycopg2
import ProductionCode.psqlConfig as config


class DataSource:

    def __init__(self):
    
        '''
        Constructor that initiates connection to database
        '''
        
        self.connection = self.connect()
        self.voteinfo = {"1": "Voted with majority",
                         "2": "Dissent",
                         "3": "Regular Concurrence",
                         "4": "Special Concurrence",
                         "5": "Judgement of the Court",
                         "6": "Dissent from denial of certiorari or of affirmation appeal",
                         "7": "Jurisdictional dissent",
                         "8": "Participation in equally divided vote"}

    def connect(self):
    
        '''
        Initiates connection to database using information in the psqlConfig.py file.
        Returns the connection object.
        '''

        try:
            connection = psycopg2.connect(database=config.database, user=config.user, host="localhost", password=config.password)
        except Exception as e:
            print("Connection error: ", e)
            exit()
        return connection
        
    def query_lookup(self, query, var):
    
        '''
        Helper method for query lookup
        '''
    
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(query,(var,))

        except Exception as e:
            return "An error has occurred while fetching the query: " + str(e)
            
        else:
            return(cursor.fetchall())
        
    def all_justice_votes(self, justice):
    
        '''
        Searches the dataset to get all case names and voting data for one justice.
        '''

            
        query = "SELECT caseinfo.caseName, voteinfo.vote FROM voteinfo INNER JOIN caseinfo \
                 ON voteinfo.lexisCite=caseinfo.lexisCite WHERE justiceName=%s"
                 
        hit = self.query_lookup(query, justice)  
        votes = []
        
        for row in hit:
            newrow = [row[0]]
            newrow[1] = self.voteinfo[row[1]]
            votes.append(newrow)
        
        return votes

    
    def case_identifier_lookup(self, us_cite_id):
    
        '''
        Searches the dataset to get all case identifiers from a U.S. Citation ID.
        '''
        
        query = "SELECT usCite, sctCite, ledCite, lexisCite, caseName FROM caseinfo WHERE usCite=%s"
        
        hit = self.query_lookup(query, us_cite_id)
        
        ids = {

               "U.S. Reporter": us_cite_id,
               "Supreme Court Reporter": hit[0][1],
               "Lawyers' Edition Reports": hit[0][2],
               "LEXIS": hit[0][3],
               "Case Name": hit[0][4]
        }
        
        return ids
        
    def case_name_lookup(self, us_cite_id):

        '''
        Searches the dataset to get case name by U.S. Citation ID.
        '''
        
        query = "SELECT caseName FROM caseinfo WHERE usCite=%s"
        
        return (self.query_lookup(query, us_cite_id))[0][0]
        
    def case_justice_votes(self, us_cite_id):
    
        '''
        Searches the dataset to get all justice votes for a certain case by U.S. Citation ID.
        '''
        
        query = "SELECT voteinfo.justiceName, voteinfo.vote FROM caseinfo INNER JOIN voteinfo \
                 ON caseinfo.lexisCite=voteinfo.lexisCite WHERE usCite=%s"
        
        hit = self.query_lookup(query, us_cite_id)
        votes = []
        
        for row in hit:
            newrow = [row[0],self.voteinfo[row[1]]]
            votes.append(newrow)
            print(newrow)
        
        return votes
    