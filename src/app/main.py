import asyncio
from twisted.internet import asyncioreactor
asyncioreactor.install(asyncio.get_running_loop())
import logging
from fastapi import FastAPI
from app.routes.scraping import router as scraping_router

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("Scraping API")

app = FastAPI(title="Footballer Scraper API")
app.include_router(scraping_router, prefix="/scrape")

logger.info("App Started Successfully!")

@app.get("/")
async def read_root():
    return {"message": "Hello, FastAPI!"}
