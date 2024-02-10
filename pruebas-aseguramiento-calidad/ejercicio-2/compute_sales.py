import json
import sys


class Product:
    def __init__(
            self,
            title: str,
            type: str,
            description: str,
            filename: str,
            height: float,
            width: float,
            price: float,
            rating: int):
        self.title: str = title
        self.type: str = type
        self.description: str = description
        self.filename: str = filename
        self.height: float = height
        self.width: float = width
        self.price: float = price
        self.rating: int = rating


class ProductPurchase:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity


class Sale:
    total_cost = 0

    def __init__(self):
        self.purchased_products: dict[str, ProductPurchase] = {}
        self.total: float = 0

    def addPurchase(self, product: Product, quantity: int):
        if product not in self.purchased_products:
            self.purchased_products[product.title] = ProductPurchase(product, quantity)
        subtotal = product.price * quantity
        Sale.total_cost += subtotal
        self.total += subtotal


def load_products_file(file_path: str) -> dict[str, Product]:
    products = {}
    with open(file_path) as file:
        content = json.load(file)
    for object in content:
        products[object["title"]] = Product(**object)
    return products

def load_sales_file(file_path: str, products: dict[str, Product]) -> dict[int, Sale]:
    sales = {}
    with open(file_path) as file:
        content = json.load(file)
    for purchase in content:
        if purchase["SALE_ID"] not in sales:
            sales[purchase["SALE_ID"]] = Sale()
        sale = sales[purchase["SALE_ID"]]
        purchased_product = products[purchase["Product"]]
        quantity = purchase["Quantity"]
        sale.addPurchase(purchased_product, quantity)
    return sales

if __name__ == "__main__":
    products = load_products_file(sys.argv[1])
    sales = load_sales_file(sys.argv[2], products)
    print(Sale.total_cost)
