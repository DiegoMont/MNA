"""Code to handle serialization of objects
"""
import os
from os import path
import pickle
import random
import string


def create_random_filename(subdirectory: str) -> str:
    """Creates a filename to store serialized objects
    """
    random_string = "".join(random.choices(string.ascii_lowercase, k=15))
    random_filename = path.join("serial", subdirectory,
                                f"{random_string}.pickle")
    return random_filename


def serialize_object(instance, destiny_path: str):
    """Saves object to file.

    Creates directories as necessary.
    """
    os.makedirs(path.dirname(destiny_path), exist_ok=True)
    with open(destiny_path, "wb") as f:
        pickle.dump(instance, f)
