import json


def get_input_on_entries(entries, owner):
    out = {}
    entry_num_dict = {}
    count = 0
    error_msg = '\nTry entering that again!\n'
    entry_owner_name_option = 0
    business_name_option = 1

    print('\n\n\nWhich of these is the correct LLC?')
    print('Owner: ', owner)

    for entry in entries:
        entry_owner_name = entry  # I know this is redundant, its because I never learned to read
        business_name = entries[entry]['business_name']
        legal_entity_type = entries[entry]['legal_entity_type']
        is_active_license = entries[entry]['is_active_license']

        entry_num_dict[count] = [entry_owner_name, business_name]

        print('Option ', count, ':')
        print('\tLegal Entity Type: ', legal_entity_type)
        print('\tActive License: ', is_active_license)
        print('\tEntry owner name: ', entry_owner_name)
        print('\tBusiness Name: ', business_name)
        count += 1

    check_flag_1 = False
    while check_flag_1 is False:
        entry_option = input('\nWhich option is correct? Enter the number: ')
        try:
            if int(entry_option) in entry_num_dict.keys():
                check_flag_1 = True
                check_flag_2 = False
                while check_flag_2 is False:
                    which_name = input('Was it:\n\t0: Entry Owner Name\n\t1: Business Name\n')
                    try:
                        if int(which_name) == 0:
                            out[owner] = entry_num_dict[int(entry_option)][entry_owner_name_option]
                            check_flag_2 = True
                        elif int(which_name) == 1:
                            out[owner] = entry_num_dict[int(entry_option)][business_name_option]
                            check_flag_2 = True
                        else:
                            print(error_msg)
                    except:
                        print(error_msg)
            elif entry_option == ' ':
                check_flag_1 = True
            else:
                print(error_msg)
        except:
            if entry_option == ' ':
                check_flag_1 = True
            else:
                print(error_msg)
    return out


def annotate_fuzzy_l(source, output):
    data = json.load(open(source))
    out = []
    total_owners_confirmed = 0
    owner_processed_count = 0
    check_point_start = int(input('Where would you like to start (Checkpoint): '))

    for owner in data:
        if owner_processed_count >= check_point_start:
            entries = data[owner]
            results = get_input_on_entries(entries, owner)
            if results != {}:
                out.append(results)
                total_owners_confirmed += 1
            if owner_processed_count % 10 == 0 and owner_processed_count != check_point_start:
                check_point_name = './../data/annotation_checks/annotated_fuzzy_L_results_checkpoint' + \
                                   str(int(owner_processed_count / 10)) + '.JSON'
                json.dump(out, open(check_point_name, 'w+'))
                print('\nJust saved a checkpoint! Checkpoint: ', owner_processed_count)
            owner_processed_count += 1
        else:
            owner_processed_count += 1
    print('This is where you left off: ', owner_processed_count)
    print('You confirmed ', total_owners_confirmed, 'owners.')


def combine_checkpoints():
    checkpoint_count = 1
    out = []

    while checkpoint_count < 21:
        file_string = './../data/annotation_checks/annotated_fuzzy_L_results_checkpoint' + \
                      str(checkpoint_count) + '.JSON'
        check_point_data = json.load(open(file_string))
        for entry in check_point_data:
            out.append(entry)
        checkpoint_count += 1
    json.dump(out, open('./../data/annotated_fuzzy_L_results.JSON', 'w+'))
    print("\nDone.\n")


# annotate_fuzzy_l('./../data/fuzz_ratio_L_split_LLC_match.JSON', './../data/annotated_fuzzy_L_results.JSON')
combine_checkpoints()
