"""Code to represent an hotel
"""

import os

from . import utils


class Hotel:
    """Represents an hotel.
    """
    def __init__(self, name: str, rating: float, location: str):
        self.__name: str = name
        self.__rating: float = rating
        self.__location: str = location
        self.serialized_filename: str = utils.create_random_filename("hotel")
        self.__rooms: list[dict] = []
        self.__total_rooms: int = 0
        utils.serialize_object(self, self.serialized_filename)

    def add_room(self, room_number: str, beds: int, max_occupants: int):
        """Adds room
        """
        new_room = {
            "beds": beds,
            "max_occupants": max_occupants,
            "room_number": room_number,
            "is_available": True}
        self.__rooms.append(new_room)
        self.__total_rooms = len(self.__rooms)
        utils.serialize_object(self, self.serialized_filename)

    def __str__(self) -> str:
        return f"{self.__name}\n" \
               f"{self.__rating}/5\n" \
               f"At: {self.__location}\n"

    def get_location(self) -> str:
        """Gets hotel location
        """
        return self.__location

    def set_location(self, new_location: str):
        """Location setter
        """
        self.__location = new_location
        utils.serialize_object(self, self.serialized_filename)

    def get_name(self) -> str:
        """Name getter
        """
        return self.__name

    def set_name(self, new_name: str):
        """Name setter
        """
        self.__name = new_name
        utils.serialize_object(self, self.serialized_filename)

    def get_rating(self) -> float:
        """Rating getter
        """
        return self.__rating

    def set_rating(self, new_rating: float):
        """Rating setter
        """
        self.__rating = new_rating
        utils.serialize_object(self, self.serialized_filename)

    def get_room(self, index: int) -> dict:
        """Gets room by index
        """
        return self.__rooms[index]

    def get_total_rooms(self) -> int:
        """Returns the count of rooms in the hotel
        """
        return self.__total_rooms

    def delete(self):
        """Deletes the existence of the object
        """
        os.remove(self.serialized_filename)
