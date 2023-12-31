# -*- coding: utf-8 -*-
import csv

from csv2md.create import convert


def test_convert(tmp_path):
    input_data = {
        "REGION_NUMBER": 7,
        "REGION_NAME": "Secret",
        "FOREST_NAME": "Double Secret",
        "DISTRICT_NAME": "Top Secret",
        "CITY": "Nowhere",
        "STATE": "AK",
        "LOCATION": "Nowhere, AK",
        "MODULES": "Super Saiyan Smokey",
        "HOUSING": "No",
        "NOTES": "All the notes",
        "FOREST_URL": "www.google.com",
    }

    expected_output = [
        """
        ## Nowhere AK

        ### Information
        * Region Name: Secret
        * Region Number: 7
        * Forest: [Double Secret](www.google.com)
        * Ranger District: Top Secret
        * Modules:
        - Super Saiyan Smokey
        * Housing: No
        * Notes:
        All the notes

        Automatically generated by csv-to-md.py on 2021-01-01 @ 12:00:00"
        """
    ]
    temp_csv_file = tmp_path / "data.csv"

    with open(temp_csv_file, mode="w", newline="") as file:
        fieldnames = input_data.keys()
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(input_data)

    # Call the function being tested
    result = convert(temp_csv_file)
    # Assert the expected output
    assert result == expected_output
