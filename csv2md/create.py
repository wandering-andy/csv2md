# -*- coding: utf-8 -*-
import csv
import logging
import os

from csv2md.directory import files
from csv2md.markdown import markdown


def convert(
    csv_file, csv_headers, output_dir, create_directories, verbose, very_verbose
):
    """
    Convert a CSV file to Markdown files.

    Args:
        csv_file (str): The path to the CSV file to be converted.
        csv_headers (bool): Flag indicating whether the CSV file contains headers.
        output_dir (str): The directory where the Markdown files will be saved.
        create_directories (bool): Flag indicating whether to create directories based on CSV data.
        verbose (bool): Flag indicating whether to display verbose output.
        very_verbose (bool): Flag indicating whether to display very verbose output.

    Returns:
        None
    """

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
                md_file = markdown.v1.build_markdown(row)

                # Creates a directory structure based on the headers in the CSV
                if create_directories:
                    logging.debug("Building directory structure...")
                    path = os.path.join(
                        output_dir, markdown.v1.file_path_formatter(row)
                    )
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


class MDLinkGenerator:
    def __init__(self, file_name="about.md", title="About", author=None):
        """
        Initialize an instance of the MDLinkGenerator class.

        Args:
            file_name (str, optional): The name of the Markdown file to be generated. Defaults to "about.md".
            title (str, optional): The title of the Markdown page. Defaults to "About".
            author (str, optional): The author of the Markdown page. Defaults to None.
        """
        self.file_name = file_name
        self.title = title
        self.author = author

    def generate_md_link_file(self, directory="."):
        """
        Generate a Markdown file with links to other files in the specified directory.

        Args:
            directory (str, optional): The directory to search for files. Defaults to ".".

        Returns:
            None
        """
        md_file = markdown.v2.generate_md_page(self.file_name, self.title, self.author)
        file_list = files.view_files(directory)

        for file in file_list:
            file_path = os.path.join(directory, file)
            file_link = f"[{file}]({file_path})"
            md_file.new_line(file_link)

        md_file.create_md_file()
