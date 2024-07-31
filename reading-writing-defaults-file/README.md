Here is `habfunctions.py` I modified from the previous homework.

It includes the two methods we can use in each menu option: 
reading `Defaults.dat` file, and updating two first values in it.

Example usage of these methods are given in 
`example-update_defaults_file.py` and `example-read_defaults_file.py`

Also, it maybe an overkill, but if there is any file operation in the code, I usually intercept exit procedure,
so when the program ends (by any way: normally, by `Ctrl+C` in Windows or `OPTION + .` on MAC, or by any other runtime error) exit procedure is executed and 
all the files which were open in the program are closed.

Everytime I open the file, I `.append()` the file object to the list of open files, and if the programs ends abruptly,
the exit procedure processes this list and close the files nicely, to prevent data loss.
