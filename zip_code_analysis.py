import csv
from tqdm import tqdm
import json
import matplotlib.pyplot as plt
import numpy as np

from collections import defaultdict


def total_zip_analysis(source, output):
    zip_counts = {}

    with open(source, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        zip_wack = []
        for row in tqdm(csv_reader, total=581456):
            zip_code = row["zip_code"].strip()[0:5]
            if zip_code == "":
                zip_wack.append(row["owner_1"].strip())
            if line_count == 0:
                line_count += 1
            if zip_code not in zip_counts.keys():
                zip_counts[zip_code] = 1
                line_count += 1
            else:
                try:
                    zip_count = zip_counts[zip_code]
                    zip_counts[zip_code] = zip_count + 1
                except:
                    print(zip_code, "is missing a count.")
                line_count += 1
    unique_zip_codes = len(zip_counts)
    print(zip_wack)
    print('There are ', unique_zip_codes, 'unique zip codes in this dataset.')

    with open(output, 'w') as file:
        file.write(json.dumps(zip_counts))


def total_zip_bar_chart(source):
    total_zip_histogram = json.load(open(source))

    pairs = total_zip_histogram.items()  # [(zip, count), ...]
    pairs = sorted(pairs, key=lambda x: x[0])
    keys = [p[0] for p in pairs]
    values = [p[1] for p in pairs]

    plt.figure(figsize=(12, 6.5))
    plt.title('Total Properties per Zip Code')
    plt.xlabel('Philadelphia Zip Codes')
    plt.ylabel('No. Properties')
    plt.bar(range(len(total_zip_histogram)), values, align='center', width=0.5)
    plt.xticks(range(len(total_zip_histogram)), keys, rotation='vertical')
    plt.show()


def single_owner_zip_analysis(source, owner_1):
    data = json.load(open(source))

    try:
        print('Getting property list...')
        properties = data[owner_1]['properties']
    except KeyError:
        print("Didn't find ", owner_1)
        return 0

    zip_counts = {}
    for property in tqdm(properties, total=len(properties.keys())):
        property_zip_code = properties[property]['zip_code'].strip()[0:5]
        if property_zip_code not in zip_counts.keys():
            zip_counts[property_zip_code] = 1
        else:
            try:
                zip_count = zip_counts[property_zip_code]
                zip_counts[property_zip_code] = zip_count + 1
            except KeyError:
                print(property_zip_code, "is missing a count.")
    unique_zip_codes = len(zip_counts)
    print('There are ', unique_zip_codes, 'unique zip codes in ', owner_1, "'s properties.")

    json.dump(zip_counts, open(owner_1+'.json', 'w'))


def single_zip_bar_chart(source, owner_1):
    single_zip_histogram = json.load(open(source))

    pairs = single_zip_histogram.items()  # [(zip, count), ...]
    pairs = sorted(pairs, key=lambda x: x[0])
    keys = [p[0] for p in pairs]
    values = [p[1] for p in pairs]

    plt.figure(figsize=(12, 6.5))
    plt.title(owner_1+"'s Properties per Zip Code")
    plt.xlabel('Philadelphia Zip Codes')
    plt.ylabel('No. Properties')
    plt.bar(range(len(single_zip_histogram)), values, align='center', width=0.5)
    plt.xticks(range(len(single_zip_histogram)), keys, rotation='vertical')
    plt.show()


def main():
    # total_zip_analysis('opa_properties_public.csv', 'total_zip_counts.json')
    # total_zip_bar_chart('total_zip_counts.json')
    # single_owner_zip_analysis('landlords_and_properties.json', 'PHILADELPHIA HOUSING AUTH')
    single_zip_bar_chart('PHILADELPHIA HOUSING AUTH.json', 'PHILADELPHIA HOUSING AUTH')

main()
