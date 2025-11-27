class UserInputError(Exception):
    pass


def validate_reference_title(title):
    cleaned_title = (title or "").strip()
    if len(cleaned_title) == 0:
        raise UserInputError("Title length can't be 0")

    if len(cleaned_title) > 1000:
        raise UserInputError("Title length must be smaller than 1000")
    return cleaned_title


def validate_reference_year(year, required=True):
    """
    Accept year from form input, ensure it represents an integer, return parsed value.
    If optional and empty, return None.
    """

    year_str = "" if year is None else str(year).strip()
    if not year_str:
        if required:
            raise UserInputError("Year is required")
        return None

    try:
        return int(year_str)
    except ValueError:
        raise UserInputError("Year must be an integer")
