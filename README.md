# Scraping Tool

## Description

This project is a web scraping tool built with FastAPI, BeautifulSoup, and aiohttp for scraping product data from an e-commerce website. It fetches product information from multiple pages and stores the data in a JSON file.

## Features

- Scrape product data including title, price, and image.
- Save scraped data to a JSON file.
- Supports authentication using tokens.
- Optionally uses a cache for storing product data.

## Requirements

- Python 3.8+
- Dependencies: `httpx`, `beautifulsoup4`, `pydantic-settings`, `aiofiles`, `fastapi`, `uvicorn`, `aiomcache`

## Setup

### 1. Clone the Repository

### 2. python -m venv myenv

### 3 source myenv/bin/activate

### 4. pip install -r requirements.txt

### 5. Run: uvicorn main:app --reload

### 6. Use curl to see output: curl -X POST "http://127.0.0.1:8000/scrape" -H "Authorization: Bearer your_static_token" -d "num_pages=1"

