from pymongo import MongoClient
from Comparison import Compare

my_client = MongoClient("mongodb://localhost:27017/Sponsearch")
my_db = my_client["Sponsearch"]
my_cols = my_db["Research_Lab"]
researcher_col = my_db["Researcher"]

comparison = Compare()

class ResearchLab:

    def add_info(self):

        #User provides basic information about the research lab
        inst = input("\nPlease provide the name of the institution you are associated with: \n")
        lab = input("Please provide the name of your research lab: \n")
        lab_summ = input("Please provide a short summary of your lab research and objectives: \n")
        tags = comparison.find_tags(lab_summ)

        #Add the lab information to the MongoDB
        lab_data = {
            'Institution': inst,
            'Lab_Name': lab,
            'Profile': lab_summ,
            'Tags': tags
        }
        result = my_cols.insert_one(lab_data)
        print("Successfully added your information to the database! \n")

    def sim_lab(self):

        #Retrieve document for the lab being processed
        name = input("\nPlease provide the name of your research lab: \n")
        lab = my_cols.find_one({'Lab_Name': name})

        #Determine search method
        search = input("How would you like to search: 1) By Institution 2) By Interests? \n")
        if int(search) == 1:
            inst = input("What is the name of the institution? \n")
            inst_labs = my_cols.find({'Institution': inst})
            print("\nHere are a list of labs at the institution you are searching for: ")
            for val in inst_labs:
                print("{}".format(val['Lab_Name']))
        elif int(search) == 2:
            #Iterate over documents in collection
            print("\nHere are a list of labs that share similar interests: ")
            for document in my_cols.find():
                if lab['Lab_Name'] != document['Lab_Name']:
                    if comparison.fin_score(lab, document) >= 0.25:
                        print("{}".format(document['Lab_Name']))
        print()

    def find_researcher(self):

        #Retrieve document for the lab being processed
        name = input("\nPlease provide the name of your research lab: \n")
        lab = my_cols.find_one({'Lab_Name': name})

        print("\nHere are a list of researchers that share similar interests: ")
        for document in researcher_col.find():
            if comparison.fin_score(lab, document) >= 0.25:
                print("{}".format(document['Name']))
        print()

    #Controls all functions possible within the Research Lab Class
    def main(self):
        print("\nHello! What are you in need of today?")
        while True:
            action = input("1) Create New Lab\n2) Search for Similar Lab\n3) Find Researchers\n4) Exit\n")
            if int(action) == 1:
                self.add_info()
            elif int(action) == 2:
                self.sim_lab()
            elif int(action) == 3:
                self.find_researcher()
            elif int(action) == 4:
                break
            print("Is there anything else you need?")
        print("Thank you!")

if __name__ == "__main__":
    ResearchLab().main()
