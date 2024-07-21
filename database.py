import json
from typing import List
from .scraper import Product

class Database:
    def __init__(self, file_path: str):
        self.file_path = file_path
    
    def save_products(self, products: List[Product]):
        data = [product.dict() for product in products]
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)
    
    def load_products(self) -> List[Product]:
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
            return [Product(**item) for item in data]
        except FileNotFoundError:
            return []
