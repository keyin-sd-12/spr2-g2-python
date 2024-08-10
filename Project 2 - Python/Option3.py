#Description: Code for option 3: Enter Company Expenses.
#Name: Jennifer Lyver
#date: August 9, 2024 - August 10, 2024

#imports:
from datetime import datetime
import FormatValues as FV

#definitions
def Val_YN(string):
    string = string.upper().strip()
    if string == "YES" or string == "Y":
        val = True
        if_yes = True
    elif string == "NO" or string == "N":
        val = True
        if_yes = False
    else:
        val = False
    return val, if_yes

def read_maintenance():
    with open("Project 2 - Python/Maintenance.dat", "r") as f:
        global Maintenance_ID
        maintenance_list = f.read().split("\n")
        Maintenance_ID = maintenance_list[-1]
        Maintenance_ID = Maintenance_ID.split(",")
        Maintenance_ID = int(Maintenance_ID[0])+1
        
def get_invoicenumber(run):
    if run == "1": #if maintence this is a maintence invoice:
        global one_invoice
        print("\n    Does the invoice contain only one expense? ")
        while True: #checking if there is only one invoice for the maintence expense
            one_invoice = input("\n    Y or N: ")
            val, one_invoice = Val_YN(one_invoice)
            if not val:
                print("Invalid input. Please enter Y or N.")
            else:
                break
        if not one_invoice:
            print("\nThe invoice must also be submittded under option 2.")
        else: print("\nThe invoice will also be saved into the expense table.")
    else:
        one_invoice = True
    while True:
        unique = True
        Invoice_ID = input("\nInvoice Number: ")
        Invoice_ID.replace(",", "|") #won't change the abilty to read the file if commas are in the invoice number.
        if one_invoice:
            with open ("Project 2 - Python/Expenses.dat", "r") as f:
                expense_line = f.readline()
                for line in expense_line:
                    line = line.split(",")
                    if line[0] == Invoice_ID:
                        Unique = True
                        print("\nInvoice Number already exists. Please enter a different Invoice Number.")
                        break
        if unique:
            break
    return Invoice_ID
def get_date(prompt):
    print("Date format: YYYY-MM-DD")
    date = input(f"{prompt}: ").strip().split("-")
    while len(date[0]) != 4 or len(date[1]) != 2 or len(date[2]) != 2:
        print("\nInvalid date format. Please enter the date in the correct format.")
        date = input(f"{prompt}: ").strip().split("/")
    try:
        date_obj = datetime.strptime(f"{date[0]}-{date[1]}-{date[2]}", "%Y-%m-%d")
        date = FV.FDateS(date_obj)
        return date
    except ValueError:
        print("\nInvalid date. Please enter a valid date.")
        return get_date(prompt)
    
def get_money(prompt):
    error_message = "\nInvalid input. Please enter a valid amount of money."
    while True:
        try:
            money = float(input(prompt))
        except ValueError:
            print(error_message)
        if money >= 0:
            break
        else:
            print(error_message)
    return money
     

def main():
    while True:
        print("""        Expense Menu:
            
            1. Enter Maintenance Expense.
            2. Enter Other Expense.
            3. Return to Main Menu.
            """)
        run = input("\n    Enter Choice: ")
        if not run.isdigit(): #if input is not a number
            print("\nInvalid input. Please enter a valid number.\n")
        elif run == "1" or run == "2": 
            #Maintenance Expense
            Invoice_ID = get_invoicenumber(run)
            Invoice_date = get_date("\n    Invoice Date")
            #Driver_ID
            if one_invoice:
                while True:
                    Driver_ID = input("\n    Driver Number: ")
                    if not Driver_ID.isdigit():
                        print("\nInvalid Driver ID. Please enter a valid Driver ID.")
                    else:
                        break
                Subtotal = get_money("\n    Subtotal: ")
                HST = get_money("\n    HST: ")
            Total = get_money("\n    Total: ")
            #write to expense file
            if one_invoice:
                with open ("Project 2 - Python/Expenses.dat", "a") as f:
                    f.write(f"\n{Invoice_ID},{Invoice_date},{Driver_ID},{Subtotal},{HST},{Total}")
            if run ==1:
                read_maintenance()
                Maintenance_date = get_date("\n    Maintenance Date: ")
                Maintenance_description = input("\n    Descitpion of Maintenance: ")
                Maintenance_description.replace(",", "|") #won't change the abilty to read the file if commas are in the descritpion.
                while True:
                    Car_ID = input("\n    Car ID: ")
                    if Car_ID.isdigit():
                        break
                    else:
                        print("\nInvalid Car ID. Please enter a valid Car ID.")
                with open("\nProject 2 - Python/Maintenance.dat", "a") as f:
                    f.write(f"\n{Maintenance_ID},{Invoice_ID},{Car_ID},{Maintenance_date},{Maintenance_description},{Total}")

        elif run == "3": 
            #Return to Main Menu
            break
        else:
            print("Invalid option. Please enter 1, 2 or 3\n")
        
    
        
    
    
#6001,1001,1918,2022-04-01,Oil Change,50.00,7.50,57.50


if __name__ == "__main__":
    main()