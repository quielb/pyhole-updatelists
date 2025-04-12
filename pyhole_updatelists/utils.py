import re


def is_regex(pattern):
    """
    Checks if the given string contains special characters using regex.

    Args:
        text: The input string.

    Returns:
        True if the string contains special characters, False otherwise.
    """
    regex = re.compile(r"[^a-zA-Z0-9\.\s]")
    if regex.search(pattern) is not None:
        return True
    return False


def string_to_bool(s):
    if isinstance(s, bool):
        return s
    if s.lower() == "false":
        return False
    return True


def strip_comments(text: str) -> str:
    """
    Removes comments (lines starting with #) from a string.
    """
    lines = text.splitlines()
    cleaned_lines = []
    for line in lines:
        if line == "":
            continue
        cleaned_line = re.sub(r"#.*", "", line).strip()
        if cleaned_line != "":
            cleaned_lines.append(cleaned_line)
    return "\n".join(cleaned_lines)
