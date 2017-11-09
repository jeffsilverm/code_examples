

import pycountry

with open("/usr/share/applications/libreoffice-calc.desktop", "r") as f:
    contents=f.readlines()
for l in contents:
    if "Name[" not in l:
        continue
    if "GenericName" in l:
        continue
    try:
        ( name, new_spreadsheet ) =l.split("=")
    except ValueError as v:
        continue
    # Some country codes are longer than 2 letters
    right_bracket_idx = name.find("]")
    country_code=name[5:right_bracket_idx]
    try:
        country_name = pycountry.countries.lookup(country_code)
        print(f"{country_code}\t{country_name.name}\t{new_spreadsheet[:-1]}")
    except LookupError as lue:
        print(f"{country_code}\tUNKNOWN\t{new_spreadsheet[:-1]}")






