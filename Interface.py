"""This is the interface for the Sponsearch programs. It allows users to
determine what kind of user they are (Research Lab or Corporate/Organizational
Sponsor) and what they would like to do (connect with other labs or sponsor
research)."""

from Lab import ResearchLab
from Researcher import Researcher
from Sponsor import Sponsor

def main():
    print("Welcome to Sponsearch where we help innovative research actualize. What kind of institution are you?")
    inst = input("1) Research Lab \n2) Resarcher \n3) Corporate/Organizational Sponsor \n")

    #Here we want the functions that will create an object for each type
    if int(inst) == 1:
        #Create Lab object
        lab = ResearchLab()
        lab.main()
    elif(int(inst)) == 2:
        #Create Researcher object
        researcher = Researcher();
        researcher.main()
    elif(int(inst)) == 3:
        #Create Sponsor Object
        sponsor = Sponsor()
        sponsor.main()

if __name__ == "__main__":
    main()
