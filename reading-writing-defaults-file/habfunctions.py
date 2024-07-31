import os, shutil, atexit, signal

# file open modes
READMODE = "r"
WRITEMODE = "w"
NEWLINE = "\n"
CSVSEPARATOR = ","

# display debug messages, such as which files are closed, etc. For production set to False
DEBUGMESSAGES = True

# names of the files used in the program
DEFAULTSFILENAME = "Defaults.dat"

# list of open files, used for cleanup at exit
# every file that is opened should be added to this list via .append() method
# exit cleanup function will go through this list and close all files that are still open
global_list_of_open_files = []

# file cleanup function, it goes through the list of previously opened files and closes them (if they are not already closed)
def create_file_cleanup(list_of_files=global_list_of_open_files):
    def file_cleanup():
        if DEBUGMESSAGES: print(NEWLINE+"*** Exiting and closing files ***")
        processed_names = []
        for f in reversed(list_of_files):
            file_message = f"    File '{f.name}' "
            if not f.closed:
                f.close()
                file_message += "closed successfully"
            else:
                file_message += "was already closed"
                
            if f.name not in processed_names:
                if DEBUGMESSAGES: print(file_message)
                processed_names.append(f.name)    

        if DEBUGMESSAGES: print("*** Done closing files ***"+NEWLINE)
        list_of_files.clear()        
    return file_cleanup

# handle Ctrl-C signal
def handle_ctrl_c(signum, frame):
    print("\n\n"+"===== Ctrl-C is detected, exiting gracefully =====")
    exit(100)

# print IOError message and exit
def process_io_error(e):
    print(f"\nOS Error {e.errno}: {e.strerror} - '{e.filename}'")
    exit(e.errno)

# reads the settings file and returns the values 
def read_hab_defaults(defaults_filename=DEFAULTSFILENAME, field_separator=CSVSEPARATOR, list_of_files=global_list_of_open_files):
    
    # create a list of default values, second index is the data type
    default_values = [ [None] * 6, [int, int, float, float, float, float] ]
       
    # open the defaults file for reading
    defaults_file_object = open_file(defaults_filename)
   
    # read the first line from the defaults file
    line_string = defaults_file_object.readline().strip()
    
    # close the defaults file
    defaults_file_object.close()    
   
    # split line into fields
    splitted_line = line_string.split(field_separator)
    if (len(splitted_line) != 6):
        print(f"ERROR! Wrong file format, must be 6 values, separated be {field_separator}\n       (file '{defaults_filename}', line 1)")
        exit(-1)
    
    for i in range(len(splitted_line)):
        try:
            # check if the value can be converted to the required data type
            default_values[0][i] = default_values[1][i](splitted_line[i].strip())
        except ValueError:
            print(f"ERROR! Value '{splitted_line[i].strip()}' must be {str(default_values[1][i])}\n       (file '{defaults_filename}', line 1)")
            exit(-1)

    return tuple(default_values[0])

# update the settings file with new values of next transaction number and next driver number
def update_hab_defaults(next_transaction_number, next_driver_number, defaults_filename=DEFAULTSFILENAME, field_separator=CSVSEPARATOR, list_of_files=global_list_of_open_files):
    
    # create backup of the defaults file
    backup_filename = os.path.splitext(defaults_filename)[0] + ".bak"
    
    copy_file(defaults_filename, backup_filename)
           
    # open the defaults file for reading
    defaults_file_object = open_file(defaults_filename)

    # read the first line from the defaults file
    line_splitted = defaults_file_object.readline().strip().split(field_separator)

    # strip the values of leading and trailing spaces
    line_splitted = [element.strip() for element in line_splitted]
        
    # close the defaults file
    defaults_file_object.close()
    
    # replace the first two values with new values    
    line_splitted[0] = str(next_transaction_number)
    line_splitted[1] = str(next_driver_number)
    
    new_line = ', '.join(line_splitted)
    
    # open the defaults file for writing
    defaults_file_object = open_file(defaults_filename, WRITEMODE)
    
    # write the new line to the defaults file
    defaults_file_object.write(new_line)
    defaults_file_object.flush()
    defaults_file_object.close()
    
    # delete the backup file
    delete_file(backup_filename)

# open file for reading or writing, handle exceptions
# add file object to the list of open files
def open_file(file_name, mode=READMODE, list_of_files=global_list_of_open_files):
    try:
        file_object = open(file_name, mode)
    except OSError as e:
        process_io_error(e)
    list_of_files.append(file_object)    
    return file_object

def write_sting_to_file(file_object, write_string, flush_file=True):
    try:
        file_object.write(write_string)
    except OSError as e:
        process_io_error(e)
    try:
        if flush_file: file_object.flush()
    except OSError as e:
        process_io_error(e)
    return 0    

# copy file to another file
# good idea to create a backup of the file before overwriting it
def copy_file(file_name, copy_file_name):
    if os.path.isfile(file_name):
        try:
            shutil.copy(file_name, copy_file_name)  # Corrected parameter name
        except IOError as e:
            process_io_error(e)

# delete file 
# after the file was sucessfully writter, we can deleter the backup file
def delete_file(file_name):
    if os.path.isfile(file_name):
        try:
            os.remove(file_name)
        except IOError as e:
            process_io_error(e)

# register file cleanup function to run at exit, so that all files are closed if program
atexit.register(create_file_cleanup(global_list_of_open_files))

# want to catch Ctrl-C exception, so the files are closed properly
# (ideally, would catch all exceptions, but that's a bit more involved)
signal.signal(signal.SIGINT, handle_ctrl_c)
# alternatively, Ctrl-C can be disabled:
#signal.signal(signal.SIGINT, signal.SIG_IGN)
