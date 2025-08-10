from fastapi import APIRouter, Query
from app.services.scrapy_runner import run_spider

router = APIRouter(tags=["Scraping"])

@router.post("/start")
def scrape(url: str = Query(...)):
    data = run_spider(url)  # blocks only this request until spider finishes
    return {"scrape_count": len(data), "items": data}
