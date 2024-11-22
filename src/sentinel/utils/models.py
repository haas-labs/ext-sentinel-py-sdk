def scientific_notation_to_int(value) -> int:
    """
    Converts a value in scientific notation to an integer, if applicable.

    Args:
        value: The input value to parse.

    Returns:
        int: The parsed integer value.

    Raises:
        ValueError: If the value cannot be converted to an integer.
    """
    if isinstance(value, str) or isinstance(value, float):
        try:
            return int(float(value))
        except ValueError:
            raise ValueError(f"Value '{value}' cannot be converted to an integer")
    elif isinstance(value, int):
        return value
    raise ValueError(f"Invalid type for value: {type(value)}")
