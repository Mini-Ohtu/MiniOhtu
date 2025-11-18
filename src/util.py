class UserInputError(Exception):
    pass

def validate_reference_title(title):
    if len(title) == 0:
        raise UserInputError("Title length can't be 0")

    if len(title) > 1000:
        raise UserInputError("Title length must be smaller than 1000")

def validate_reference_year(year):
    if isinstance(year, int) is False:
        raise UserInputError("Year must be int")