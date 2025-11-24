class UserInputError(Exception):
    pass


def validate_reference_title(title):
    cleaned_title = (title or "").strip()
    if len(cleaned_title) == 0:
        raise UserInputError("Title length can't be 0")

    if len(cleaned_title) > 1000:
        raise UserInputError("Title length must be smaller than 1000")
    return cleaned_title


def validate_reference_year(year):
    """
    Accept year from form input, ensure it represents an integer, return parsed value.
    """
    if year is None:
        raise UserInputError("Year is required")

    year_str = str(year).strip()
    if not year_str:
        raise UserInputError("Year is required")

    try:
        return int(year_str)
    except ValueError:
        raise UserInputError("Year must be an integer")
