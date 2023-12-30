# -*- coding: utf-8 -*-
import pytest

from csv2md.helpers import replace_spaces


# Happy path tests with various realistic test values
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        ("Hello World", "hello-world", "id=normal_case"),
        (
            "  Leading and trailing spaces  ",
            "--leading-and-trailing-spaces--",
            "id=leading_trailing_spaces",
        ),
        ("Periods... and spaces", "periods-and-spaces", "id=periods_and_spaces"),
        ("ALLCAPS", "allcaps", "id=all_caps"),
        ("", "", "id=empty_string"),
        ("NoSpacesOrPeriods", "nospacesorperiods", "id=no_spaces_or_periods"),
        ("123 456 789.", "123-456-789", "id=numeric_with_spaces_and_period"),
        (
            "Tabs\tand\nnewlines",
            "tabs\tand\nnewlines",
            "id=tabs_and_newlines_unchanged",
        ),
    ],
)
def test_replace_spaces_happy_path(input_text, expected_output):
    # Act
    result = replace_spaces(input_text)

    # Assert
    assert result == expected_output


# Edge cases
@pytest.mark.parametrize(
    "input_text, expected_output",
    [
        (" ", "-", "id=single_space"),
        (".", "", "id=single_period"),
        (" . ", "-", "id=space_period_space"),
        ("a" * 1000, "a" * 1000, "id=long_string"),
    ],
)
def test_replace_spaces_edge_cases(input_text, expected_output):
    # Act
    result = replace_spaces(input_text)

    # Assert
    assert result == expected_output


# Error cases are not applicable here since the function does not raise any exceptions
# and works with any string input. If non-string inputs were to be tested, they would
# result in a TypeError, but the function's type hint specifies the input must be a string.
