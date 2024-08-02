#Description: A program to generate a corporate summary report.
#Name: Me
#date: The date the program was written

# Imports:
import datetime
import FormatValues as FV

# Constants:
CUR_DATE = datetime.datetime.now()

# Main Progam:
__name__ = "__main__" # REMOVE WHEN DONE TESTING!! !!! !!! !!! !!!

def main():
    print()
   
   # Counters and Accumulators:
    OilExpenseCtr = 0
    OilExpenseAccu = 0
    BreakExpenseCtr = 0
    BreakExpenseAccu = 0
    EngineExpenseCtr = 0
    EngineExpenseAccu = 0
    TireExpenseCtr = 0
    TireExpenseAccu = 0
    BatteryExpenseCtr = 0
    BatteryExpenseAccu = 0
    WiperExpenseCtr = 0
    WiperExpenseAccu = 0
    TransExpenseCtr = 0
    TransExpenseAccu = 0
    HeadLightsExpenseCtr = 0
    HeadLightsExpenseAccu = 0
    AirExpenseCtr = 0
    AirExpenseAccu = 0
    FuelExpenseCtr = 0
    FuelExpenseAccu = 0
    ExpenseCtr = 0
    ExpenseAccu = 0
    ExpenseHSTAccu = 0
    
    MonthlyStandCtr = 0
    MonthlyStandAccu = 0
    WeeklyStandCtr = 0
    WeeklyStandAccu = 0
    DailyRentalCtr = 0
    DailyRentalAccu = 0
    RevenueCtr = 0
    RevenueAccu = 0
    RevenueHSTAccu = 0
    
    EmployeeCtr = 0
    EmployeeDuesCtr = 0
    EmployeeDuesAccu = 0
    EmployeeOwnerCtr = 0
    
    
    # Open the expense file for reading 
    f = open('Expenses.dat', 'r')
    
    # Read the record
    for Expense in f:
        ExpenseList = Expense.split(',')
        ExpenseType = ExpenseList[4].strip()
        ExpenseAmount = float(ExpenseList[10].strip())
        ExpenseHST = float(ExpenseList[9].strip())
        
        
    # Update the counters and accumulators
        if ExpenseType == 'Oil Change':
            OilExpenseCtr += 1
            OilExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Brake Pads':
            BreakExpenseCtr += 1
            BreakExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Engine Tune-up':
            EngineExpenseCtr += 1
            EngineExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Tire Replacement':
            TireExpenseCtr += 1
            TireExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Battery Replacement':
            BatteryExpenseCtr += 1
            BatteryExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Transmission Repair':
            TransExpenseCtr += 1
            TransExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Wiper Blades':
            WiperExpenseCtr += 1
            WiperExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Headlights':
            HeadLightsExpenseCtr += 1
            HeadLightsExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Air Filter':
            AirExpenseCtr += 1
            AirExpenseAccu += ExpenseAmount
        elif ExpenseType == 'Fuel Injection':
            FuelExpenseCtr += 1
            FuelExpenseAccu += ExpenseAmount
        else:
            print("Invalid Expense Type")
        
        ExpenseHSTAccu += ExpenseHST 
        ExpenseCtr += 1
        ExpenseAccu += ExpenseAmount
        
    # Close the file
    f.close()
    
    # Open the Revenue file for reading
    f = open('Revenue.dat', 'r')
    
    # Read the record
    for Revenue in f:
        RevenueList = Revenue.split(',')
        RevenueAmount = float(RevenueList[6].strip())
        RevenueType = RevenueList[2].strip()
        RevenueHST = float(RevenueList[5].strip())
        
        # Update the accumulators
        if RevenueType == 'Monthly Stand Fees':
            MonthlyStandCtr += 1
            MonthlyStandAccu += RevenueAmount
        elif RevenueType == 'Weekly Rental Fee':
            WeeklyStandCtr += 1
            WeeklyStandAccu += RevenueAmount
        elif RevenueType == 'Daily Rental Fee':
            DailyRentalCtr += 1
            DailyRentalAccu += RevenueAmount
        else:
            print("Invalid Revenue Type")
        
        RevenueHSTAccu += RevenueHST
        RevenueCtr += 1
        RevenueAccu += RevenueAmount
    
    # Close the file
    f.close()
    
    # Open the Employee file for reading
    f = open('Employee.dat', 'r')
    
    # Read the record
    for Employee in f:
        EmployeeList = Employee.split(',')
        EmployeeOwnership = EmployeeList[8].strip()
        EmployeeDues = float(EmployeeList[9].strip())
        
        # Update the accumulators
        if EmployeeDues > 0:
            EmployeeDuesCtr += 1
        if EmployeeOwnership == 'true':
            EmployeeOwnerCtr += 1
        elif EmployeeOwnership == 'false':
            # do nothing
            pass
        else:
            print("Invalid Employee Ownership")
            
        EmployeeCtr += 1
        EmployeeDuesAccu += EmployeeDues
        
    # Display the results
    print("                      ---------------------------------------------------------")
    print("                                         HAB TAXI SERVICES")
    print("                                         123 ANY STREET")
    print("                                         ST.John's, NL, A1A 1A1")
    print("                                         Phone: 709-555-1234")
    print("                              Corporate Summary Report as of ", CUR_DATE.strftime("%Y/%m/%d"))
    print("                      ---------------------------------------------------------")
    print("                                         Expenses Summary:")
    print()
    print(f"                      Oil Change:           {OilExpenseCtr:>3d} transactions for {FV.FDollar2(OilExpenseAccu):>10s}")
    print(f"                      Brake Pads:           {BreakExpenseCtr:>3d} transactions for {FV.FDollar2(BreakExpenseAccu):>10s}")
    print(f"                      Engine Tune-up:       {EngineExpenseCtr:>3d} transactions for {FV.FDollar2(EngineExpenseAccu):>10s}")
    print(f"                      Tire Replacement:     {TireExpenseCtr:>3d} transactions for {FV.FDollar2(TireExpenseAccu):>10s}")
    print(f"                      Battery Replacement:  {BatteryExpenseCtr:>3d} transactions for {FV.FDollar2(BatteryExpenseAccu):>10s}")
    print(f"                      Transmission Repair:  {TransExpenseCtr:>3d} transactions for {FV.FDollar2(TransExpenseAccu):>10s}")
    print(f"                      Wiper Blades:         {WiperExpenseCtr:>3d} transactions for {FV.FDollar2(WiperExpenseAccu):>10s}")
    print(f"                      Headlights:           {HeadLightsExpenseCtr:>3d} transactions for {FV.FDollar2(HeadLightsExpenseAccu):>10s}")
    print(f"                      Air Filter:           {AirExpenseCtr:>3d} transactions for {FV.FDollar2(AirExpenseAccu):>10s}")
    print(f"                      Fuel Injection:       {FuelExpenseCtr:>3d} transactions for {FV.FDollar2(FuelExpenseAccu):>10s}")
    print("                      ---------------------------------------------------------")
    print(f"                      Total HST:                                   {FV.FDollar2(ExpenseHSTAccu):>8s}")
    print(f"                      Total Expenses:       {ExpenseCtr:>3d} transactions for {FV.FDollar2(ExpenseAccu):>10s}")
    print()
    print("                      ---------------------------------------------------------")
    print("                                          Revenue Summary:")
    print()
    print(f"                      Monthly Stand:        {MonthlyStandCtr:>3d} transactions for {FV.FDollar2(MonthlyStandAccu):>10s}")
    print(f"                      Weekly Rental:        {WeeklyStandCtr:>3d} transactions for {FV.FDollar2(WeeklyStandAccu):>10s}")
    print(f"                      Daily Rental:         {DailyRentalCtr:>3d} transactions for {FV.FDollar2(DailyRentalAccu):>10s}")
    print("                      ---------------------------------------------------------")
    print(f"                      Total HST:                                   {FV.FDollar2(RevenueHSTAccu):>8s}")
    print(f"                      Total Revenue:        {RevenueCtr:>3d} transactions for {FV.FDollar2(RevenueAccu):>10s}")
    print()
    print("                      ---------------------------------------------------------")
    print("                                          Employee Summary:")
    print()
    print(f"                      Total Employees:      {EmployeeCtr:>3d}")
    print(f"                      Employees that rent:  {EmployeeCtr - EmployeeOwnerCtr:>3d}")
    print(f"                      Employees that own:   {EmployeeOwnerCtr:>3d}")
    print(f"                      Employee Dues:        {EmployeeDuesCtr:>3d} employees owe us {FV.FDollar2(EmployeeDuesAccu):>9s}")
    print()
    print("                      ---------------------------------------------------------")
    
if __name__ == "__main__":
    main()
