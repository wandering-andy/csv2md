def replace_spaces(text: str) -> str:
    """
    Replaces spaces in a string with hyphens and removes dots.
    """
    return text.replace(" ", "-").replace(".", "").lower()
