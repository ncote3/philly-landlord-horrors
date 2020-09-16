from tqdm import tqdm
import json
import matplotlib.pyplot as plt
import numpy
import csv


def find_llc_owners(source, output):
    data = json.load(open(source))
    out = []
    count = 0
    for owner in tqdm(data, total=len(data)):
        if owner[0].find('LLC') != -1:
            out.append(owner)
            count += 1

    json.dump(out, open(output, 'w+'))
    print('There are ', count, 'LLCs in this dataset or ', (count/len(data))*100, '% of owners.')


def make_llc_owners_histogram(source, n_bins):
    data = json.load(open(source))
    property_counts = [p[1] for p in data]
    fig, ax = plt.subplots(1, 1)
    ax.hist(property_counts, n_bins, log=True, color=['grey'])
    ax.set_title('Histogram of Property Ownership by LLCs')
    ax.set_xlabel('No. of Properties Owned')
    ax.set_ylabel('No. of Owners (Logged)')
    plt.savefig('./../figures/llc_histogram.png')
    plt.show()


def find_one_char_owner(source, output):
    data = json.load(open(source))
    out = []
    count = 0
    for owner in tqdm(data, total=len(data)):
        if len(owner[0]) == 1:
            out.append(owner)
            count += 1

    json.dump(out, open(output, 'w+'))
    print('There are ', count, 'one character owner_1 in this dataset.')


def find_n_char_owner(source, output, n):
    data = json.load(open(source))
    out = []
    count = 0
    for owner in tqdm(data, total=len(data)):
        if len(owner[0]) == n:
            out.append(owner)
            count += 1

    json.dump(out, open(output, 'w+'))
    print('There are ', count, n, ' character owner_1 in this dataset.')


def make_char_count_owner_histogram(source, n_bins):
    data = json.load(open(source))
    owner_lens = []
    for owner in tqdm(data, total=len(data)):
        owner_lens.append(len(owner[0]))
    fig, ax = plt.subplots(1, 1)
    ax.hist(owner_lens, n_bins, color=['grey'])
    ax.set_title('Histogram of Owner Name Length')
    ax.set_xlabel('Number of owner_1s')
    ax.set_ylabel('Character Count')
    plt.savefig('./../figures/char_count_owner_histogram.png')
    plt.show()


def make_address_owners_histogram(source, n_bins, title, output):
    data = json.load(open(source))
    owner_prop_counts = []
    for owner in tqdm(data, total=len(data)):
        owner_prop_counts.append(owner[1])

    fig, ax = plt.subplots(1, 1)
    ax.hist(owner_prop_counts, n_bins, color=['grey'], log=True)
    ax.set_title(title)
    ax.set_xlabel('Number of address owner_1s')
    ax.set_ylabel('Property Count')
    plt.savefig(output)


def find_address_owners(source):
    data = json.load(open(source))
    out = []
    count = 0

    for owner in tqdm(data, total=len(data)):
        for prop in data[owner]['properties']:
            if owner.find(prop) != -1:
                out.append([owner, data[owner]['total_properties']])
                count += 1

    json.dump(out, open('./../data/address_owners.json', 'w+'))

    no_llc_out = []
    no_llc_count = 0

    for owner in tqdm(data, total=len(data)):
        for prop in data[owner]['properties']:
            if owner.find(prop) != -1 and owner.find('LLC') == -1:
                no_llc_out.append([owner, data[owner]['total_properties']])
                no_llc_count += 1

    json.dump(out, open('./../data/no_llc_address_owners.json', 'w+'))

    llc_out = []
    llc_count = 0

    for owner in tqdm(data, total=len(data)):
        for prop in data[owner]['properties']:
            if owner.find(prop) != -1 and owner.find('LLC') != -1:
                llc_out.append([owner, data[owner]['total_properties']])
                llc_count += 1

    json.dump(out, open('./../data/llc_address_owners.json', 'w+'))

    print('There are ', count, 'Address Owners in this dataset.')
    print('There are ', no_llc_count, 'Non-LLC Address Owners in this dataset.')
    print('There are ', llc_count, 'LLC Address Owners in this dataset.')

    print('Creating figures...')
    make_address_owners_histogram('./../data/address_owners.json',
                                  40,
                                  'Histogram of Address Named owner_1s',
                                  './../figures/address_owners_histogram.png')

    make_address_owners_histogram('./../data/no_llc_address_owners.json',
                                  40,
                                  'Histogram of Non-LLC Address Named owner_1s',
                                  './../figures/no_llc_address_owners_histogram.png')

    make_address_owners_histogram('./../data/llc_address_owners.json',
                                  40,
                                  'Histogram of LLC Address Named owner_1s',
                                  './../figures/llc_address_owners_histogram.png')

def find_one_prop_owners(source):
    data = json.load(open(source))
    count = 0
    for owner in tqdm(data, total=len(data)):
        if owner[1] == 1:
            count += 1
    percentage = (count / len(data)) * 100
    print('There are ', count, 'one property owners in this dataset.')
    print("That's ", percentage, '% of total owners.')
    
def get_owner_2_count(source, output):
    owners = []
    owner2_count = 0
    with open(source, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in tqdm(csv_reader, total=581456):
            if line_count == 0:
                line_count += 1
            else:
                try:
                    owners.append([row["owner_1"].strip(), row["owner_2"].strip()])
                    if (row["owner_2"].strip() == ""):
                        owner2_count += 1
                except:
                     print(row["owner_1"].strip(), "is missing a count.")
    with open(output, 'w') as file:
        file.write(json.dumps(owners))
    print('There are ', owner2_count, 'owner_2s in this dataset.')
    
def get_owners_and_mailing_address(source, output):
    owners_with_mailing_address = []
    mailing_address_count = 0
    with open(source, mode="r") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        owner_1_count = 0
        owner_2_count = 0
        mailing_address_1_count = 0
        mailing_address_2_count = 0
        mailing_care_of_count = 0
        mailing_city_state_count = 0
        mailing_street_count = 0
        mailing_zip_count = 0
        for row in tqdm(csv_reader, total=581456):
            if line_count == 0:
                line_count += 1
            else:
                line_count += 1
            
                owner_1 = row["owner_1"].strip()
                owner_2 = row["owner_2"].strip()
                mailing_address_1 = row["mailing_address_1"].strip()
                mailing_address_2 = row["mailing_address_2"].strip()
                mailing_care_of = row["mailing_care_of"].strip()
                mailing_city_state = row["mailing_city_state"].strip()
                mailing_street = row["mailing_street"].strip()
                mailing_zip = row["mailing_zip"].strip()
                mailing_info = [
                    mailing_address_1,
                    mailing_address_2,
                    mailing_care_of,
                    mailing_city_state,
                    mailing_street,
                    mailing_zip
                ]
                owners_with_mailing_address.append([owner_1, owner_2, mailing_info])
                if (owner_1 != ""):
                    owner_1_count += 1
                if (owner_2 != ""):
                    owner_2_count += 1
                if (mailing_address_1 != ""):
                    mailing_address_1_count += 1
                if (mailing_address_2 != ""):
                    mailing_address_2_count += 1
                if (mailing_care_of != ""):
                    mailing_care_of_count += 1
                if (mailing_city_state != ""):
                    mailing_city_state_count += 1
                if (mailing_street != ""):
                    mailing_street_count += 1
                if (mailing_zip != ""):
                    mailing_zip_count += 1

    with open(output, 'w') as file:
        file.write(json.dumps(owners_with_mailing_address))
    line_count -= 1 # need to account for the first line in the csv
    print('There are ', line_count, 'properties in this dataset.')
    print('There are ', owner_1_count, 'owner_1s in this dataset or ', (owner_1_count/line_count)*100, ' %.')
    print('There are ', owner_2_count, 'owner_2s in this dataset or ', (owner_2_count/line_count)*100, ' %.')
    print('There are ', mailing_address_1_count, 'mailing_address_1s in this dataset or ', (mailing_address_1_count/line_count)*100, ' %.')
    print('There are ', mailing_address_2_count, 'mailing_address_2s in this dataset or ', (mailing_address_2_count/line_count)*100, ' %.')
    print('There are ', mailing_care_of_count, 'mailing_care_ofs in this dataset or ', (mailing_care_of_count/line_count)*100, ' %.')
    print('There are ', mailing_city_state_count, 'mailing_city_states in this dataset or ', (mailing_city_state_count/line_count)*100, ' %.')
    print('There are ', mailing_street_count, 'mailing_streets in this dataset or ', (mailing_street_count/line_count)*100, ' %.')
    print('There are ', mailing_zip_count, 'mailing_zips in this dataset or ', (mailing_zip_count/line_count)*100, ' %.')
    
def main():
    # find_llc_owners('./../../../data_sets/sorted_landlords.json', './../data/llc_owner.json')
    # make_llc_owners_histogram('./../data/llc_owner.json', 100)
    # find_one_char_owner('./../../../data_sets/sorted_landlords.json', './../data/one_char_owner.json')
    # find_n_char_owner('./../../../data_sets/sorted_landlords.json', './../data/25_char_owner.json', 25)
    # make_char_count_owner_histogram('./../../../data_sets/sorted_landlords.json', 25)
    # find_address_owners('./../../../data_sets/landlords_and_properties.json')
    # find_one_prop_owners('./../../../data_sets/sorted_landlords.json')
    # get_owner_2_count('./../../../data_sets/opa_properties_public.csv', './../../../data_sets/owner1_owner2.json')
    get_owners_and_mailing_address('./../../../data_sets/opa_properties_public.csv', './../../../data_sets/owners_mailing_address.json')

main()
