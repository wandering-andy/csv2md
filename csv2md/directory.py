# -*- coding: utf-8 -*-
import logging
import os

import click

from csv2md.generator_link import MDLinkGenerator

logging.basicConfig(level=logging.INFO)
# TODO: add level=logging.DEBUG
# TODO: add level=logging.ERROR
# TODO: add logging points for verbose and very-verbose
# TODO: add logging points for view-files and search-files


# TODO: all of the Click stuff needs to be moved to main.py.
# I want the submodules to mostly be functions and I want main.py to mostly be a
# Click flavored wrapper. That means all the staticmethod stuff can be deleted.
class Files:
    import os

    def view_files(directory, sort="name"):
        """
        View the files in a directory.

        Args:
            directory (str): The directory path.
            sort (str, optional): The sort option. Defaults to "name".

        Returns:
            list: A sorted list of file names.
        """
        files = os.listdir(directory)

        if sort == "name":
            files.sort()
        elif sort == "size":
            files.sort(key=lambda file: os.path.getsize(os.path.join(directory, file)))

        return files

    # Note: in an older version of the code, search_files() was meant to search for the default file
    # we were creating, before creating the default file.
    def search_files(directory, file_name, sort="name"):
        """
        Search for a specific file in a directory.
        If no arguments are provided, show all files in the current directory.

        Args:
            directory (str): The directory to search in.
            file_name (str): The name of the file to search for.
            sort (str, optional): Defaults to "name". Can be 'name', 'size', or 'date'.
        """
        logging.info(f"Searching for file '{file_name}' in directory '{directory}'")

        if file_name is None:
            files = Files.view_files(directory, sort)
            for file in files:
                click.echo(file)
        else:
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                click.echo(f"File '{file_name}' found at: {file_path}")
            else:
                click.echo(f"File '{file_name}' not found in directory '{directory}'")


def generate_dir_structure(root_directory=None, nested_list=None, create_links=False):
    """
    Generate a directory structure from a nested list.

    Args:
        root_directory (str): The root directory to start generating the structure from. Defaults to the current working directory if not provided.
        nested_list (list): A nested list representing the directory structure. Defaults to an empty list if not provided.
        create_links (bool): Whether to generate links to files or not. Defaults to False.

    Raises:
        ValueError: If the nested_list is empty.

    Returns:
        str: The path of the root directory and the total number of directories created.
    """
    if nested_list is None:
        nested_list = []

    if not nested_list:
        raise ValueError("Nested list cannot be empty.")

    if root_directory is None:
        root_directory = os.getcwd()

    directory_counter = 0

    md_link_generator = MDLinkGenerator()  # Instantiate the MDLinkGenerator class

    for item in nested_list:
        directory_path = os.path.join(root_directory, item[0])
        os.makedirs(directory_path, exist_ok=True)
        directory_counter += 1

        if len(item) > 1:
            subdirectory_counter = generate_dir_structure(
                directory_path, item[1:], create_links
            )
            directory_counter += subdirectory_counter

        if create_links:
            md_link_generator.generate_md_link_file(
                directory_path
            )  # Call the generate_md_link_file method

    return f"Directory structure created in {root_directory}. Total directories created: {directory_counter}"
