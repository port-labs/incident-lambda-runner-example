
import uuid


def generate_short_uuid():
    """
    Generates a random UUID and returns the first 10 characters.
    """
    return str(uuid.uuid4())
