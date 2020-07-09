# philly-landlord-horrors
Playing with Philly Open Property Assessment Data to uncover the secrets of the owning class.

## Data Source:
https://www.opendataphilly.org/dataset/opa-property-assessments

## To Run:

Make sure you have downloaded the data set and place it in the
root of this repository. The program knows it as `opa_properties_public.csv`.

This program uses Python3.

The following needs to be installed in your python3 venv:
* `tqdm`
* `numpy`
* `matplotlib`

Once these are installed simply run: `python3 main.py`

## Usage:
###`landlord_count(source, output)`
This function creates a basic dictionary histogram of owner_1's and how many properties they own. 

It saves the results to a json file.

###`json_creator(source, output)`
This function creates a dictionary using owner_1's as a key and for the value a dictionary
of how many properties they own, a list of the properties, and the properties geo coordinates.

It saves the results to a json file.

###`landlord_json_creator(source, output)`
This function creates a basic dictionary of owner_1's and how many properties they own.

It saves the results to a json file.

###`property_json_creator(source, output)`
This function creates a basic list of the properties in the data set.

It saves the results to a json file.

###`remove_one_off_landlords(source, output, significant_property_count)`
This function modifies a json file to contain only landlords with property counts higher than
significant_property_count.

The results are saved to a json file.

###`histogram(source, n_bins)`
This function takes json landlord histogram data and turns it into a
logged histogram to visualize gaps in ownership

###`housing_justice_node_json_generator()`
This function generates the json files needed to easier process data in other programs.

###`main()`
Program driver, insert the function you want to use here.