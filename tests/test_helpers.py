# -*- coding: utf-8 -*-
import pytest
from csv2md.helpers import replace_spaces, build_nested_list_from_csv


# Tests for replace_spaces function
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("Hello World", "hello-world"),
        ("  Leading and trailing spaces  ", "--leading-and-trailing-spaces--"),
        ("Periods... and spaces", "periods-and-spaces"),
        ("ALLCAPS", "allcaps"),
        ("", ""),
        ("NoSpacesOrPeriods", "nospacesorperiods"),
        ("123 456 789.", "123-456-789"),
        ("Tabs\tand\nnewlines", "tabs\tand\nnewlines"),
    ],
    ids=[
        "normal_case",
        "leading_trailing_spaces",
        "periods_and_spaces",
        "all_caps",
        "empty_string",
        "no_spaces_or_periods",
        "numeric_with_spaces_and_period",
        "tabs_and_newlines_unchanged",
    ],
)
def test_replace_spaces(input_text, expected_output):
    # Act
    result = replace_spaces(input_text)

    # Assert
    assert result == expected_output


# Tests for build_nested_list_from_csv function
def test_build_nested_list_from_csv(tmpdir):
    # Create a temporary CSV file for testing
    csv_file = tmpdir.join("test.csv")
    csv_file.write("1,2,3\n4,5,6\n7,8,9")

    # Test case 1: Read CSV file and build nested list
    expected_output = [["1", "2", "3"], ["4", "5", "6"], ["7", "8", "9"]]
    assert build_nested_list_from_csv(csv_file) == expected_output

    # Test case 2: Empty CSV file
    empty_csv_file = tmpdir.join("empty.csv")
    empty_csv_file.write("")
    expected_output = []
    assert build_nested_list_from_csv(empty_csv_file) == expected_output
