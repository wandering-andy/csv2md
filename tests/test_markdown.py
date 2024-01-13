# -*- coding: utf-8 -*-
import os

import pytest
from mdutils.mdutils import MdUtils

from csv2md.markdown import (
    generate_markdown_file,
    generate_markdown_header,
    generate_markdown_list,
    generate_markdown_list_linked,
    generate_markdown_page,
)


@pytest.fixture
def markdown_file(tmp_path):
    file_path = os.path.join(tmp_path, "test.md")
    title = "Test Title"
    author = "Test Author"

    markdown_file = generate_markdown_file(file_path, title, author)
    return markdown_file


def test_generate_markdown_page(tmp_path):
    markdown_file_path = generate_markdown_page()
    assert os.path.exists(markdown_file_path)
    assert os.path.basename(markdown_file_path) == "README.md"


def test_generate_markdown_file(markdown_file):
    assert isinstance(markdown_file, MdUtils)
    assert markdown_file.file_name.endswith("test.md")
    assert markdown_file.title == "Test Title"
    assert markdown_file.author == "Test Author"


def test_generate_markdown_header(markdown_file):
    generate_markdown_header(markdown_file)

    with open(markdown_file.file_name, "r") as f:
        content = f.read()

    assert "# This is the Header" in content


def test_generate_markdown_list_linked(markdown_file):
    generate_markdown_list_linked(markdown_file)

    with open(markdown_file.file_name, "r") as f:
        content = f.read()

    assert "- [Link 1](http://example.com/link1)" in content
    assert "- [Link 2](http://example.com/link2)" in content


def test_generate_markdown_list(markdown_file):
    items = ["Item 1", "Item 2", "Item 3"]
    generate_markdown_list(markdown_file, items)

    with open(markdown_file.file_name, "r") as f:
        content = f.read()

    assert "- Item 1" in content
    assert "- Item 2" in content
    assert "- Item 3" in content
