from pymongo import MongoClient
from Comparison import Compare

my_client = MongoClient("mongodb://localhost:27017/Sponsearch")
my_db = my_client["Sponsearch"]
my_cols = my_db["Researcher"]
lab_col = my_db["Research_Lab"]

comparison = Compare()

class Researcher:

    def add_info(self):

        #User provides basic information about themselves and their researcher
        name = input("\nPlease enter your full name: \n")
        background = input("\nPlease provide a brief description of your background and your skills: \n")
        tags = comparison.find_tags(background)

        #Add researcher information to the MongoDB
        user_data = {
            'Name': name,
            'Profile': background,
            'Tags': tags
        }
        result = my_cols.insert_one(user_data)
        print("Successfully added your information to the database! \n")

    def find_lab(self):

        #Retrieve document for the researcher being processed
        name = input("\nPlease enter your name: \n")
        researcher = my_cols.find_one({'Name': name})

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
                if comparison.fin_score(researcher, document) >= 0.25:
                    print("{}".format(document['Lab_Name']))
        print()

    #Controls all functions possible within the Researcher Class
    def main(self):
        print("\nHello! What are you in need of today?")
        action = input("1) Create Researcher Profile\n2) Search for a Lab\n3) Exit\n")
        while True:
            if int(action) == 1:
                self.add_info()
            elif int(action) == 2:
                self.find_lab()
            elif int(action) == 3:
                break
            print("Is there anything else you need?")
        print("Thank you!")

if __name__ == "__main__":
    Researcher().main()
