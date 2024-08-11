import os, shutil, signal, datetime

# file open modes
READMODE = "r"
WRITEMODE = "w"
APPENDMODE = "a"
NEWLINE = "\n"
CSVSEPARATOR = ","
FORMATYYYYMMDD = "%Y-%m-%d"
BACKUPFILEEXTENSION = "bak"
TMPFILEEXTENSION = "tmp"
TRUESTR = "True"
FALSESTR = "False"

# display debug messages, such as which files are closed, etc. For production set to False
DEBUGMESSAGES = False

# delete backup files after successful update (recommended to set to False, backups are important)
DELETEBACKUPS = True

# NUMBER OF FIELDS IN THE DEFAULTS FILE RECORD
DEFAULTSFILEFIELDS = 6

# names of the files used in the program
DEFAULTSFILENAME = "Defaults.dat"
REVENUEFILENAME = "Revenue.dat"
EMPLOYEEFILENAME = "Employee.dat"

MONTHLYSTANDSTRING = "Monthly Stand Fees"

# converts YYYY-MM-DD to date and handles exceptions
def yyyymmdd(date_string):
    try:
        return datetime.datetime.strptime(date_string, FORMATYYYYMMDD).date()
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}")

# data types for each field in a record
FIELD_DATA_TYPES = {
    DEFAULTSFILENAME: [int, int, float, float, float, float], 
    EMPLOYEEFILENAME: [int, str, str, str, str, str, str, str, str, yyyymmdd, str, str, bool, float],
    REVENUEFILENAME:  [int, yyyymmdd, str, int, float, float, float]
}

# number of fields in a single record of each file
NUMBER_OF_FIELDS = {
    DEFAULTSFILENAME: len(FIELD_DATA_TYPES[DEFAULTSFILENAME]),
    EMPLOYEEFILENAME: len(FIELD_DATA_TYPES[EMPLOYEEFILENAME]),
    REVENUEFILENAME: len(FIELD_DATA_TYPES[REVENUEFILENAME])
}

REVENUE_DATE_INDEX = 1
REVENUE_DESCRIPTION_INDEX = 2
REVENUE_EMPLOYEE_ID_INDEX = 3
EMPLOYEE_OWN_CAR_INDEX = FIELD_DATA_TYPES[EMPLOYEEFILENAME].index(bool)
EMPLOYEE_BALANCE_DUE_INDEX = len(FIELD_DATA_TYPES[EMPLOYEEFILENAME]) - 1

# print IOError message and exit
def process_io_error(e):
    # print the error message
    print(f"{NEWLINE}OS Error {e.errno}: {e.strerror} - '{e.filename}'")
    # we have to exit the program (we cannot continue with IO error)
    exit(e.errno)

# converts the record from a data file to a list of values
# need to provide the type of the record (it is the name of the data file)
# by default it is the Defaults.dat file
# return a list of values is default (return_as_strings=False)
# return a list of strings is return_as_strings=True
def convert_record_to_data(record_string, type_of_record=DEFAULTSFILENAME, field_separator=CSVSEPARATOR, return_as_strings=False):
    splitted_line = record_string.strip().split(field_separator)
    fields = NUMBER_OF_FIELDS[type_of_record]

    # check if the number of values in the record is correct        
    if (len(splitted_line) != fields):
        print(f"ERROR! Wrong file format, must be {str(fields)} values, separated by '{field_separator}'\n       (file '{type_of_record}')")
        exit(-1)
        
    data_values = []

    # loop through all fields in the record    
    for i in range(fields):

        # value must be converted to the required data type
        data_type = FIELD_DATA_TYPES[type_of_record][i]
        
        try:
            splitted_line[i] = splitted_line[i].strip()
            # check if the value can be converted to the required data type
            if return_as_strings:
                data_values.append(splitted_line[i])
            else:
                if data_type is bool:
                    if splitted_line[i].lower() == TRUESTR.lower():
                        data_values.append(True)
                    elif splitted_line[i].lower() == FALSESTR.lower():
                        data_values.append(False)
                    else:
                        print(f"ERROR! Value '{splitted_line[i]}' must be 'True' or 'False'\n       (file '{type_of_record}'")
                        exit(-1)
                else:        
                    data_values.append(data_type(splitted_line[i]))        
        except ValueError:
            print(f"ERROR! Value '{splitted_line[i]}' must be '{str(data_type)}'\n       (file '{type_of_record}'")
            exit(-1)

    # return a list of values
    return data_values

# converts data values to a record for a data file, separated by field_separator
# if data_as_strings is True, then the values are already converted to strings
def convert_data_to_record(data_values, type_of_record=DEFAULTSFILENAME, field_separator=CSVSEPARATOR, data_as_strings=False):
    # number of field in data list received
    number_of_fields = len(data_values)
    # number of fields which must be in the record
    fields = len(FIELD_DATA_TYPES[type_of_record])
    # if they are not the same, then report an error
    if number_of_fields != fields:
        print(f"ERROR! Wrong number of values in the record, must be {fields}")
        return ""
    # if the data is already in string format, just join them with the field separator
    if data_as_strings:
        record_string = field_separator.join(data_values)
    else:
        # else convert the data to string and join them with the field separator
        string_data = []
        # loop over the data and their corresponding types
        for item, data_type in zip(data_values, FIELD_DATA_TYPES[type_of_record]):
            # if date object, format it as FORMATYYYYMMDD = "%Y-%m-%d"
            if data_type is yyyymmdd:
                string_data.append(item.strftime(FORMATYYYYMMDD))
            # If the item is a float, format it with 2 decimal places
            elif data_type is float:
                string_data.append("{:.2f}".format(item))
            # Otherwise, convert the item to a string
            else:
                string_data.append(str(item))
        record_string = field_separator.join(string_data)
    # return the record string
    return record_string

# reads the settings file and returns the values
# by default returns the values as a tuple, if return_values_as_tuple is False, returns as a list
def read_hab_defaults(defaults_filename=DEFAULTSFILENAME, field_separator=CSVSEPARATOR, return_values_as_tuple=True):
    # open the defaults file for reading
    defaults_file_object = open_file(defaults_filename)
    # read the first line from the defaults file
    line_string = read_line_from_file(defaults_file_object).strip()
    # close the defaults file
    defaults_file_object.close()    
    # get a list of values from the record
    default_values = convert_record_to_data(line_string, defaults_filename, field_separator)
    # return values as a tuple
    if return_values_as_tuple:
        return tuple(default_values)
    else:
        return default_values

# update the settings file with new values of next transaction number and next driver number
def update_hab_defaults(next_transaction_number, next_driver_number, defaults_filename=DEFAULTSFILENAME,field_separator=CSVSEPARATOR):
    
    # read the current values from the defaults file
    defaults_values = read_hab_defaults(defaults_filename, field_separator, False)
    defaults_values[0] = next_transaction_number
    defaults_values[1] = next_driver_number
    new_record = convert_data_to_record(defaults_values, defaults_filename, field_separator)
   
    # create temporary and backup file names
    tmp_filename = change_file_extension(defaults_filename, TMPFILEEXTENSION)
    backup_filename = change_file_extension(defaults_filename, BACKUPFILEEXTENSION)
   
    # open the temporaty file for writing
    tmp_file_object = open_file(tmp_filename, WRITEMODE)
    # write the new line to the tmp file
    write_line_to_file(tmp_file_object, new_record)
    # close the tmp file
    close_file(tmp_file_object)

    # rename the defaults file to the backup file
    rename_file(defaults_filename, backup_filename)

    # rename the tmp file to the defaults file
    rename_file(tmp_filename, defaults_filename)

    # delete the backup file
    if DELETEBACKUPS: delete_file(backup_filename)

# open file for reading or writing, handle exceptions
def open_file(file_name, mode=READMODE):
    try:
        file_object = open(file_name, mode)
    except OSError as e:
        process_io_error(e)
    return file_object

# read line from file, handle exceptions
def read_line_from_file(file_object, read_all_file=False):
    line = None
    try:
        if read_all_file:
            line = [record_line.strip() for record_line in file_object.readlines()]
            if not line: # if line is not an empty list or empty string raise OS error
                raise OSError(1, "Unexpected end of file ", file_object.name)
        else: 
            line = file_object.readline().strip()
    except OSError as e:
        process_io_error(e)
    return line

# write line to file, handle exceptions
def write_line_to_file(file_object, write_string, flush_file=True, start_new_line=False, end_new_line=True):
    try:
        if start_new_line:
            write_string = NEWLINE + write_string
        if end_new_line:
            write_string += NEWLINE    
        file_object.write(write_string)
    except OSError as e:
        process_io_error(e)
    try:
        if flush_file: file_object.flush()
    except OSError as e:
        process_io_error(e)

# copy file to another file
# (good idea to create a backup of the file before overwriting it)
def copy_file(file_name, copy_file_name):
    if os.path.isfile(file_name):
        try:
            shutil.copy(file_name, copy_file_name)
        except IOError as e:
            process_io_error(e)

# rename file and handle exceptions
def rename_file(file_name, new_file_name):
    if os.path.isfile(file_name):
        try:
            os.rename(file_name, new_file_name) 
        except IOError as e:
            process_io_error(e)

# delete file 
# (after the file was sucessfully written, we can delete the backup file)
def delete_file(file_name):
    if os.path.isfile(file_name):
        try:
            os.remove(file_name)
        except IOError as e:
            process_io_error(e)

# close file, handle exceptions            
def close_file(file_object):
    try:
        file_object.close()
    except OSError as e:
        process_io_error(e)
    return 0

# disable CTRL+C / COMMAND+C            
def disable_ctrl_c():
    signal.signal(signal.SIGINT, signal.SIG_IGN)

# enable CTRL+C / COMMAND+C    
def enable_ctrl_c():
    signal.signal(signal.SIGINT, signal.SIG_DFL)

def change_file_extension(file_name, new_extension):
    return os.path.splitext(file_name)[0] + '.' + new_extension

# get current date and return first day of the month
# as a string in format "YYYY-MM-01"
def get_first_day_of_month(date_object, return_as_string=False):
    # get the current date
    today = datetime.date.today()
    # Set the day to 1
    first_day = today.replace(day=1)
    # Format the date as "YYYY-MM-01"
    if return_as_string:
        return first_day.strftime(FORMATYYYYMMDD)
    else:
        return first_day


# function to update monthly stand fees automatically
# it should be called every time the main menu is displayed
def update_stand_fees():
    # read defaults file
    default_values_tuple = read_hab_defaults()

    next_transaction = default_values_tuple[0]
    next_driver = default_values_tuple[1]
    monthly_stand_fee = default_values_tuple[2]
    daily_rental_fee = default_values_tuple[3]
    weekly_rental_fee = default_values_tuple[4]
    hst_rate = default_values_tuple[5]

    if DEBUGMESSAGES: 
        print("the following values were read from the defaults file:")
        for value in default_values_tuple:
            print(value)
        print()    

    if DEBUGMESSAGES: print("employees:")
    employee_file_object = open_file(EMPLOYEEFILENAME)
    employee_records_str = read_line_from_file(employee_file_object, True)
    employee_records_data = []
    employees_with_own_car = []
    for record_str in employee_records_str:
        employee_data = convert_record_to_data(record_str, EMPLOYEEFILENAME, CSVSEPARATOR)    
        employee_records_data.append(employee_data)
        if employee_data[EMPLOYEE_OWN_CAR_INDEX]:
            employees_with_own_car.append(employee_data[0])
        if DEBUGMESSAGES: print(employee_data)
        
    close_file(employee_file_object)

    if DEBUGMESSAGES: 
        print(NEWLINE+"employees with own car:")
        for employee in employees_with_own_car:
            print('Employee #',employee)
        print()

    # get today's date, and first day of the month date object
    current_date_object = datetime.date.today()
    #first_day_of_the_month_object = datetime.date(current_date_object.year, current_date_object.month, 1)
    first_day_of_the_month_object = get_first_day_of_month(current_date_object)
    if DEBUGMESSAGES: print("current date is: ", current_date_object, " first day of month is: ", first_day_of_the_month_object)

    if DEBUGMESSAGES: print(NEWLINE+"revenues has the following records for monthly stand fees:")

    # open the revenues file for reading
    revenue_file_object = open_file(REVENUEFILENAME)

    # create empty sets for drivers to charge monthly stand fee, and drivers to exclude (already charged for this month)
    drivers_to_charge = set ()
    drivers_to_exclude = set ()

    # go through the revenues file and find out who needs to be charged for monthly stand fee for the current month
    # this is necessary because we do not want to charge the same employee twice for the same month, and for some
    # reason program may be run more than once on the first of the month, or another case is when the program is run
    # not on the first of the month, so the charges hasn't been made yet
    #
    # AND WE NEED to do this evey time the program is run (not only on the first of the month)
    #
    while True:
        
        # read the next record from the file
        revenue_record_str = read_line_from_file(revenue_file_object)
        # if end of file is reached, break the loop
        if not revenue_record_str:
            break
        
        # convert the record string to a list of data
        revenue_record_data = convert_record_to_data(revenue_record_str, REVENUEFILENAME, CSVSEPARATOR)
        
        # if the record is for monthly stand fee, process it
        if revenue_record_data[REVENUE_DESCRIPTION_INDEX] == MONTHLYSTANDSTRING:
            if DEBUGMESSAGES: print('revenue #', revenue_record_data[0], ' employee #', revenue_record_data[3], ' date: ', revenue_record_data[1])
            
            # if there is already a record for the current month, and employee is in employee list, then skip charging again
            employee_id = revenue_record_data[REVENUE_EMPLOYEE_ID_INDEX]
            if employee_id in employees_with_own_car:
                if revenue_record_data[REVENUE_DATE_INDEX] != first_day_of_the_month_object:
                    drivers_to_charge.add(employee_id)
                else:
                    drivers_to_exclude.add(employee_id)
                    if DEBUGMESSAGES: print(' '*14,'(employee #', revenue_record_data[REVENUE_EMPLOYEE_ID_INDEX], ' was already charged for this month)')

    # close the revenues file            
    close_file(revenue_file_object)

    drivers_to_charge = list(drivers_to_charge - drivers_to_exclude)
    if DEBUGMESSAGES: 
        print(NEWLINE+'drivers to be charged charged monthly stand fees', drivers_to_charge)
        print('--> drivers excluded (were already charged for this month):', drivers_to_exclude)

    # now will be updating records (adding new records to revenues file and changing balance due in the employee file)
    # in order not to lose data in case of an error, we will be using a temporary files for updating, then make backup copies, and

    # copy revenues file to a temporary file and open if in APPEND mode
    tmp_revenue_file_name = change_file_extension(REVENUEFILENAME, TMPFILEEXTENSION)
    backup_revenue_file_name = change_file_extension(REVENUEFILENAME, BACKUPFILEEXTENSION)
    copy_file(REVENUEFILENAME, tmp_revenue_file_name)
    tmp_revenue_file_object = open_file(tmp_revenue_file_name, APPENDMODE)

    tmp_employee_file_name = change_file_extension(EMPLOYEEFILENAME, TMPFILEEXTENSION)
    backup_employee_file_name = change_file_extension(EMPLOYEEFILENAME, BACKUPFILEEXTENSION)
    # open tmp employee file in WRITE mode
    tmp_employee_file_object = open_file(tmp_employee_file_name, WRITEMODE)

    for i in range(len(employee_records_data)):
        employee_no = employee_records_data[i][0]
        
        # update procedure - update balance due in the employee file, and add a new record to the revenues file
        if employee_no in drivers_to_charge:
            
            hst_amount = monthly_stand_fee * hst_rate
            total_amount = monthly_stand_fee + hst_amount
            
            # update the balance due in the employe's record
            employee_records_data[i][EMPLOYEE_BALANCE_DUE_INDEX] += total_amount
            
            # add a new record to the revenues file
            new_revenue_record = [ next_transaction, first_day_of_the_month_object, MONTHLYSTANDSTRING, employee_no, monthly_stand_fee, hst_amount, total_amount ]
            new_revenue_record_str = convert_data_to_record(new_revenue_record, REVENUEFILENAME)
            write_line_to_file(tmp_revenue_file_object, new_revenue_record_str)

            # increment the transaction number for the next revenue record
            next_transaction += 1
        
        new_employee_record_str = convert_data_to_record(employee_records_data[i], EMPLOYEEFILENAME)
        write_line_to_file(tmp_employee_file_object, new_employee_record_str)
        
    # all done, close the files
    close_file(tmp_employee_file_object)
    close_file(tmp_revenue_file_object)
    # rename the employee file to a backup file, and tmp employee file to the employee file
    rename_file(EMPLOYEEFILENAME, backup_employee_file_name)
    rename_file(tmp_employee_file_name, EMPLOYEEFILENAME)
    # rename the revenues file to a backup file, and tmp revenues file to the revenues file
    rename_file(REVENUEFILENAME, backup_revenue_file_name)
    rename_file(tmp_revenue_file_name, REVENUEFILENAME)
    # delete backup files
    if DELETEBACKUPS:
        delete_file(backup_employee_file_name)
        delete_file(backup_revenue_file_name)

    # need to update the default values file with the new transaction number
    update_hab_defaults(next_transaction, next_driver)

    # ALL DONE!
    # this function needs to be called every time the main menu is displayed!  


