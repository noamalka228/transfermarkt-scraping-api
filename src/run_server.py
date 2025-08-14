import asyncio, sys, uvicorn

if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

uvicorn.run("app.main:app", app_dir="src", reload=False, workers=1)
