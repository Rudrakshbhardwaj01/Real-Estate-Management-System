import pandas as pd
from admin import Admin
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

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
            print("Press 6 to calculate the EMI payable for a chosen property.")
            print("Press 7 to generate a PDF report of a chosen property.")
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
            elif preference=="6":
                self.emiCalculator()
            elif preference=="7":
                self.downloadPropertyPDF()
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
    
    def emiCalculator(self):
        try:
            data = pd.read_csv("real_estate_data.csv")
            print("Available properties:")
            print(data)

            property_id_input = input("Enter the row number of the property to calculate EMI (1-based index): ")

            try:
                property_id = int(property_id_input) - 1
            except ValueError:
                print("Invalid input. Please enter a valid integer for the property ID.")
                return

            if property_id < 0 or property_id >= len(data):
                print("Invalid property ID. Please select a number from the list shown.")
                return

            price = data.iloc[property_id]["price"]
            print(f"Selected Property Price: {price}")

            loan_term = input("Choose loan term in years (4, 6, or 8): ").strip()
            if loan_term == "4":
                interest_rate = 5 / 100
                months = 4 * 12
            elif loan_term == "6":
                interest_rate = 7 / 100
                months = 6 * 12
            elif loan_term == "8":
                interest_rate = 9 / 100
                months = 8 * 12
            else:
                print("Invalid loan term. Choose 4, 6, or 8 years.")
                return

            monthly_interest_rate = interest_rate / 12
            emi = (price * monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)
            print(f"Monthly EMI for {loan_term} years at an interest rate of {interest_rate * 100}%: {emi:.2f}")

            balances = []
            remaining_balance = price

            for month in range(1, months + 1):
                interest_for_month = remaining_balance * monthly_interest_rate
                principal_for_month = emi - interest_for_month
                remaining_balance -= principal_for_month
                balances.append(remaining_balance)

            plt.figure(figsize=(10, 6))
            plt.plot(range(1, months + 1), balances, label="Remaining Loan Balance", color="blue")
            plt.title("Loan Balance Over Time")
            plt.xlabel("Months")
            plt.ylabel("Remaining Balance")
            plt.legend()
            plt.grid()
            plt.show()

        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")

    def downloadPropertyPDF(self):
        try:
            data = pd.read_csv("real_estate_data.csv")
            print("Available properties:")
            print(data)

            property_id_input = input("Enter the row number of the property to download information as PDF (1-based index): ")

            try:
                property_id = int(property_id_input) - 1
            except ValueError:
                print("Invalid input. Please enter a valid integer for the property ID.")
                return

            if property_id < 0 or property_id >= len(data):
                print("Invalid property ID. Please select a number from the list shown.")
                return

            property_details = data.iloc[property_id]
            price = property_details["price"]
            address = property_details["Address"]
            house_type = property_details["House Type"]
            bhk_type = property_details["BHK Type"]
            garage = property_details["Garage Included"]
            yard = property_details["Yard Available"]

            loan_term = input("Choose loan term in years (4, 6, or 8): ").strip()
            if loan_term == "4":
                interest_rate = 5 / 100
                months = 4 * 12
            elif loan_term == "6":
                interest_rate = 7 / 100
                months = 6 * 12
            elif loan_term == "8":
                interest_rate = 9 / 100
                months = 8 * 12
            else:
                print("Invalid loan term. Choose 4, 6, or 8 years.")
                return

            monthly_interest_rate = interest_rate / 12
            emi = (price * monthly_interest_rate * (1 + monthly_interest_rate) ** months) / ((1 + monthly_interest_rate) ** months - 1)

            pdf_file = f"Property_{property_id + 1}_Details.pdf"
            pdf = canvas.Canvas(pdf_file, pagesize=A4)
            pdf.setTitle(f"Property {property_id + 1} Details")

            pdf.drawString(100, 800, "Property Details")
            pdf.drawString(100, 780, f"Address: {address}")
            pdf.drawString(100, 760, f"House Type: {house_type}")
            pdf.drawString(100, 740, f"BHK Type: {bhk_type}")
            pdf.drawString(100, 720, f"Garage Included: {garage}")
            pdf.drawString(100, 700, f"Yard Available: {yard}")
            pdf.drawString(100, 680, f"Price: {price}")
            pdf.drawString(100, 640, "EMI Details")
            pdf.drawString(100, 620, f"Loan Term: {loan_term} years")
            pdf.drawString(100, 600, f"Interest Rate: {interest_rate * 100}%")
            pdf.drawString(100, 580, f"Monthly EMI: {emi:.2f}")

            pdf.save()
            print(f"PDF generated successfully: {pdf_file}")

        except FileNotFoundError:
            print("The file 'real_estate_data.csv' was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
