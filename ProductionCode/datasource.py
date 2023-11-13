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
                         "3": "Regular concurrence",
                         "4": "Special concurrence",
                         "5": "Judgement of the Court",
                         "6": "Dissent from denial of certiorari or of affirmation appeal",
                         "7": "Jurisdictional dissent",
                         "8": "Participation in equally divided vote"
        }


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
        
        
    def query_lookup(self, query: str, var: str) -> list:
    
        '''
        Helper method for query lookup.
        '''
    
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(query,(var,))

        except Exception as e:
            return "An error has occurred while fetching the query: " + str(e)
            
        else:
            return(cursor.fetchall())
            
            
    def direct_query_lookup(self, query: str) -> list:
    
        '''
        Helper method for query lookup without variables.
        '''
    
        try:
            cursor = self.connection.cursor()
            
            cursor.execute(query)

        except Exception as e:
            return "An error has occurred while fetching the query: " + str(e)
            
        else:
            return(cursor.fetchall())
            
    
    def get_case_id_form(self) -> list:
    
        """
        Gets all case IDs in a list.
        """
        
        query = "SELECT usCite FROM caseinfo"
        
        hit = self.direct_query_lookup(query)
        final = []
        for row in hit:
            final.append(row[0])
            print(row[0])
        
        return final
        
    
    def get_justice_name_form(self) -> list:
    
        """
        Gets all justice names in a list.
        """
    
        query = "SELECT DISTINCT justiceName FROM voteinfo"
        
        hit = self.direct_query_lookup(query)
        final = []
        for row in hit:
            final.append(row[0])
        
        return final
        
        
    def all_justice_votes(self, justice: str) -> list:
    
        '''
        Searches the dataset to get all case names and voting data for one justice.
        '''

            
        query = "SELECT caseinfo.caseName, voteinfo.vote FROM voteinfo INNER JOIN caseinfo \
                 ON voteinfo.lexisCite=caseinfo.lexisCite WHERE justiceName=%s"
                 
        hit = self.query_lookup(query, justice)  
        votes = []
        
        for row in hit:
            if row[1] == None:
                newrow = [row[0], None]
            else:
                newrow = [row[0], self.voteinfo[row[1]]]
            votes.append(newrow)
        
        return votes

    
    def case_identifier_lookup(self, us_cite_id: str) -> dict:
    
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
        
        
    def case_name_lookup(self, us_cite_id: str) -> str:

        '''
        Searches the dataset to get case name by U.S. Citation ID.
        '''
        
        query = "SELECT caseName FROM caseinfo WHERE usCite=%s"
        
        return (self.query_lookup(query, us_cite_id))[0][0]
        
        
    def case_justice_votes(self, us_cite_id: str) -> list:
    
        '''
        Searches the dataset to get all justice votes for a certain case by U.S. Citation ID.
        '''
        
        query = "SELECT voteinfo.justiceName, voteinfo.vote FROM caseinfo INNER JOIN voteinfo \
                 ON caseinfo.lexisCite=voteinfo.lexisCite WHERE usCite=%s"
        
        hit = self.query_lookup(query, us_cite_id)
        votes = []
        
        for row in hit:
            if row[1] == None:
                newrow = [row[0], None]
            else:
                newrow = [row[0], self.voteinfo[row[1]]]
            votes.append(newrow)
        
        return votes
    