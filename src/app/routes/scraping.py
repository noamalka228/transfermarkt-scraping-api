import logging, asyncio
from fastapi import APIRouter, Query, status
from app.services.scrapy_runner import run_spider

logger = logging.getLogger("Scraping API")
router = APIRouter(tags=["Scraping"])

@router.post("/start")
async def scrape(url: str = Query(...)):
    logger.info("started crawling data")
    try:
        data = await asyncio.wait_for(run_spider(url), timeout=100)
    except asyncio.TimeoutError:
        return {"status": status.HTTP_408_REQUEST_TIMEOUT, "message": "Operation took too long"}
    return {"scrape_count": len(data), "items": data}
