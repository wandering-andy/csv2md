# -*- coding: utf-8 -*-
import click
import os


# TODO: add some logging flags and options
def file_search(directory, file_name, sort):
    """
    Search for a specific file in a directory.
    If no arguments are provided, show all files in the current directory.

    Args:
        directory (str): The directory to search in.
        file_name (str): The name of the file to search for.
        sort (str): The sorting method to use. Can be 'name', 'size', or 'date'.
    """
    if file_name is None:
        files = view_files(directory, sort)
        for file in files:
            click.echo(file)
    else:
        file_path = os.path.join(directory, file_name)
        if os.path.exists(file_path):
            click.echo(f"File '{file_name}' found at: {file_path}")
        else:
            click.echo(f"File '{file_name}' not found in directory: {directory}")


def view_files(directory, sort):
    """
    Get a list of files in a directory.

    Args:
        directory (str): The directory to get files from.
        sort (str): The sorting method to use. Can be 'name', 'size', or 'date'.

    Returns:
        list: The list of file names in the directory, sorted according to the specified sorting method.
    """
    files = os.listdir(directory)
    if sort == "name":
        files.sort()
    elif sort == "size":
        files.sort(key=lambda f: os.path.getsize(os.path.join(directory, f)))
    elif sort == "date":
        files.sort(key=lambda f: os.path.getmtime(os.path.join(directory, f)))
    return files


def walkthrough_structure(directory):
    """
    Walk through the directory structure and call file_search() in each directory.

    Args:
        directory (str): The root directory to start the walkthrough from.
    """
    for root, files in os.walk(directory):
        for file in files:
            file_search(root, file)
