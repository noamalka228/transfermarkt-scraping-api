from fastapi import FastAPI
from app.routes.scraping import router as scraping_router

app = FastAPI()
app.include_router(scraping_router)


@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
