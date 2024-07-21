import httpx
from bs4 import BeautifulSoup
from typing import List, Optional
from pydantic import BaseModel
import aiofiles
import asyncio
import os
import json

class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str

class Scraper:
    def __init__(self, base_url: str, proxy: Optional[str] = None):
        self.base_url = base_url
        self.proxy = proxy
        self.client = httpx.AsyncClient(proxies=self.proxy)
        
    async def fetch_page(self, page_num: int):
        url = f"{self.base_url}?page={page_num}"
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.text
        except httpx.HTTPStatusError:
            await asyncio.sleep(5)
            return await self.fetch_page(page_num)

    async def parse_page(self, page_content: str) -> List[Product]:
        soup = BeautifulSoup(page_content, 'html.parser')
        products = []
        for item in soup.select('.product'):
            title = item.select_one('.woo-loop-product__title').text.strip()
            price = float(item.select_one('.woocommerce-Price-amount').text.strip().replace('₹', '').replace(',', ''))
            image_url = item.select_one('.mf-product-thumbnail img').get('src')
            print(image_url, price, title)
            image_path = await self.download_image(image_url)
            products.append(Product(product_title=title, product_price=price, path_to_image=image_path))
        return products

    async def download_image(self, url: str) -> str:
        response = await self.client.get(url)
        file_path = f"images/{os.path.basename(url)}"
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        async with aiofiles.open(file_path, 'wb') as f:
            await f.write(response.content)
        return file_path

    async def scrape(self, num_pages: int) -> List[Product]:
        tasks = [self.fetch_page(page) for page in range(1, num_pages + 1)]
        pages = await asyncio.gather(*tasks)
        products = []
        for page_content in pages:
            products.extend(await self.parse_page(page_content))
        await self.client.aclose()
        self.save_to_file(products)
        return products

    def save_to_file(self, products: List[Product]):
        file_path = "products.json"
        with open(file_path, 'w') as f:
            json.dump([product.dict() for product in products], f, indent=4)
        print(f"Data saved to {file_path}")
