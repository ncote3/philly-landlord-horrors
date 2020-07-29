import json
from tqdm import tqdm

# Removes and entry from landlords_and_properties.json
# Example usage can be found in main()


def remove_entry(source, entry_to_remove):
    data = json.load(open(source))
    data.pop(entry_to_remove)
    json.dump(data, open(source, 'w'))

# Removes an entry from significant_landlords.json & significant_sorted_landlords.json
# Example usage can be found in  main()


def remove_significant_landlord(source, entry_to_remove):
    data = json.load(open(source))
    for sig_landlord in tqdm(data):
        if sig_landlord[0] == entry_to_remove:
            data.remove(sig_landlord)
    json.dump(data, open(source, 'w'))


def print_property_addresses_by_owner(source, owner_string):
    data = json.load(open(source))
    for owner in data:
        if owner_string == owner:
            for property in data[owner]["properties"]:
                print(property)


def main():
    # remove_entry('./data_sets/landlords_and_properties.json', "PHILADELPHIA HOUSING AUTH")
    # remove_significant_landlord('./data_sets/significant_sorted_landlords.json', "PHILADELPHIA HOUSING AUTH")
    print_property_addresses_by_owner('./data_sets/landlords_and_properties.json', 'JAMISON ROAD ASSOC')


main()
