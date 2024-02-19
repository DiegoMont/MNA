from os import path
import pickle
import unittest

from hospitality import Customer

TEST_CUSTOMER_NAME = "Mario"


class TestCustomer(unittest.TestCase):
    def test_create_customer(self):
        c = Customer(TEST_CUSTOMER_NAME)
        c_file = c.serialized_filename
        self.assertTrue(path.isfile(c_file))
        c = None
        with open(c_file, "rb") as f:
            reloaded_c = pickle.load(f)
        self.assertEqual(reloaded_c.get_name(), TEST_CUSTOMER_NAME)

    def test_delete_customer(self):
        customer = Customer("")
        customer_file = customer.serialized_filename
        customer.delete()
        self.assertFalse(path.isfile(customer_file))

    def test_display_information(self):
        customer = Customer(TEST_CUSTOMER_NAME)
        display_information = str(customer)
        self.assertTrue(TEST_CUSTOMER_NAME in display_information)

    def test_modify(self):
        customer = Customer(TEST_CUSTOMER_NAME)
        new_name = "Luigi"
        customer.set_name(new_name)
        c_file = customer.serialized_filename
        self.assertTrue(path.isfile(c_file))
        with open(c_file, "rb") as f:
            updated_customer = pickle.load(f)
        self.assertEqual(updated_customer.get_name(), new_name)
