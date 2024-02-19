"""Code to create reservations
"""
import os

from . import utils
from .customer import Customer
from .hotel import Hotel


class Reservation:
    """Create instances of room reservations
    """
    def __init__(self, customer: Customer, hotel: Hotel, room_index: int):
        self.customer: Customer = customer
        self.host: Hotel = hotel
        self.room: dict = hotel.get_room(room_index)
        self.room["is_available"] = False
        aux = "reservation"
        self.serialized_filename: str = utils.create_random_filename(aux)
        utils.serialize_object(self, self.serialized_filename)

    def cancel(self):
        """Deletes the existence of the object
        """
        self.room["is_available"] = True
        os.remove(self.serialized_filename)

    def __str__(self) -> str:
        return f"Reserved by {self.customer.get_name()}"
