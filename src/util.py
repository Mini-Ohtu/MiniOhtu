class UserInputError(Exception):
    pass

def validate_reference_title(title):
    if len(title) == 0:
        raise UserInputError("Title length can't be 0")

    if len(title) > 1000:
        raise UserInputError("Title length must be smaller than 1000")

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

def validate_todo(content):
    """
    Legacy validation kept for tests:
    todo content length must be between 4 and 100 characters.
    """
    if content is None:
        raise UserInputError("Todo cannot be empty")

    length = len(content)
    if length < 4 or length > 100:
        raise UserInputError("Todo length must be between 4 and 100 characters")
