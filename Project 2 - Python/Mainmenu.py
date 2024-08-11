#Description: Main menu to run other sprint programs
#name: Jennifer Lyver
#date: June 30, 2024
#EDIT - EK August 11, 2024 - Added abilty to update stand fees automatically.
#EDIT - JL August 11, 2024 - Adjusted Filepaths due to feedback - will no longer run with github desktop.
#EDIT - JL August 11, 2024 - Adjusted code as it no longer needs to find absolute filepath.

#imports
import os 
import habfunctions #added 2024-08-11

#definitions
def run_main(pythonfile):
    module = __import__(f"Option{run}")
    module.main() #runs the python file
    
indent = " "*4

# added 2024-08-11
# code to run everytime the program is started
# automatic updates of stand fees on the first of the month
habfunctions.update_stand_fees()

#main program loop
while True:
    # main menu print
    print('''\n
    Main Menu:
        1. Enter a new employee (driver).
        2. Enter Company Revenues.
        3. Enter Company Expenses.
        4. Track Car Rentals.
        5. Record Employee Payment.
        6. Print Company Profit Listing.
        7. Print Driver Financial Listing.
        8. Corperate Summary Report.
        9. Quit Program.
      ''')
    errormessage = '\n\n   Input Error: Please enter number between 1-9\n'
    while True:
        try:
            run = int(input('   Enter Choice: '))
            if run < 1 or run > 9:
                print(errormessage)
            else:break
        except:
            print(errormessage)
    if run <= 8:
        print('\n\n')
        run_main(f'Option{run}')
    else:
        print(f'\n{indent*2}Thank you for using our program!')
        break

