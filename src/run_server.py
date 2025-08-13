import asyncio, sys, uvicorn, os

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# os.environ.setdefault("TWISTED_REACTOR", "twisted.internet.asyncioreactor.AsyncioSelectorReactor")

uvicorn.run("app.main:app", app_dir="src", reload=False, workers=1)