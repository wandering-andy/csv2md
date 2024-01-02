# -*- coding: utf-8 -*-
import os
from string import capwords

from mdutils.mdutils import MdUtils

from csv2md.helpers import replace_spaces


class MarkdownGenerator:
    def __init__(self):
        pass

    # TODO: These functions need to be rewritten to be more general. Some of them might be redundant but I think I'll need some of them to keep building out the generate_* functions.
    class v1:
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
            # TODO: Rewrite this so that when a key:value pair is passed in it creates a new line with the key and value
            # example: md_file.new_line(f"* key: value")
            md_file.new_line("# Information")
            md_file.new_line(f"* Region Name: [{row['REGION_NAME']}]()")
            md_file.new_line(f"* Region Number: {row['REGION_NUM']}")
            md_file.new_line(
                f"* Forest: [{capwords(row['FOREST_NAME'])}]({row['FOREST_URL']})"
            )
            md_file.new_line(f"* Ranger District: [{capwords(row['DISTRICT_NAME'])}]()")
            md_file.new_line("* Modules:")
            for module in sorted(row["MODULES"].split(",")):
                if module.strip() == "":
                    md_file.new_line("  - Unknown")
                else:
                    md_file.new_line(f"  - {module.strip()}")
            housing = (
                "Unknown" if len(row["HOUSING"]) == 0 else row["HOUSING"].capitalize()
            )
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

        def build_markdown(self, row):
            """
            [CONVERT] Generate a markdown file based on the given row data.

            Args:
                row (dict): A dictionary containing information for generating the markdown file.

            Returns:
                str: The generated markdown file.
            """
            md_file = self.v2.generate_markdown_page(
                file_name=self.v1.file_path_formatter(row),
                title=capwords(row["LOCATION"]),
                author="Big Ernie",
            )
            self.v1.add_information_section(md_file, row)
            self.v1.add_notes_section(md_file, row)
            return md_file

    class v2:
        def generate_md_page(file_name, title, author) -> str:
            """
            Generates a markdown page with the given file name, title, and author.

            Args:
                file_name (str): The file name for the generated markdown file.
                title (str): The title for the markdown page.
                author (str): The author of the markdown page.

            Returns:
                str: The path of the generated markdown file.
            """
            md_file = MdUtils(file_name=file_name, title=title, author=author)
            md_file.create_md_file()
            return md_file.file_name

        def generate_md_link(md_file: MdUtils, link: str, text: str) -> MdUtils:
            """
            Generates a markdown-formatted link and adds it to the given Markdown file.

            Args:
                md_file (MdUtils): The `MdUtils` object to which the link will be added.
                link (str): The URL for the link.
                text (str): The text to display for the link.

            Returns:
                MdUtils: The `MdUtils` object with the link added.
            """
            md_file.new_inline_link(text, link)
            return md_file

        def generate_md_list(md_file: MdUtils, item_list) -> MdUtils:
            """
            Generates a markdown-formatted list and adds it to the given Markdown file.

            Args:
                md_file (MdUtils): The `MdUtils` object to which the list will be added.
                item_list: A nested list representing the items of the markdown list.

            Returns:
                MdUtils: The `MdUtils` object with the list added.
            """
            md_file.new_list(item_list)

            return md_file
