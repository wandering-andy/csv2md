# -*- coding: utf-8 -*-

import logging

import click
import create
import directory

from csv2md.directory import generate_dir_structure
from csv2md.helpers import build_nested_list_from_csv


@click.command()
@click.argument("dir_path", type=click.Path(exists=True), default=".")
@click.argument("filename", required=False)
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date"]),
    default="name",
    help="Sort the files by name, size, or date",
)
def search_files(dir_path, filename, sort):
    """
    Search for files in a directory.

    Args:
        dir_path (str): The path of the directory to search.
        filename (str): The name of the file to search for (optional).
        sort (str): The sorting criteria for the search results.
    """
    directory.files.file_search(dir_path, filename, sort)


@click.command()
@click.option("--file-name", help="Name of the Markdown file")
@click.option("--title", help="Title of the Markdown file")
@click.option("--author", help="Author of the Markdown file")
@click.option(
    "-y",
    "--yes",
    is_flag=True,
    help="Get all files in the current directory without prompting",
)
def create_stub_file(file_name, title, author, yes):
    # TODO: Implement this
    """
    Create a stub Markdown file with a list of links to all files in the current directory.
    """
    pass


@click.command(no_args_is_help=True, context_settings={"ignore_unknown_options": True})
@click.argument(
    "csv_file",
    type=click.Path(exists=True, readable=True, resolve_path=True, file_okay=True),
    default="./data.csv",
    nargs=1,
)
@click.option(
    "--csv-headers",
    default=True,
    show_default=True,
    help="Whether the CSV file has headers or not.",
)
@click.option(
    "-o",
    "--output-dir",
    type=click.Path(resolve_path=True),
    default=".",
    show_default=True,
    help="Output directory for the Markdown files.",
)
@click.option(
    "-d",
    "--create-directories",
    default=True,
    show_default=True,
    help="Create folder structure for output files.",
)
@click.option("-v", "--verbose", is_flag=True, default=False)
@click.option("-vv", "--very-verbose", is_flag=True, default=False)
def csv2md(
    csv_file, csv_headers, output_dir, create_directories, verbose, very_verbose
):
    """
    Convert CSV to Markdown.
    """
    if verbose:
        logging.basicConfig(level=logging.INFO)
    if very_verbose:
        logging.basicConfig(level=logging.DEBUG)
    create.convert(
        csv_file, csv_headers, output_dir, create_directories, verbose, very_verbose
    )


# FIXME: [PL1] Needs to have help options here
@click.command(name="bootstrap")
@click.argument("csv_file", type=click.Path(exists=True))
@click.option(
    "--root",
    type=click.Path(exists=True, readable=True, resolve_path=True, file_okay=False),
    help="Root directory to start generating the structure from",
)
@click.option(
    "--create-links",
    default=True,
    is_flag=True,
    help="Creates stub files with links to all files in the current directory",
)
def bootstrap(csv_file, root, create_links):
    """
    Generate a directory structure from a CSV file.

    Args:
        csv_file (str): The path to the CSV file containing the directory structure.
        root (str): The root directory to start generating the structure from. If not provided, the current working directory will be used.
    """
    nested_list = build_nested_list_from_csv(csv_file)
    result = generate_dir_structure(root, nested_list, create_links)
    click.echo(result)


@click.command(name="view-files")
@click.argument("directory", default=".", type=click.Path(exists=True))
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date"]),
    default="name",
    help="Sorting method",
)
@click.command(name="search-files")
@click.argument("directory", default=".", type=click.Path(exists=True))
@click.argument("file_name", required=False)
@click.option(
    "--sort",
    type=click.Choice(["name", "size", "date"]),
    default="name",
    help="Sorting method",
)
def search(directory, file_name, sort):
    """
    Search for files in a directory.

    Args:
        directory (str): The directory to search in.
        file_name (str): The name of the file to search for.
        sort (str): The sorting method to use. Can be 'name', 'size', or 'date'.
    """
    directory.files.search_files(directory, file_name, sort)
    # TODO: Need to add some....thing else? Probably click.echo()
    # TODO: Need to add a help command? I feel like there should be something I can set
    # to up make all the commands show up in the help menu or inherit certain settings from
    # a parent class.


def csv2md_help():
    # TODO: Implement this. Can this automatically run all the commands? So I don't have to update
    # it every time I make a new command.
    # Add additional Click commands and their respective help pages here
    csv2md()
    create_stub_file()
    search_files()
    bootstrap()


# TODO: What the f is this for? Do I need it? How do I default the whole thing to help?
if __name__ == "__main__":
    csv2md_help()
