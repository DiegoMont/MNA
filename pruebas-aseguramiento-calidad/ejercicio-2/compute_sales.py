"""This module can parse the product info of products stored as JSON files and
compute the total cost of product purchases stored in another JSON file
"""

import json
import sys
import time


class Sale:
    """Class that stores the purchased items in a sale. The `total_cost` class
    variable holds the total cost of all the purchases accross `Sale`
    instances.
    """
    total_cost = 0

    def __init__(self):
        self.total: float = 0

    def add_purchase(self, product: dict, quantity: int):
        """Computes the cost of the purchase and adds it to the `total_cost` of
        all `Sale`s
        """
        subtotal = product['price'] * quantity
        Sale.total_cost += subtotal
        self.total += subtotal

    def get_total(self) -> float:
        """Gets the total cost of the sale
        """
        return self.total


def load_products_file(file_path: str) -> dict[str, dict]:
    """Parses a JSON file containing info about products
    """
    products = {}
    with open(file_path, encoding="utf-8") as file:
        content = json.load(file)
    for product in content:
        products[product["title"]] = product
    return products


def load_sales_file(
        file_path: str,
        products: dict[str, dict]
        ) -> dict[int, Sale]:
    """Parses a JSON file containing info about sales
    """
    sales = {}
    with open(file_path, encoding="utf-8") as file:
        content = json.load(file)
    for purchase in content:
        if purchase["SALE_ID"] not in sales:
            sales[purchase["SALE_ID"]] = Sale()
        sale = sales[purchase["SALE_ID"]]
        try:
            purchased_product = products[purchase["Product"]]
            quantity = purchase["Quantity"]
            sale.add_purchase(purchased_product, quantity)
        except KeyError:
            print(f"No está registrado el producto {purchase['Product']}")
    return sales


if __name__ == "__main__":
    start = time.time()
    available_products = load_products_file(sys.argv[1])
    purchases = load_sales_file(sys.argv[2], available_products)
    elapsed_time = time.time() - start
    output = f"Total cost: ${Sale.total_cost:.2f}\n"
    output += f"EXECUTION TIME: {elapsed_time:10.3f}s"
    print(output)
    with open("SalesResults.txt", "w", encoding="utf-8") as results_file:
        results_file.write(output)
