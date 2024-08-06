#Description: Print Company Profit Listing for HAB Taxi Services Company Services System
#Name: Melanie Adams
#Date: Aug 05 24

# Imports
from datetime import datetime

# Constants
import FormatValues as FV

# Gather inputs
start_date = datetime.strptime(input("Enter the start date (YYYY-MM-DD): "), '%Y-%m-%d')
end_date = datetime.strptime(input("Enter the end date (YYYY-MM-DD): "), '%Y-%m-%d')
start_dateDSP = start_date.strftime('%Y-%m-%d')
end_dateDSP = end_date.strftime('%Y-%m-%d')

# Main Program
def main():

    total_expenses = 0
    # Open the expense file for reading 
    f = open('Expenses.dat', 'r')
    
    # Read the record
    for expense in f:
        expense_list = expense.split(',')
        expense_date = datetime.strptime(expense_list[1].strip(), '%Y-%m-%d')  # Adjust the index based on your file format
        if start_date <= expense_date <= end_date:
            expense_amount = float(expense_list[10].strip())
            # Add the expense amount to the total expenses
            total_expenses += expense_amount
    # Close the file
    f.close()

    total_revenue = 0 
    # Open the revenue file for reading
    f = open('Revenue.dat', 'r')
    
    # Read the record
    for revenue in f:
        revenue_list = revenue.split(',')
        revenue_date = datetime.strptime(revenue_list[1].strip(), '%Y-%m-%d')  # Adjust the index based on your file format
        if start_date <= revenue_date <= end_date:
            revenue_amount = float(revenue_list[6].strip())
            # Add the revenue amount to the total revenues
            total_revenue += revenue_amount

    # Close the file
    f.close()  

    profit = total_revenue - total_expenses

    # Display the results
    print()
    print(f" " * 36 + f"(709) 555-1234") 
    print(f" " * 23 + f"-" * 40) 
    print(f" " * 33 + f"PROFIT LISTING REPORT") 
    print( )
    print(f" " * 24 + f"From: " + str(start_dateDSP) + f" " * 8 + f"To: " + str(end_dateDSP))
    print(f" " * 23 + f"-" * 40) 
    print(f" " * 23 + f"Total Revenues:" + f" " * 15 + f"{FV.FDollar2(total_revenue):>10s}")
    print(f" " * 23 + f"Total Expenses:" + f" " * 15 + f"{FV.FDollar2(total_expenses):>10s}")
    print(f" " * 23 + f"-" * 40) 
    print(f" " * 23 + f"Profit  (Loss):" + f" " * 15 + f"{FV.FDollar2(profit):>10s}")
    print(f" " * 23 + f"-" * 40) 
    print(f" " * 31 + f"Thank you! Have a nice day!") 
    print(f" " * 23 + f"-" * 40) 
    print()
    print()

#  testing main menu
if __name__ == "__main__":
    main()