from fastapi import FastAPI
from app.routes.scraping import router as scraping_router

app = FastAPI(title="Footballer Scraper API")
app.include_router(scraping_router, prefix="/scrape")


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
