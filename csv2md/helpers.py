# -*- coding: utf-8 -*-
import csv


def replace_spaces(text: str) -> str:
    """
    Replaces spaces in the given text with hyphens and removes periods, converting the text to lowercase.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The processed text with spaces replaced by hyphens, periods removed, and converted to lowercase.

    Raises:
        None
    """
    return text.replace(" ", "-").replace(".", "").lower()


def build_nested_list_from_csv(csv_file_path):
    nested_list = []
    with open(csv_file_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            nested_list.append(row)
    return nested_list
