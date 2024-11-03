import pandas as pd
from admin import Admin
from client import Client
class System:
    def __init__(self):
        print('''Press * to enter as an admin admin.
Press # to enter as a client.''')
        print("Enter [exit] to exit the program. ")
        self.cOA()
    def cOA(self):
            choice=input("Enter your choice: ")
            choice=choice.lower()
            if(choice=="*"):
                Admin()
            elif(choice=="#"):
                Client()
            elif(choice=="exit"):
                print("\n ---- Exiting the system. ----")
                exit()
            else:
                print("Invalid choice! Retry!")
                self.cOA()
    


print("#################### Real Estate Management System ####################")
print("---- ---- ---- ---- ----")

system=System()