from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .scraper import Scraper
from .database import Database
from .settings import settings

app = FastAPI()
security = HTTPBearer()

def authenticate(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials.credentials != settings.token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.post("/scrape")
async def scrape_data(num_pages: Optional[int] = 1, proxy: Optional[str] = None, credentials: HTTPAuthorizationCredentials = Depends(authenticate)):
    scraper = Scraper(settings.base_url, proxy or settings.proxy)
    products = await scraper.scrape(num_pages)
    
    db = Database(settings.db_file)
    existing_products = db.load_products()
    
    updated_count = 0
    for product in products:
        existing_product = next((p for p in existing_products if p.product_title == product.product_title), None)
        if not existing_product or existing_product.product_price != product.product_price:
            db.save_products(products)
            updated_count += 1

    print(f"Scraped {len(products)} products, {updated_count} updated in DB.")
    return {"message": f"Scraped {len(products)} products, {updated_count} updated in DB."}
