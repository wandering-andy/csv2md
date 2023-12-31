# -*- coding: utf-8 -*-
from csv2md.directory import file_search
import click
import csv
import logging
import os
from csv2md.markdown import build_markdown, file_path_formatter, generate_markdown_page


def convert(
    csv_file, csv_headers, output_dir, create_directories, verbose, very_verbose
):
    """This script converts each row in a CSV file into a Markdown file."""

    row_count = 0
    try:
        # Check if the output directory exists, create it if it doesn't
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        with open(csv_file, "r", encoding="utf-8") as csv_file:
            if not csv_headers:
                # If the CSV file doesn't have headers, use csv.reader
                csv_reader = csv.reader(csv_file, delimiter=",")
            else:
                # If the CSV file has headers, use DictReader
                csv_reader = csv.DictReader(csv_file, delimiter=",", dialect="excel")

            for row in csv_reader:
                md_file = build_markdown(row)

                # Creates a directory structure based on the headers in the CSV
                if create_directories:
                    logging.debug("Building directory structure...")
                    path = os.path.join(output_dir, file_path_formatter(row))
                    logging.debug(path)
                    os.makedirs(path, exist_ok=True)
                    os.chdir(path)

                md_file.create_md_file()
                os.chdir(output_dir)
                row_count += 1

        print(f"Conversion complete. Processed {row_count} rows.")

    except FileNotFoundError as e:
        print(f"Error: File '{csv_file}' not found.")
        logging.debug("Error Args: %s" % e.args)
        logging.debug("Traceback: %s" % e.with_traceback)
    except csv.Error as e:
        print("CSV Error:", e)
    except Exception as e:
        print("Error while converting:", e)


def generate_stub_file(file_name, title, author, yes):
    """Generates a stub file with a list of links to all files in the current directory."""
    if yes or click.confirm(
        """
                            Do you want to include a list of links to all files
                            in the current directory in your stub file?'):
                            """
    ):
        file_list = file_search
    else:
        file_list = []
    generate_markdown_page(file_name, title, author, file_list)
