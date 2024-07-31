import habfunctions as hab

default_values_tuple = hab.read_hab_defaults()

next_transaction = default_values_tuple[0]
next_driver = default_values_tuple[1]
monthly_stand_fee = default_values_tuple[2]
daily_rental_fee = default_values_tuple[3]
weekly_rental_fee = default_values_tuple[4]
hst_rate = default_values_tuple[5]

print("the following values were read from the defaults file:")
for value in default_values_tuple:
    print(value)

exit(0)