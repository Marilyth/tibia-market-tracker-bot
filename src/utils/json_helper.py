import json


def object_to_json(obj, indent=None):
    """Convert an object to a JSON string.

    Args:
        obj (Any): The object to convert.
        indent (int, optional): The indentation level. Defaults to None.

    Returns:
        str: The JSON string.
    """
    return json.dumps(obj, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o), indent=indent)
