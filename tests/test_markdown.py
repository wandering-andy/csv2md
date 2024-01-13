# -*- coding: utf-8 -*-
import pytest
from csv2md.markdown import MarkdownGenerator


class MockMarkdownFile:
    def __init__(self):
        self.lines = []

    def new_line(self, line):
        self.lines.append(line)


@pytest.fixture
def markdown_generator():
    return MarkdownGenerator.v1()


def test_file_name_formatter(markdown_generator):
    row = {"CITY": "San Francisco", "STATE": "California"}
    expected_result = "San_Francisco_California.md"
    result = markdown_generator.file_name_formatter(row)
    assert result == expected_result


def test_file_path_formatter(markdown_generator):
    row = {"REGION_NUM": 1, "FOREST_NAME": "Forest", "DISTRICT_NAME": "District"}
    expected_result = "region-1/Forest/District"
    result = markdown_generator.file_path_formatter(row)
    assert result == expected_result


def test_add_information_section(markdown_generator):
    md_file = MockMarkdownFile()
    row = {
        "REGION_NAME": "Region",
        "REGION_NUM": 1,
        "FOREST_NAME": "Forest",
        "FOREST_URL": "http://example.com/forest",
        "DISTRICT_NAME": "District",
        "MODULES": "A,B,C",
        "HOUSING": "housing",
    }
    expected_lines = [
        "# Information",
        "* Region Name: [Region]()",
        "* Region Number: 1",
        "* Forest: [Forest](http://example.com/forest)",
        "* Ranger District: [District]()",
        "* Modules:",
        "  - A",
        "  - B",
        "  - C",
        "* Housing: Housing",
        "",
    ]

    markdown_generator.add_information_section(md_file, row)

    assert md_file.lines == expected_lines


def test_add_notes_section(markdown_generator):
    md_file = MockMarkdownFile()
    row = {"NOTES": "These are some notes."}
    expected_lines = ["## Notes", "These are some notes."]

    markdown_generator.add_notes_section(md_file, row)

    assert md_file.lines == expected_lines


def test_build_markdown(markdown_generator):
    row = {
        "CITY": "San Francisco",
        "STATE": "California",
        "REGION_NAME": "Region 1",
        "REGION_NUM": 1,
        "FOREST_NAME": "Forest",
        "FOREST_URL": "http://example.com/forest",
        "DISTRICT_NAME": "District",
        "MODULES": "A,B,C",
        "HOUSING": "housing",
        "NOTES": "These are some notes.",
    }
    expected_file_content = """# San Francisco, California

## Information
* Region Name: [Region 1]()
* Region Number: 1
* Forest: [Forest](http://example.com/forest)
* Ranger District: [District]()
* Modules:
  - A
  - B
  - C
* Housing: housing

## Notes
These are some notes.
"""
    markdown_file = markdown_generator.build_markdown(row)
    assert markdown_file.get_content() == expected_file_content


def test_format_data(markdown_generator):
    input_data = [
        {"CITY": "San Francisco", "STATE": "California"},
        {"CITY": "Los Angeles", "STATE": "California"},
        {"CITY": "New York", "STATE": "New York"},
    ]
    expected_output = [
        {
            "CITY": "San Francisco",
            "STATE": "California",
            "LOCATION": "San Francisco, California",
        },
        {
            "CITY": "Los Angeles",
            "STATE": "California",
            "LOCATION": "Los Angeles, California",
        },
        {"CITY": "New York", "STATE": "New York", "LOCATION": "New York, New York"},
    ]

    result = markdown_generator.format_data(input_data)
    assert result == expected_output


def test_format_data_empty_input(markdown_generator):
    input_data = []
    expected_output = []

    result = markdown_generator.format_data(input_data)
    assert result == expected_output


def test_format_data_missing_keys(markdown_generator):
    input_data = [
        {"CITY": "San Francisco", "STATE": "California"},
        {"CITY": "Los Angeles"},  # Missing "STATE" key
        {
            "CITY": "New York",
            "STATE": "New York",
            "POPULATION": 8.4,
        },  # Additional "POPULATION" key
    ]
    expected_output = [
        {
            "CITY": "San Francisco",
            "STATE": "California",
            "LOCATION": "San Francisco, California",
        },
        {"CITY": "New York", "STATE": "New York", "LOCATION": "New York, New York"},
    ]

    result = markdown_generator.format_data(input_data)
    assert result == expected_output


@pytest.mark.parametrize("generator", [MarkdownGenerator.v1(), MarkdownGenerator.v2()])
def test_format_data_invalid_input_type(generator: MarkdownGenerator):
    invalid_input = "Invalid input type"

    result = generator.format_data(invalid_input)
    assert result is None


def test_format_data_duplicate_keys(markdown_generator):
    input_data = [
        {"CITY": "San Francisco", "STATE": "California"},
        {"CITY": "Los Angeles", "STATE": "California"},
        {"CITY": "New York", "STATE": "New York"},
    ]
    expected_output = [
        {
            "CITY": "San Francisco",
            "STATE": "California",
            "LOCATION": "San Francisco, California",
        },
        {
            "CITY": "Los Angeles",
            "STATE": "California",
            "LOCATION": "Los Angeles, California",
        },
        {"CITY": "New York", "STATE": "New York", "LOCATION": "New York, New York"},
    ]

    result = markdown_generator.format_data(input_data)
    assert result == expected_output
