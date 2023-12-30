def replace_spaces(text: str) -> str:
    """
    Replaces spaces in the given text with hyphens and removes periods, converting the text to lowercase.

    Args:
        text (str): The input text to be processed.

    Returns:
        str: The processed text with spaces replaced by hyphens, periods removed, and converted to lowercase.

    Raises:
        None
    """
    return text.replace(" ", "-").replace(".", "").lower()
