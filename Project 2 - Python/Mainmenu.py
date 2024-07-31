#Description: Main menu to run other sprint programs
#name: Jennifer Lyver
#date: June 30, 2024


#imports
import os 

#definitions
def run_main(pythonfile):
    # Get the absolute path of the script
    script_path = os.path.abspath(__file__)
    # Extract the directory path
    script_dir = os.path.dirname(script_path)
    # Construct the full path to the module
    module_path = os.path.join(script_dir, f"{pythonfile}.py")
    # Import the module
    module = __import__(f"{pythonfile}")
    # Call the main function of the module
    module.main()
    
indent = " "*4

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

