from os import path
import pickle
import unittest

from hospitality import Hotel


TEST_HOTEL_NAME = "Hotel Inn"
TEST_HOTEL_RATING = 4.5
TEST_HOTEL_LOCATION = "Denver, Colorado, USA"

class TestHotel(unittest.TestCase):
    def test_create_hotel(self):
        hotel = Hotel(TEST_HOTEL_NAME, TEST_HOTEL_RATING, TEST_HOTEL_LOCATION)
        hotel_file = hotel.serialized_filename
        self.assertTrue(path.isfile(hotel_file))
        hotel = None
        with open(hotel_file, "rb") as f:
            reloaded_hotel = pickle.load(f)
        self.assertEqual(reloaded_hotel.get_name(), TEST_HOTEL_NAME)
        self.assertEqual(reloaded_hotel.get_rating(), TEST_HOTEL_RATING)
        self.assertEqual(reloaded_hotel.get_location(), TEST_HOTEL_LOCATION)

    def test_delete_hotel(self):
        hotel = Hotel('', 4.5, '')
        hotel_file = hotel.serialized_filename
        hotel.delete()
        self.assertFalse(path.isfile(hotel_file))

    def test_display_information(self):
        hotel = Hotel(TEST_HOTEL_NAME, TEST_HOTEL_RATING, TEST_HOTEL_LOCATION)
        display_information = str(hotel)
        self.assertTrue(TEST_HOTEL_NAME in display_information)
        self.assertTrue(TEST_HOTEL_LOCATION in display_information)

    def test_modify_information(self):
        hotel = Hotel(TEST_HOTEL_NAME, TEST_HOTEL_RATING, TEST_HOTEL_LOCATION)
        new_rating = 5
        new_name = "Hotel Deluxe"
        new_location = "Mexico, City"
        hotel.set_name(new_name)
        hotel.set_location(new_location)
        hotel.set_rating(new_rating)
        hotel_file = hotel.serialized_filename
        with open(hotel_file, "rb") as f:
            reloaded_hotel = pickle.load(f)
        self.assertEqual(reloaded_hotel.get_name(), new_name)
        self.assertEqual(reloaded_hotel.get_rating(), new_rating)
        self.assertEqual(reloaded_hotel.get_location(), new_location)

    def test_add_room(self):
        hotel = Hotel(TEST_HOTEL_NAME, TEST_HOTEL_RATING, TEST_HOTEL_LOCATION)
        hotel.add_room("111", 2, 4)
        self.assertEqual(hotel.get_total_rooms(), 1)
