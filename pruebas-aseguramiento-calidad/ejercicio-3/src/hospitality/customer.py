"""Code to create customers
"""
import os

from . import utils


class Customer:
    """Represents a customer
    """
    def __init__(self, name: str):
        self.__name: str = name
        aux = "customer"
        self.serialized_filename: str = utils.create_random_filename(aux)
        utils.serialize_object(self, self.serialized_filename)

    def delete(self):
        """Deletes the existence of the object
        """
        os.remove(self.serialized_filename)

    def get_name(self) -> str:
        """Name getter
        """
        return self.__name

    def set_name(self, new_name: str):
        """Name setter
        """
        self.__name = new_name
        utils.serialize_object(self, self.serialized_filename)

    def __str__(self) -> str:
        return self.__name
