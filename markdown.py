from mdutils.mdutils import MdUtils
from python.csv2md.helpers import replace_spaces
from string import capwords
from main import os


def markdownify(text: str, output_type: str) -> str:
    """
    Converts text to markdown format based on the specified output type.

    Args:
        text: The input text.
        output_type: The type of output ('name' or 'path').

    Returns:
        The markdown-formatted text.
    """
    ext = ".md"
    text_list = [text]

    def markdown_path_formatter(text_list):
        for text in text_list:
            text_list.append(replace_spaces(text))
        return "/".join(text_list) + ext

    def markdown_file_name_formatter(text_list):
        for text in text_list:
            text_list.append(replace_spaces(text))

    if output_type == "name":
        return markdown_file_name_formatter(text_list)
    elif output_type == "path":
        return markdown_path_formatter(text_list)
    else:
        return "Type left blank, type must be 'name' or 'path'."


# TODO: rewrite most of this to possible be more generalized
def file_name_formatter(row):
    # TODO: This is going to need to be expanded so that it
    # returns a markdown file name based whatever strings are passed to it
    """
    Formats a file name based on the given row data.

    Parameters:
        row (dict): A dictionary containing the row data.

    Returns:
        str: The formatted file name.

    Example:
        >>> row = {'CITY': 'San Francisco', 'STATE': 'California'}
        >>> file_name_formatter(row)
        'San_Francisco_California.md'
        """
    ext = ".md"
    city_name = replace_spaces(row['CITY'])
    state_name = replace_spaces(row['STATE'])
    return f"{city_name}_{state_name}{ext}"


def file_path_formatter(row):
    region = f"region-{row['REGION_NUM']}"
    forest = replace_spaces(row['FOREST_NAME'])
    district = replace_spaces(row['DISTRICT_NAME'])
    return os.path.join(region, forest, district)


def add_information_section(md_file, row):
    md_file.new_line("# Information")
    md_file.new_line(f"* Region Name: [{row['REGION_NAME']}]()")
    md_file.new_line(f"* Region Number: {row['REGION_NUM']}")
    md_file.new_line(f"* Forest: [{capwords(row['FOREST_NAME'])}]({row['FOREST_URL']})")
    md_file.new_line(f"* Ranger District: [{capwords(row['DISTRICT_NAME'])}]()")
    md_file.new_line("* Modules:")
    for module in sorted(row['MODULES'].split(",")):
        if module.strip() == "":
            md_file.new_line("  - Unknown")
        else:
            md_file.new_line(f"  - {module.strip()}")
    housing = "Unknown" if len(row['HOUSING']) == 0 else row['HOUSING'].capitalize()
    md_file.new_line(f"* Housing: {housing}")
    md_file.new_line()


def add_notes_section(md_file, row):
    md_file.new_line("## Notes")
    md_file.new_paragraph(row['NOTES'])


def build_markdown(row):
    md_file = generate_markdown_file(file_name=file_path_formatter(row),
                                     title=capwords(row['LOCATION']),
                                     author="Big Ernie")
    add_information_section(md_file, row)
    add_notes_section(md_file, row)
    return md_file


# TODO: create folder structure given an input
# TODO: create about pages for every level of structure
# TODO: create index page
# TODO: inputs needed:
# TODO: Docstring as template?


def generate_markdown_page():
    # Create a new Markdown file
    mdFile = generate_markdown_file(file_name="README.md", title="title", author="author")

    # Add content to Markdown file
    generate_markdown_header(mdFile)
    generate_markdown_list(mdFile)

    # Write Markdown file
    writeMarkdownFile(mdFile)

    # Return full pile path to file
    return mdFile.file_path


def generate_markdown_header(mdFile):
    mdFile.write("# This is the Header\n\n")


# Add # Given file mdFile, add a new link link_name pointing to link_path
def generate_markdown_link(mdFile, link_path, link_name):
    return mdFile.new_inline_link(text=link_name, url=link_path)


def generate_markdown_list(mdFile, file_list):
    # TODO: search directory for files
    # TODO: add files to list
    for file in file_list:
        generate_markdown_link(mdFile=mdFile, link_path=file, link_name=file)
    # TODO: return list formatted as bulleted list of links
    return


def generate_markdown_file(file_name, title, author):
    mdFile = MdUtils(file_name=file_name,
                     title=title,
                     author=author)
    return mdFile


def writeMarkdownFile(mdFile):
    return mdFile.create_md_file()


def chooseTemplate(template_name):
    public = "template1"
    private = "template2"
    federal = "template3"
    state = "template4"

    location_stub = ""

    if template_name == "template1":
        return "template1"
    elif template_name == "template2":
        return "template2"
    else:
        return "template1"
