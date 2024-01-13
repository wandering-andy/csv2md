# -*- coding: utf-8 -*-
import os

import pytest

from csv2md.create import MDLinkGenerator, convert


@pytest.mark.parametrize(
    "csv_headers, create_directories, expected_files",
    [
        (True, True, 2),  # Test case 1: CSV file with headers, create directories
        (
            False,
            False,
            2,
        ),  # Test case 2: CSV file without headers, don't create directories
    ],
)
def test_convert(tmpdir, csv_headers, create_directories, expected_files):
    """
    Test the convert function.
    """

    # Create a single CSV file for all test cases
    csv_file_path = tmpdir.join("test.csv")
    csv_file_path.write("Name,Description\nJohn,Doe\nJane,Smith")

    output_dir = tmpdir.mkdir("output")

    convert(
        csv_file_path,
        csv_headers,
        output_dir,
        create_directories,
        verbose=False,
        very_verbose=False,
    )

    # Assert
    assert len(os.listdir(output_dir)) == expected_files


@pytest.mark.parametrize(
    "input_url, expected_md_link",
    [
        (
            "https://www.example.com",
            "[Example](https://www.example.com)",
        ),  # Test case 1: Valid URL
        ("invalid_url", ""),  # Test case 2: Invalid URL
        ("", ""),  # Test case 3: Empty URL
    ],
)
def test_md_link_generator(input_url, expected_md_link):
    """
    Test the MDLinkGenerator class.
    """

    md_link_generator = MDLinkGenerator()
    md_link = md_link_generator.generate_link(input_url)

    # Assert
    assert md_link == expected_md_link
