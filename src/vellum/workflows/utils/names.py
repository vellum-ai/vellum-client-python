import re


def pascal_to_title_case(pascal_str: str) -> str:
    # Insert space before each capital letter (except the first one)
    title_case_str = re.sub(r"(?<!^)(?=[A-Z])", " ", pascal_str)

    # Return the result in title case
    return title_case_str.title()


def snake_to_title_case(snake_str: str) -> str:
    return pascal_to_title_case(snake_str.replace("_", " "))
