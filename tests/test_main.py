# -*- coding: utf-8 -*-
import logging

import click
from csv2md import directory, create


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
    directory.file_search(dir_path, filename, sort)


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
    """
    Create a stub Markdown file with a list of links to all files in the current directory.
    """
    directory.generate_stub_file(file_name, title, author, yes)


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
