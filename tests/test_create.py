# -*- coding: utf-8 -*-
import csv
import os

import pytest

from csv2md.create import MDLinkGenerator, convert


def test_convert(tmpdir):
    """
    Test the convert function.
    """

    # Test case 1: CSV file with headers, create directories
    csv_file_path = tmpdir.join("test.csv")
    csv_file_path.write("Name,Description\nJohn,Doe\nJane,Smith")

    output_dir = tmpdir.mkdir("output")

    csv_headers = True
    create_directories = True

    convert(
        csv_file_path,
        csv_headers,
        output_dir,
        create_directories,
        verbose=False,
        very_verbose=False,
    )

    # Assert
    assert len(output_dir.listdir()) == 2

    # Test case 2: CSV file without headers, don't create directories
    csv_headers = False
    create_directories = False

    convert(
        csv_file_path,
        csv_headers,
        output_dir,
        create_directories,
    )

    # Assert
    assert len(output_dir.listdir()) == 2

    # Test case 3: Non-existent CSV file
    non_existent_csv_file = tmpdir.join("non_existent.csv")

    with pytest.raises(FileNotFoundError):
        convert(
            non_existent_csv_file,
            csv_headers,
            output_dir,
            create_directories,
        )

    # Test case 4: CSV file with errors
    invalid_csv_file = tmpdir.join("invalid.csv")
    invalid_csv_file.write("1,2,3\n4,5")

    with pytest.raises(csv.Error):
        convert(
            invalid_csv_file,
            csv_headers,
            output_dir,
            create_directories,
        )

    # Test case 5: Generic exception while converting
    with pytest.raises(Exception, match="Exception while converting"):
        convert(
            csv_file_path,
            csv_headers,
            output_dir,
            create_directories,
        )


def test_md_link_generator(tmpdir):
    """
    Test the MDLinkGenerator class.
    """

    # Test case 1: Generate MD link file with default parameters
    md_link_generator = MDLinkGenerator()
    md_link_generator.generate_md_link_file(tmpdir)

    # Assert
    expected_md_file_path = os.path.join(tmpdir, "about.md")
    assert os.path.isfile(expected_md_file_path)

    with open(expected_md_file_path, "r") as md_file:
        content = md_file.read()
        assert "# About" in content
        assert "## Files" in content
        assert "[test.csv](test.csv)" in content

    # Test case 2: Generate MD link file with custom parameters
    md_link_generator = MDLinkGenerator(
        file_name="links.md", title="Links", author="John Doe"
    )
    md_link_generator.generate_md_link_file(tmpdir)

    # Assert
    expected_md_file_path = os.path.join(tmpdir, "links.md")
    assert os.path.isfile(expected_md_file_path)

    with open(expected_md_file_path, "r") as md_file:
        content = md_file.read()
        assert "# Links" in content
        assert "## Files" in content
        assert "[test.csv](test.csv)" in content
