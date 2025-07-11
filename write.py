"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )
    with open(filename, 'w', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for approach in results:
            # Prepare the row data for CSV.
            # Ensure all fields are present, even if some are None or NaN.
            row = {
                'datetime_utc': approach.time.strftime('%Y-%m-%d %H:%M') if approach.time else '',
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach._designation, # Use _designation for the primary designation
                'name': approach.neo.name if approach.neo and approach.neo.name else '',
                'diameter_km': approach.neo.diameter if approach.neo else float('nan'),
                'potentially_hazardous': approach.neo.hazardous if approach.neo else False
            }
            writer.writerow(row)


def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.

    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.

    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    output_data = []
    for approach in results:
        # Prepare the dictionary for each close approach.
        # Ensure all fields are included, handling potential None values.
        approach_dict = {
            'datetime_utc': approach.time.strftime('%Y-%m-%d %H:%M') if approach.time else None,
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
        }

        # Prepare the nested dictionary for the associated NEO.
        neo_dict = {
            'designation': approach.neo.designation if approach.neo else None,
            'name': approach.neo.name if approach.neo and approach.neo.name else None,
            'diameter_km': approach.neo.diameter if approach.neo else None,
            'potentially_hazardous': approach.neo.hazardous if approach.neo else False
        }
        # Add the neo_dict under the 'neo' key in the approach_dict.
        approach_dict['neo'] = neo_dict
        output_data.append(approach_dict)

    with open(filename, 'w') as outfile:
        # Use indent for pretty-printing the JSON output.
        json.dump(output_data, outfile, indent=2)

