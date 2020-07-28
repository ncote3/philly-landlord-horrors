import csv
from tqdm import tqdm
import json
import matplotlib.pyplot as plt

# Will do a zip code analysis of the csv property data
# Example usage can be found in main()


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

# This will create a bar chart of the zip code analysis done in total_zip_analysis()
# Example usage can be found in main()


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

# This will do an analysis on where owner_1's property is distributed across zip codes
# Example usage can be found in main()


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

    json.dump(zip_counts, open(owner_1 + '.json', 'w'))

# This will create a bar chart for the data outputted by single_owner_zip_analysis()
# Example Usage can be found in main()


def single_zip_bar_chart(source, owner_1):
    single_zip_histogram = json.load(open(source))

    pairs = single_zip_histogram.items()  # [(zip, count), ...]
    pairs = sorted(pairs, key=lambda x: x[0])
    keys = [p[0] for p in pairs]
    values = [p[1] for p in pairs]

    plt.figure(figsize=(12, 6.5))
    plt.title(owner_1 + "'s Properties per Zip Code")
    plt.xlabel('Philadelphia Zip Codes')
    plt.ylabel('No. Properties')
    plt.bar(range(len(single_zip_histogram)), values, align='center', width=0.5)
    plt.xticks(range(len(single_zip_histogram)), keys, rotation='vertical')
    plt.show()

# This will create analysis data for the biggest property owners in a given zip code
# Example Usage can be found in main()


def generate_single_zip_analysis_full(source, output):
    data = json.load(open(source))
    landlord_zip_counts = {}
    for landlord in tqdm(data, total=len(data)):
        try:
            properties = data[landlord]['properties']
        except KeyError:
            print("Didn't find ", landlord)
            return 0
        zip_counts = {}
        for property in properties:
            property_zip_code = properties[property]['zip_code'].strip()[0:5]
            if property_zip_code not in zip_counts.keys():
                zip_counts[property_zip_code] = 1
            else:
                try:
                    zip_count = zip_counts[property_zip_code]
                    zip_counts[property_zip_code] = zip_count + 1
                except KeyError:
                    print(property_zip_code, "is missing a count.")
        landlord_zip_counts[landlord] = zip_counts
    json.dump(landlord_zip_counts, open(output, 'w'))

# This will get the biggest property owners in a single zip code
# Example usage can be found in main()


def get_single_zip_counts(source, zip_code):
    data = json.load(open(source))
    zip_counts = {}
    for landlord in data:
        if zip_code in data[landlord].keys():
            count = data[landlord][zip_code]
            zip_counts[landlord] = count
    sorted_top = {k: v for k, v in sorted(zip_counts.items(), key=lambda item: item[1], reverse=True)}
    return sorted_top

# This function is used to truncate how many people are displayed in the analysis of get_single_zip_counts()
# and generate_single_zip_analysis_full()


def truncate_to_top_n(source, top_n):
    data = json.load(open(source))
    zip_dict = {}
    for zip_code in tqdm(data, total=len(data)):
        counts = data[zip_code]
        top = {}
        for count in list(counts)[0:top_n + 1]:
            top[count] = counts[count]
        zip_dict[zip_code] = top
    output = 'top_' + str(top_n) + '_in_all_zips.json'
    json.dump(zip_dict, open(output, 'w'))

# This function will create a json object that contains the top 20 owners in every zip code
# Example Usage in main()


def get_zip_tops(source, output):
    philly_zip_codes = [
        '19102', '19103', '19104', '19106', '19107', '19109', '19110', '19111', '19112', '19113', '19114', '19115',
        '19116', '19118', '19119', '19120', '19121', '19122', '19123', '19124', '19125', '19126', '19127', '19128',
        '19129', '19130', '19131', '19132', '19133', '19134', '19135', '19136', '19137', '19138', '19139', '19140',
        '19141', '19142', '19143', '19144', '19145', '19146', '19147', '19148', '19149', '19150', '19151', '19152',
        '19153', '19154',
    ]
    zip_dict = {}
    for zip_code in tqdm(philly_zip_codes, total=len(philly_zip_codes)):
        zip_dict[zip_code] = get_single_zip_counts(source, zip_code)
    json.dump(zip_dict, open(output, 'w'))

# Function to create bar chart of the data generated by get_zip_tops()
# Usage can be found in main()


def make_zip_tops_bar_chart(source):
    data = json.load(open(source))
    for zip_code in tqdm(data, total=len(data)):
        pairs = data[zip_code].items()
        keys = [p[0] for p in pairs]
        values = [p[1] for p in pairs]
        plt.figure(figsize=(12, 8))
        plt.title(zip_code + " Top Owners per Zip Code")
        plt.xlabel('owner_1')
        plt.ylabel('No. Properties')
        plt.bar(range(len(data[zip_code])), values, align='center', width=0.5)
        plt.xticks(range(len(data[zip_code])), keys, rotation='vertical')
        plt.subplots_adjust(bottom=0.4)
        plt.savefig('./figures/top_in_zip_code/'+zip_code+'.png')
        plt.close()

# Function used to format individual zip analysis data in a way that Victory (React Visualization Lib)
# can use it.
# Example usage in main()


def format_data_for_react(source, output):
    data = json.load(open(source))
    output_object = {}
    for zip_code in tqdm(data, total=len(data)):
        plot_array = []
        for owner in data[zip_code]:
            plot_array.append({'owner': owner, 'property_count': data[zip_code][owner]})
        output_object[zip_code] = plot_array
    json.dump(output_object, open(output, 'w'))

# Used to create bar chart data of the city's owner
# Example usage in main()


def city_wide_dist_for_react(source, output):
    data = json.load(open(source))
    output_a = []
    for owner in tqdm(data, total=len(data)):
        output_a.append({'owner': owner[0], 'property_count': owner[1]})
    json.dump(output_a, open(output, 'w'))


def main():
    # total_zip_analysis('opa_properties_public.csv', 'total_zip_counts.json')
    # total_zip_bar_chart('total_zip_counts.json')
    # single_owner_zip_analysis('landlords_and_properties.json', 'PHILADELPHIA HOUSING AUTH')
    # single_zip_bar_chart('PHILADELPHIA HOUSING AUTH.json', 'PHILADELPHIA HOUSING AUTH')
    # generate_single_zip_analysis_full('landlords_and_properties.json', 'landlord_zip_counts.json')
    # get_single_zip_counts('landlord_zip_counts.json', '19104')
    # get_zip_tops('landlord_zip_counts.json', 'top_in_zip_full.json')
    # truncate_to_top_n('top_in_zip_full.json', 20)
    # make_zip_tops_bar_chart('top_20_in_all_zips.json')
    # format_data_for_react('./data_sets/top_20_in_all_zips.json', './data_sets/FE/zip_code_bar_data.json')
    city_wide_dist_for_react('./data_sets/significant_sorted_landlords.json', './data_sets/FE/city_wide_dist.json')


main()
