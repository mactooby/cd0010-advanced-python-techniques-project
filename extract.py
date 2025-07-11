"""Extract data on near-Earth objects and close approaches from CSV and JSON files.

The `load_neos` function extracts NEO data from a CSV file, formatted as
described in the project instructions, into a collection of `NearEarthObject`s.

The `load_approaches` function extracts close approach data from a JSON file,
formatted as described in the project instructions, into a collection of
`CloseApproach` objects.

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

You'll edit this file in Task 2.
"""
import csv
import json

from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file.

    :param neo_csv_path: A path to a CSV file containing data about near-Earth objects.
    :return: A collection of `NearEarthObject`s.
    """
    # TODO: Load NEO data from the given CSV file.
    neos_list = []

    with open(neo_csv_path,'r') as neo_file:
        reader  = csv.DictReader(neo_file)
        for row in reader:
            #print(type(row))
            neos_list.append(NearEarthObject(**row))
            


    return neos_list


# def load_approaches(cad_json_path):
#     """Read close approach data from a JSON file.

#     :param cad_json_path: A path to a JSON file containing data about close approaches.
#     :return: A collection of `CloseApproach`es.
#     """
#     # TODO: Load close approach data from the given JSON file.
#     return ()

# def load_approaches(cad_json_path):
#     """Read close approach data from a JSON file.

#     :param cad_json_path: A path to a JSON file containing data about close approaches.
#     :return: A collection of `CloseApproach`es.
#     """
#     approaches = []
#     with open(cad_json_path, 'r') as f:
#         data = json.load(f)
    
#     for approach_data in data['data']:
#         designation = approach_data[0]
#         time = approach_data[3]  # You might want to convert this to a datetime object later
#         distance = float(approach_data[4])
#         velocity = float(approach_data[7])
        
#         #approaches.append(CloseApproach(designation, time, distance, velocity))
#         approaches.append(CloseApproach(**approach_data))
#     return approaches


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param cad_json_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    approaches = []
    with open(cad_json_path, 'r') as f:
        raw_data = json.load(f)

    fields = raw_data['fields'] # Get the list of field names
    
    for approach_data_list in raw_data['data']:
        # Create a dictionary by zipping field names with their corresponding values
        approach_info = dict(zip(fields, approach_data_list))
        
        # Pass the dictionary to the CloseApproach constructor using **
        approaches.append(CloseApproach(**approach_info))

    return approaches







