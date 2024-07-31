import habfunctions as hab

hab.update_hab_defaults(50, 200)

new_default_values_tuple = hab.read_hab_defaults()

print("New values in the defaults file:")
for value in new_default_values_tuple:
    print(value)

exit(0)
