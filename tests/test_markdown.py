from main import markdownify

def test_markdownify_name():
    # Test case for output type 'name'
    text = "Hello World"
    output_type = "name"
    expected_result = "Hello_World.md"
    assert markdownify(text, output_type) == expected_result

def test_markdownify_path():
    # Test case for output type 'path'
    text = "Hello World"
    output_type = "path"
    expected_result = "/Hello/World.md"
    assert markdownify(text, output_type) == expected_result

def test_markdownify_invalid_type():
    # Test case for invalid output type
    text = "Hello World"
    output_type = "invalid"
    expected_result = "Type left blank, type must be 'name' or 'path'."
    assert markdownify(text, output_type) == expected_result