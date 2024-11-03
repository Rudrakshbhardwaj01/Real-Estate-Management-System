import pandas as pd
from admin import Admin

class Client:
    def __init__(self):
        self.clientMenu()

    def clientMenu(self):
        while True:
            print("Press 1 to view a specific number of properties.")
            print("Press 2 to search for properties on the basis of specific attributes.")
            print("Press 3 to sort the properties on the basis of their prices (ascending/descending).")
            print("Press 4 to sort the properties on the basis of their total rooms [BHK] (ascending/descending).")
            print("Press 5 to book a property.")
            print("Enter 'back' to go back to the main menu.")
            print("Enter 'exit' to close the system.")

            preference = input("Enter your choice: ").lower()
            if preference == "1":
                Admin.readProperties()
            elif preference == "2":
                self.searchProperties()
            elif preference == "3":
                self.sortByPrice()
            elif preference == "4":
                self.sortByBHK()
            elif preference == '5':
                self.bookProperty()
            elif preference == 'back':
                from system import System
                System()
            elif preference == 'exit':
                exit()
            else:
                print("Invalid choice! Enter again!")
                self.clientMenu()

            continue_choice = input("Do you want to continue using the client menu? (yes/no): ").lower()
            if continue_choice == 'no':
                print("Exiting client menu.")
                break
            elif continue_choice != 'yes':
                print("Invalid choice! Please enter 'yes' or 'no'.")

    def searchProperties(self):
        print("\n---- Search Properties ----")
        try:
            data = pd.read_csv("real_estate_data.csv")

            house_type = input("Enter House Type (leave blank if not specified): ").strip()
            address = input("Enter Address (leave blank if not specified): ").strip()
            bhk_type = input("Enter BHK Type (leave blank if not specified): ").strip()
            garage_included = input("Garage Included (yes/no or leave blank): ").strip().lower()
            yard_available = input("Yard Available (yes/no or leave blank): ").strip().lower()

            min_price_input = input("Enter minimum price (or leave blank if not specified): ").strip()
            max_price_input = input("Enter maximum price (or leave blank if not specified): ").strip()
            
            min_price = int(min_price_input) if min_price_input else None
            max_price = int(max_price_input) if max_price_input else None
            
            filtered_data = data
            if house_type:
                filtered_data = filtered_data[filtered_data['House Type'].str.contains(house_type, case=False, na=False)]
            if address:
                filtered_data = filtered_data[filtered_data['Address'].str.contains(address, case=False, na=False)]
            if bhk_type:
                filtered_data = filtered_data[filtered_data['BHK Type'].str.contains(bhk_type, case=False, na=False)]
            if garage_included in ["yes", "no", ""]:
                filtered_data = filtered_data[filtered_data['Garage Included'].str.lower() == garage_included]
            if yard_available in ["yes", "no", ""]:
                filtered_data = filtered_data[filtered_data['Yard Available'].str.lower() == yard_available]
            
            if min_price is not None:
                filtered_data = filtered_data[filtered_data['price'] >= min_price]
            if max_price is not None:
                filtered_data = filtered_data[filtered_data['price'] <= max_price]

            if not filtered_data.empty:
                print(filtered_data)
            else:
                print("No properties found matching your criteria.")

        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except ValueError:
            print("Invalid input for price. Please enter numbers only.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def sortByPrice(self):
        print("\n---- Sorting by Price ----")
        try:
            order = input("Enter 'asc' for ascending order or 'desc' for descending order: ").strip().lower()
            data = pd.read_csv("real_estate_data.csv")
            
            if order == 'asc':
                sorted_data = data.sort_values(by='price', ascending=True)
            elif order == 'desc':
                sorted_data = data.sort_values(by='price', ascending=False)
            else:
                print("Invalid input. Please enter 'asc' or 'desc'.")
                return
            
            print(sorted_data)
        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def sortByBHK(self):
        print("\n---- Sorting by BHK ----")
        try:
            order = input("Enter 'asc' for ascending order or 'desc' for descending order: ").strip().lower()
            data = pd.read_csv("real_estate_data.csv")
            
            if order == 'asc':
                sorted_data = data.sort_values(by='BHK Type', ascending=True)
            elif order == 'desc':
                sorted_data = data.sort_values(by='BHK Type', ascending=False)
            else:
                print("Invalid input. Please enter 'asc' or 'desc'.")
                return
            
            print(sorted_data)
        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def bookProperty(self):
        print("\n---- Booking Property ----")
        try:
            data = pd.read_csv("real_estate_data.csv")
            print("Available properties to book:")
            print(data)

            property_id_input = input("Enter the row number of the property you want to book (1-based index): ")

            try:
                property_id = int(property_id_input) - 1
            except ValueError:
                print("Invalid input. Please enter a valid integer for the property ID.")
                return

            if property_id < 0 or property_id >= len(data):
                print("Invalid property ID. Please select a number from the list shown.")
                return

            client_name = input("Enter your name: ").strip()
            client_contact = input("Enter your contact number: ").strip()

            booking_details = {
                "Property ID": property_id + 1,
                "House Type": data.iloc[property_id]["House Type"],
                "Address": data.iloc[property_id]["Address"],
                "BHK Type": data.iloc[property_id]["BHK Type"],
                "Garage Included": data.iloc[property_id]["Garage Included"],
                "Yard Available": data.iloc[property_id]["Yard Available"],
                "Price": data.iloc[property_id]["price"],
                "Client Name": client_name,
                "Client Contact": client_contact
            }

            try:
                bookings = pd.read_csv("booking.csv")
            except FileNotFoundError:
                bookings = pd.DataFrame(columns=booking_details.keys())
            except pd.errors.EmptyDataError:
                bookings = pd.DataFrame(columns=booking_details.keys())

            new_booking_df = pd.DataFrame([booking_details])

            bookings = pd.concat([bookings, new_booking_df], ignore_index=True)

            bookings.to_csv("booking.csv", index=False)
            print("Property booked successfully.")
            
        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
