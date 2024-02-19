from os import path
import pickle
import unittest

from hospitality import Hotel, Customer, Reservation


def get_test_hotel() -> Hotel:
    hotel = Hotel("Hotel Inn", 5, "Los Angeles, California, USA")
    hotel.add_room("111", 2, 4)
    return hotel

def get_test_customer() -> Customer:
    return Customer("Mario")


class TestReservation(unittest.TestCase):
    def test_create(self):
        hotel = get_test_hotel()
        customer = get_test_customer()
        reservation = Reservation(customer, hotel, 0)
        self.assertFalse(hotel.get_room(0)["is_available"])
        reservation_file = reservation.serialized_filename
        self.assertTrue(path.isfile(reservation_file))
        reservation = None
        with open(reservation_file, "rb") as f:
            reloaded_reservation = pickle.load(f)
        self.assertEqual(hotel.get_name(), reloaded_reservation.host.get_name())

    def test_cancel(self):
        hotel = get_test_hotel()
        customer = get_test_customer()
        ROOM_INDEX = 0
        reservation = Reservation(customer, hotel, ROOM_INDEX)
        reservation_file = reservation.serialized_filename
        reservation.cancel()
        self.assertFalse(path.isfile(reservation_file))
        self.assertTrue(hotel.get_room(ROOM_INDEX)["is_available"])
