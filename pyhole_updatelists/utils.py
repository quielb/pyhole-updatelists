import re


def is_valid_regex(pattern):
    try:
        re.compile(pattern)
        return True
    except re.error:
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
