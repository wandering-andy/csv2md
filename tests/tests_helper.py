import pytest

def test_replace_spaces():
    assert replace_spaces("hello world") == "hello-world"
    assert replace_spaces("hello.world") == "helloworld"
    assert replace_spaces("hello  world") == "hello--world"
    assert replace_spaces("") == ""
