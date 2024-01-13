# -*- coding: utf-8 -*-
import os


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

    # TODO: add logging
    def generate_md_link_file(self, directory="."):
        """
        Generate a Markdown file with links to other files in the specified directory.

        Args:
            directory (str, optional): The directory to search for files. Defaults to ".".

        Returns:
            None
        """
        from csv2md.directory import Files as files
        from csv2md.markdown import MarkdownGenerator

        md_file = MarkdownGenerator.v2.generate_md_page(
            self.file_name, self.title, self.author
        )
        file_list = files.view_files(directory)

        for file in file_list:
            file_path = os.path.join(directory, file)
            file_link = f"[{file}]({file_path})"
            md_file.new_line(file_link)
