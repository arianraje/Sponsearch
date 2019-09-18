from pymongo import MongoClient
from Comparison import Compare

my_client = MongoClient("mongodb://localhost:27017/Sponsearch")
my_db = my_client["Sponsearch"]
my_cols = my_db["Sponsor"]
lab_col = my_db["Research_Lab"]

comparison = Compare()

class Sponsor:

    def add_info(self):

        #User provides basic information about the research lab
        org = input("\nPlease provide the name of your organization or corporation: \n")
        interests = input("Pleas write a brief description of research initiatives you would be interested in: \n")
        tags = comparison.find_tags(interests)

        #Add the sponsor information to the MongoDB
        sponsor_data = {
            'Organization': org,
            'Profile': interests,
            'Tags': tags
        }
        result = my_cols.insert_one(sponsor_data)
        print("Successfully added your information to the database! \n")

    def find_lab(self):

        #Retrieve document for the researcher being processed
        org = input("\nPlease enter the name of your organization: \n")
        organization = my_cols.find_one({'Organization': org})

        #Determine search method
        search = input("How would you like to search: 1) By Institution 2) By Interests? \n")
        if int(search) == 1:
            inst = input("What is the name of the institution? \n")
            inst_labs = lab_col.find({'Institution': inst})
            print("\nHere are a list of labs at the institution you are searching for: ")
            for val in inst_labs:
                print("{}".format(val['Lab_Name']))
        elif int(search) == 2:
            #Iterate over documents in collection
            print("\nHere are a list of labs that share similar interests: ")
            for document in lab_cols.find():
                if comparison.fin_score(organization, document) >= 0.25:
                    print("{}".format(document['Lab_Name']))
        print()

    #Controls all functions possible within the Research Lab Class
    def main(self):
        print("\nHello! What are you in need of today?")
        while True:
            action = input("1) Create New Corporate/Organizational Sponsor Account\n2) Search for Labs to Sponsor\n3) Exit\n")
            if int(action) == 1:
                self.add_info()
            elif int(action) == 2:
                self.find_lab()
            elif int(action) == 3:
                break
            print("Is there anything else you need?")
        print("Thank you!")

if __name__ == "__main__":
    Sponsor().main()
