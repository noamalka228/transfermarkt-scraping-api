import asyncio
from fastapi import APIRouter, Query, status
from app.services.scrapy_runner import run_spider


router = APIRouter(tags=["Scraping"])

@router.post("/start")
async def scrape(url: str = Query(...)):
    try:
        data = await asyncio.wait_for(run_spider(url), timeout=100)
    except asyncio.TimeoutError:
        return {"status": status.HTTP_408_REQUEST_TIMEOUT, "message": "Operation took too long"}
    return {"scrape_count": len(data), "items": data}
