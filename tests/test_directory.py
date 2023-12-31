# -*- coding: utf-8 -*-
import os

from csv2md.directory import file_search, view_files


def test_file_search_with_existing_file(capsys):
    directory = "/path/to/directory"
    file_name = "example.txt"
    sort = "name"
    file_search(directory, file_name, sort)
    captured = capsys.readouterr()
    expected_output = (
        f"File '{file_name}' found at: {os.path.join(directory, file_name)}\n"
    )
    assert captured.out == expected_output


def test_file_search_with_non_existing_file(capsys):
    directory = "/path/to/directory"
    file_name = "non_existing.txt"
    sort = "name"
    file_search(directory, file_name, sort)
    captured = capsys.readouterr()
    expected_output = f"File '{file_name}' not found in directory: {directory}\n"
    assert captured.out == expected_output


def test_view_files_sort_by_name(tmpdir):
    directory = tmpdir.strpath
    sort = "name"
    expected_files = ["file1.txt", "file2.txt", "file3.txt"]
    for file_name in expected_files:
        tmpdir.join(file_name).write("")
    files = view_files(directory, sort)
    assert files == sorted(expected_files)


# Add more test cases as needed
