# -*- coding: utf-8 -*-
import os
from string import capwords
from typing import List

from mdutils.mdutils import MdUtils

from csv2md.helpers import replace_spaces


# TODO: These functions need to be rewritten to be more general. Some of them might be redundant but I think I'll need some of them to keep building out the generate_* functions.
def file_name_formatter(row):
    # TODO: This is going to need to be expanded so that it
    # returns a markdown file name based whatever strings are passed to it
    """
    [CONVERT] Formats a file name based on the given row data.

    Parameters:
        row (dict): A dictionary containing the row data.

    Returns:
        str: The formatted file name.

    Example:
        >>> row = {
        ...     "CITY": "San Francisco",
        ...     "STATE": "California",
        ... }
        >>> file_name_formatter(row)
        'San_Francisco_California.md'
    """
    ext = ".md"
    city_name = replace_spaces(row["CITY"])
    state_name = replace_spaces(row["STATE"])
    return f"{city_name}_{state_name}{ext}"


def file_path_formatter(row):
    """
    [CONVERT] Generates a file path by formatting the given row.

    Args:
        row (dict): A dictionary representing a row of data containing the following keys:
            - 'REGION_NUM': An integer representing the region number.
            - 'FOREST_NAME': A string representing the name of the forest.
            - 'DISTRICT_NAME': A string representing the name of the district.

    Returns:
        str: The formatted file path generated using the region, forest, and district names.
    """
    region = f"region-{row['REGION_NUM']}"
    forest = replace_spaces(row["FOREST_NAME"])
    district = replace_spaces(row["DISTRICT_NAME"])
    return os.path.join(region, forest, district)


def add_information_section(md_file, row):
    """
    [CONVERT] Adds an information section to the markdown file.

    Parameters:
        md_file (MarkdownFile): The markdown file object to add the information section to.
        row (dict): The row containing the information to be added.

    Returns:
        None
    """
    md_file.new_line("# Information")
    md_file.new_line(f"* Region Name: [{row['REGION_NAME']}]()")
    md_file.new_line(f"* Region Number: {row['REGION_NUM']}")
    md_file.new_line(f"* Forest: [{capwords(row['FOREST_NAME'])}]({row['FOREST_URL']})")
    md_file.new_line(f"* Ranger District: [{capwords(row['DISTRICT_NAME'])}]()")
    md_file.new_line("* Modules:")
    for module in sorted(row["MODULES"].split(",")):
        if module.strip() == "":
            md_file.new_line("  - Unknown")
        else:
            md_file.new_line(f"  - {module.strip()}")
    housing = "Unknown" if len(row["HOUSING"]) == 0 else row["HOUSING"].capitalize()
    md_file.new_line(f"* Housing: {housing}")
    md_file.new_line()


def add_notes_section(md_file, row):
    """
    [CONVERT] Adds a new notes section to the given Markdown file.

    Parameters:
        md_file (MarkdownFile): The Markdown file to add the notes section to.
        row (dict): A dictionary representing a row of data containing the notes.

    Returns:
        None
    """
    md_file.new_line("## Notes")
    md_file.new_paragraph(row["NOTES"])


def build_markdown(row):
    """
    [CONVERT] Generate a markdown file based on the given row data.

    Args:
        row (dict): A dictionary containing information for generating the markdown file.

    Returns:
        str: The generated markdown file.
    """
    md_file = generate_markdown_file(
        file_name=file_path_formatter(row),
        title=capwords(row["LOCATION"]),
        author="Big Ernie",
    )
    add_information_section(md_file, row)
    add_notes_section(md_file, row)
    return md_file


# HACK: the generate_* functions seem to be in a good place. Now I need to start USING them to generate some pages.


def generate_markdown_page() -> str:
    """
    Generates a markdown page with a header and a list of files.

    Returns:
        str: The file path of the generated markdown file.
    """
    md_file = generate_markdown_file("README.md", "title", "author")
    # FIXME: Don't I need to be passing more than one parameter?
    generate_markdown_header(md_file)
    # FIXME: Don't I need to be passing more than one parameter?
    generate_markdown_list_linked(md_file)
    # FIXME: Does .create_md_file() actually exist?
    md_file.create_md_file()
    return md_file  # .file_path Goal was probably to return the full path name


def generate_markdown_file(file_name: str, title: str, author: str) -> MdUtils:
    """
    Creates a `MdUtils` object for generating a markdown file.

    Args:
        file_name (str): The name of the markdown file.
        title (str): The title of the markdown file.
        author (str): The author of the markdown file.

    Returns:
        MdUtils: The `MdUtils` object.
    """
    return MdUtils(file_name=file_name, title=title, author=author)


def generate_markdown_header(md_file: MdUtils) -> None:
    """
    Adds a markdown header to the given Markdown file.

    Args:
        md_file (MdUtils): The `MdUtils` object to which the markdown header will be added.

    Returns:
        None
    """
    md_file.write("# This is the Header\n\n")


def generate_markdown_list_linked(
    md_file: MdUtils, file_list: List[str] = None
) -> MdUtils:
    """
    Generates a markdown-formatted list of file names and their paths.

    Args:
        md_file (MdUtils): The `MdUtils` object to which the markdown list will be added.
        file_list (Optional[List[str]]): A list of file paths. Defaults to the current working directory if not provided.

    Returns:
        MdUtils: The `MdUtils` object with the markdown list added.
    """
    if file_list is None:
        file_list = [os.getcwd()]

    for file_path in file_list:
        if os.path.isdir(file_path):
            file_names = [f"- {f}" for f in os.listdir(file_path)]
            md_file.new_inline_link("\n".join(file_names), file_path)
        else:
            md_file.new_inline_link(f"- {os.path.basename(file_path)}", file_path)

    return md_file


def generate_markdown_list(md_file, list):
    """
    Adds a markdown formatted list to the given Markdown file.

    Args:
        md_file (MdUtils): The `MdUtils` object to which the markdown list will be added.
        list (List[str]): A list of strings representing the list items.

    Returns:
        MdUtils: The `MdUtils` object with the markdown list added.

    Raises:
        None
    """

    md_file.new_line("\n".join(f"- {item}" for item in list))

    return md_file
