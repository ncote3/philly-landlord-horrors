import csv
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
import numpy as np

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
                    'properties': [row['location'].strip()],
                    'prop_coords': [[row['lat'].strip(), row['lng'].strip()]]
                }
                line_count += 1
            else:
                properties = data[row['owner_1'].strip()]['properties']
                properties.append(row['location'].strip())
                data[row['owner_1'].strip()]['properties'] = properties
                total_properties = data[row['owner_1'].strip()]['total_properties'] + 1
                data[row['owner_1'].strip()]['total_properties'] = total_properties
                prop_coords = data[row['owner_1'].strip()]['prop_coords']
                prop_coords.append([row['lat'].strip(), row['lng'].strip()])
                data[row['owner_1'].strip()]['prop_coords'] = prop_coords

                line_count += 1
        with open(output, 'w') as file:
            file.write(json.dumps(data))

def remove_one_off_landlords(source, output, significant_property_count):
    with open(source, mode='r') as file:
        data = file.read()
    landlords_and_properties = json.loads(data)
    landlord_count = len(landlords_and_properties.keys())
    significant_landlords = {}
    for landlord in tqdm(landlords_and_properties, total=landlord_count):
        if landlords_and_properties[landlord]['total_properties'] >= significant_property_count:
            significant_landlords[landlord] = {
                'total_properties': landlords_and_properties[landlord]['total_properties'],
                'properties': landlords_and_properties[landlord]['properties']
            }
    print('Significance Threshold: ', significant_property_count, 'Properties Owned')
    print('Significant Landlords: ', len(significant_landlords))
    with open(output, 'w') as file:
            file.write(json.dumps(significant_landlords))

def histogram(source, n_bins):
    with open(source, mode='r') as file:
        landlords_and_properties = file.read()
    data = json.loads(landlords_and_properties)
    landlord_count = len(data.keys())
    x = []
    for landlord in tqdm(data, total=landlord_count):
        x.append(data[landlord]['total_properties'])

    plt.hist(x, n_bins, log=True)
    plt.show()

def main():
#     landlord_count('opa_properties_public.csv', 'unique_landlords.json')
    json_creator('opa_properties_public.csv', 'landlords_and_properties.json')
#     remove_one_off_landlords('landlords_and_properties.json', 'significant_landlords.json', 1)
#     histogram('significant_landlords.json', 100)

main()