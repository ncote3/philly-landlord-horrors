import json
from tqdm import tqdm
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def fuzzy_string_match_on_owner_1(source, string_to_match):
    data = json.load(open(source))
    owner_1s = []
    print('Getting Owners...')
    for owner in tqdm(data, total=len(data)):
        owner_1s.append(owner[0])
    ratios = []
    print('uwu fuzzy wuzzy at werk uwu....')
    for owner in tqdm(owner_1s, total=len(owner_1s)):
        score = fuzz.ratio(string_to_match, owner)
        if score > 80:
            ratios.append([owner, score])
    ratios.sort(key=lambda x: x[1], reverse=True)
    output = './data_sets/fuzzy_string_ratios/' + string_to_match + '.json'
    json.dump(ratios, open(output, 'w'))


def merge_same_owners(source, correct_entry, entry_to_merge):
    data = json.load(open(source))
    correct_owner_object = {}
    to_merge_owner_object = {}
    print('Finding correct owner objects...')
    for owner in tqdm(data, total=len(data)):
        if owner == correct_entry:
            correct_owner_object = data[owner]
        if owner == entry_to_merge:
            to_merge_owner_object = data[owner]
    del data[correct_entry]
    del data[entry_to_merge]
    original_count_property = correct_owner_object["total_properties"]
    expected_count_property = correct_owner_object["total_properties"] + to_merge_owner_object["total_properties"]
    correct_owner_object["total_properties"] += to_merge_owner_object["total_properties"]
    print('Merging properties...')
    for property in tqdm(to_merge_owner_object["properties"], total=len(to_merge_owner_object["properties"])):
        correct_owner_object["properties"][property] = to_merge_owner_object["properties"][property]
    data[correct_entry] = correct_owner_object

    print('Original Property Count:',  original_count_property)
    print('Expected Property Count:', expected_count_property)
    print('Actual Property Count:', correct_owner_object["total_properties"])

    json.dump(data, open(source, 'w'))


def main():
    merge_same_owners('./data_sets/landlords_and_properties.json', 'JAMISON ROAD ASSOCIATES L',
                      'JAMISON ROAD ASSOC')
    # fuzzy_string_match_on_owner_1('./data_sets/unique_landlords.json', 'PHILADELPHIA HOUSING AUTH')


main()
