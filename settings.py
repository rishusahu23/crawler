from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    base_url: str = "https://dentalstall.com/shop/"
    db_file: str = "products.json"
    token: str = "your_static_token"
    proxy: Optional[str] = None  # Default is None    cache_host: str = "localhost"
    cache_host: str = "localhost"
    cache_port: int = 11211

settings = Settings()
