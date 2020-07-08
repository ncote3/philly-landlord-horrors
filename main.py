import csv
from tqdm import tqdm
import json
from statistics import mean, median, mode

def landlord_count(source, output):
    landlords = {}

    with open(source, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in tqdm(csv_reader, total=581456):
            if line_count == 0:
                line_count += 1
            if row["owner_1"] not in landlords.keys():
                landlords[row["owner_1"].strip()] = 1
                line_count += 1
            else:
                try:
                    landlord_prop_count = landlords[row["owner_1"].strip()]
                    landlords[row["owner_1"].strip()] = landlord_prop_count + 1
                except:
                    print(row["owner_1"].strip(), "is missing a count.")
                line_count += 1

    landlord_count = len(landlords)
    print("There are ", line_count, "properties in this data set.")
    print("There are ", landlord_count, "unique owner_1's.")
    print("That's ", line_count/landlord_count, "properties per landlord!")
    print("Mean Properties Owned: ", mean(landlords.values()))
    print("Median Properties Owned: ", median(landlords.values()))
    print("Mode Properties Owned: ", mode(landlords.values()))

    sorted_landlords = sorted(landlords.items(), key=lambda x: x[1], reverse=True)
    with open(output, 'w') as file:
        file.write(json.dumps(sorted_landlords))

def json_creator(source, output):
    data = {}

    with open(source, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in tqdm(csv_reader, total=581456):
            if line_count == 0:
                line_count += 1
            if row["owner_1"].strip() not in data.keys():
                data[row["owner_1"].strip()] = {
                    'total_properties': 1,
                    'properties': [row['location'].strip()]
                }
                line_count += 1
            else:
                properties = data[row['owner_1'].strip()]['properties']
                properties.append(row['location'].strip())
                data[row['owner_1'].strip()]['properties'] = properties
                total_properties = data[row['owner_1'].strip()]['total_properties'] + 1
                data[row['owner_1'].strip()]['total_properties'] = total_properties

                line_count += 1
        with open(output, 'w') as file:
            file.write(json.dumps(data))

def main():
#     landlord_count('opa_properties_public.csv', 'unique_landlords.json')
    json_creator('opa_properties_public.csv', 'landlords_and_properties.json')

main()