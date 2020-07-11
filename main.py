# This program is meant to take data provided by Philadelphia's public property data and modify it.
# In order for this to work it is preferred to as opa_properties_public.csv
# Here is a link to the data: https://www.opendataphilly.org/dataset/opa-property-assessments

import csv
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
import numpy as np

# void landlord_count(String source, String output)
# This function creates a basic dictionary histogram of owner_1's
# and how many properties they own.
# It saves the results to a json file.
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

# void json_creator(String source, String output)
# This function creates a dictionary using owner_1's as a key and for the value a dictionary
# of how many properties they own, a list of the properties, and the properties geo coordinates.
# It saves the results to a json file.
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

# void landlord_json_creator(String source, String output)
# This function creates a basic dictionary of owner_1's and how many properties they own.
# It saves the results to a json file.
def landlord_json_creator(source, output):
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
        sorted_landlords = sorted(landlords.items(), key=lambda x: x[1], reverse=True)
    with open(output, 'w') as file:
        file.write(json.dumps(sorted_landlords))

# void property_json_creator(String source, String output)
# This function creates a basic list of the properties in the data set.
# It saves the results to a json file.
def property_json_creator(source, output):
    properties = []

    with open(source, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in tqdm(csv_reader, total=581456):
            if line_count == 0:
                line_count += 1
            properties.append(row['location'].strip())
            line_count += 1
    with open(output, 'w') as file:
        file.write(json.dumps(properties))

# void remove_one_off_landlords(String source, String output, int significant_property_count)
# This function modifies a json file to contain only landlords with property counts higher than
# significant_property_count.
# The results are saved to a json file.
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

# void histogram(String source, int n_bins)
# This function takes json landlord histogram data and turns it into a
# logged histogram to visualize gaps in ownership
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

# void housing_justice_node_json_generator()
# This function generates the json files needed to easier process data in other programs.
def housing_justice_node_json_generator():
    print('Creating landlords_and_properties.json...')
    json_creator('opa_properties_public.csv', 'landlords_and_properties.json')
    print('Creating properties.json...')
    property_json_creator('opa_properties_public.csv', 'properties.json')
    print('Creating landlords.json...')
    landlord_json_creator('opa_properties_public.csv', 'landlords.json')

# void significant_landlords_generator(String source, String output, int significant_property_count)
# This function modifies a json file to contain only landlords with property counts higher than
# significant_property_count.
# The results are saved to a json file.
def significant_landlords_generator(source, output, significant_property_count):
    with open(source, mode='r') as file:
        data = file.read()
    landlords_and_properties = json.loads(data)
    landlord_count = len(landlords_and_properties)
    significant_landlords = []
    for landlord in tqdm(landlords_and_properties, total=landlord_count):
        if landlord[1] >= significant_property_count:
            significant_landlords.append(landlord)
    print('Significance Threshold: ', significant_property_count, 'Properties Owned')
    print('Significant Landlords: ', len(significant_landlords))
    with open(output, 'w') as file:
            file.write(json.dumps(significant_landlords))

def main():
#     landlord_count('opa_properties_public.csv', 'unique_landlords.json')
#     json_creator('opa_properties_public.csv', 'landlords_and_properties.json')
#     remove_one_off_landlords('landlords_and_properties.json', 'significant_landlords.json', 200)
#     histogram('significant_landlords.json', 100)
    landlord_json_creator('opa_properties_public.csv', 'sorted_landlords.json')
    significant_landlords_generator('sorted_landlords.json', 'significant_sorted_landlords.json', 50)
#     property_json_creator('opa_properties_public.csv', 'properties.json')
#     housing_justice_node_json_generator()

main()