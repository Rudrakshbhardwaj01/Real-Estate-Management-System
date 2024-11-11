import pandas as pd
class Admin:
    def __init__(self):
        self.authentication()
    
    def authentication(self):
        print("\n---- Admin Sub-system ----\n")
        print("---- Login Window ----\n")
        print("-- Enter Credentials --")
        username = input("Username: ").lower()
        password = input("Password: ")
        if username == "admin" and password == "ABCXYZ":
            print("Credentials matched!\n")
            print("<<<< Entering the system >>>>")
            self.adminMenu()
        else:
            print("\nCredential Mismatch!\nRetry!\n")
            self.authentication()

    def adminMenu(self):
        while True:
            print("Press 1 to view a specific number of properties.")
            print("Press 2 to add a new listing (Property).")
            print("Press 3 to update an existing listing (Property).")
            print("Press 4 to delete an existing listing (Property).")
            print("Press 5 to search for properties on the basis of specific attributes.")
            print("Enter 'back' to go back to the main menu.")
            print("Enter 'exit' to close the system.")

            preference = input("Enter your choice: ").lower()
            if preference == "1":
                Admin.readProperties()
            elif preference == "2":
                self.addProperty()
            elif preference == "3":
                self.updateProperty()
            elif preference == "4":
                self.deleteProperty()
            elif preference == "5":
                from client import Client
                Client().searchProperties()
            elif preference == 'back':
                from system import System
                System()
            elif preference == 'exit':
                exit()
            else:
                print("Invalid choice! Enter again!")
                self.adminMenu()

            continue_choice = input("Do you want to continue using the admin menu? (yes/no): ").lower()
            if continue_choice == 'no':
                print("Exiting admin menu.")
                break
            elif continue_choice != 'yes':
                print("Invalid choice! Please enter 'yes' or 'no'.")

    @staticmethod
    def readProperties():
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

    def addProperty(self):
        print("\n---- Adding New Property ----")
        try:
            house_type = input("Enter House Type: ").strip()
            address = input("Enter Address: ").strip()
            bhk_type = input("Enter BHK Type: ").strip()
            garage_included = input("Garage Included (yes/no): ").strip().lower()
            yard_available = input("Yard Available (yes/no): ").strip().lower()
            price = int(input("Enter Price: ").strip())

            data = pd.read_csv("real_estate_data.csv")

            new_property = {
                "House Type": house_type,
                "Address": address,
                "BHK Type": bhk_type,
                "Garage Included": garage_included,
                "Yard Available": yard_available,
                "price": price
            }

            new_property_df = pd.DataFrame([new_property])
            data = pd.concat([data, new_property_df], ignore_index=True)
            data.to_csv("real_estate_data.csv", index=False)
            print("New property added successfully.")

        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except ValueError:
            print("Invalid input for price. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def updateProperty(self):
        print("\n---- Updating Existing Property ----")
        try:
            data = pd.read_csv("real_estate_data.csv")
            property_id = int(input("Enter the row number of the property you want to update: "))

            if property_id >= len(data) or property_id < 0:
                print("Property ID does not exist.")
                return

            data.at[property_id, "House Type"] = input("Enter new House Type (leave blank to keep current): ").strip() or data.at[property_id, "House Type"]
            data.at[property_id, "Address"] = input("Enter new Address (leave blank to keep current): ").strip() or data.at[property_id, "Address"]
            data.at[property_id, "BHK Type"] = input("Enter new BHK Type (leave blank to keep current): ").strip() or data.at[property_id, "BHK Type"]
            data.at[property_id, "Garage Included"] = input("Garage Included (yes/no, leave blank to keep current): ").strip().lower() or data.at[property_id, "Garage Included"]
            data.at[property_id, "Yard Available"] = input("Yard Available (yes/no, leave blank to keep current): ").strip().lower() or data.at[property_id, "Yard Available"]
            price_input = input("Enter new Price (leave blank to keep current): ").strip()
            data.at[property_id, "price"] = int(price_input) if price_input else data.at[property_id, "price"]

            data.to_csv("real_estate_data.csv", index=False)
            print("Property updated successfully.")
        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except ValueError:
            print("Invalid input for property ID or price. Please enter numbers only.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def deleteProperty(self):
        print("\n---- Deleting Property ----")
        try:
            data = pd.read_csv("real_estate_data.csv")
            property_id = int(input("Enter the row number of the property you want to delete: "))

            if property_id >= len(data) or property_id < 0:
                print("Property ID does not exist.")
                return

            data = data.drop(property_id).reset_index(drop=True)
            data.to_csv("real_estate_data.csv", index=False)
            print("Property deleted successfully.")
        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except ValueError:
            print("Invalid input for property ID. Please enter a valid number.")
        except Exception as e:
            print(f"An error occurred: {e}")
