import pandas as pd
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
                #client
                pass
            elif(choice=="exit"):
                exit()
            else:
                print("Invalid choice! Retry!")
                self.cOA()
    
class Admin:
    def __init__(self):
        self.authentication()
    
    def authentication(self):
            print()
            print("---- Admin Sub-system ---- ")
            print()
            print()
            print("---- Login Window ----")
            print()
            print("-- Enter Credentials --")
            username=input("Username:")
            username=username.lower()
            password=input("Password:")
            if(username=="admin" and password=="ABCXYZ"):
                print("Credentials matched!")
                print()
                print("<<<< Entering the system >>>>")
                self.adminMenu()
                
            else:
                print()
                print("Credential Mismatch!")
                print()
                print("Retry!")
                print()
                self.authentication()
    
    
    def adminMenu(self):
        while True:
            print("Press 1 to view a specific number of properties.")
            print("Press 2 to add a new listing (Property).")
            print("Press 3 to update an existing listing (Property).")
            print("Press 4 to delete an existing listing (Property).")
            print("Press 5 to sort the properties on the basis of price.")
            print("Enter 'back' to go back to the main menu.")
            print("Enter 'exit' to close the system.")

            preference=input("Enter your choice:").lower()
            if(preference=="1"):
                self.readProperties()
            elif(preference=='back'):
                System()
            elif(preference=='exit'):
                exit()
            else:
                print("Invalid choice! Enter again!")
                self.adminMenu()
            continue_choice = input("Do you want to continue using the admin menu? (yes/no): ").lower()
            if continue_choice == 'no':
                print("Exiting admin menu.")
            elif continue_choice != 'yes':
                print("Invalid choice! Please enter 'yes' or 'no'.")

    
    def readProperties(self):
        print("\n---- Displaying Properties ----")
        try:
            n = int(input("Enter the number of properties you would like to see (from the beginning): "))
            data = pd.read_csv("real_estate_data.csv")
            print(data.head(n))
        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except ValueError:
            print("Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")
    

print("#################### Real Estate Management System ####################")
print("---- ---- ---- ---- ----")

system=System()