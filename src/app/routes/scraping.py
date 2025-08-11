from fastapi import APIRouter, Query
from app.services.scrapy_runner import run_spider


router = APIRouter(tags=["Scraping"])

@router.post("/start")
async def scrape(url: str = Query(...)):
    data = await run_spider(url)
    return {"scrape_count": len(data), "items": data}
