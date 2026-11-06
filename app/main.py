import sys
import asyncio

if sys.platform == "win32":
    # Uvicorn explicitly forces SelectorEventLoop on Windows, which breaks Playwright.
    # We monkey-patch it here so Uvicorn uses ProactorEventLoop instead.
    asyncio.WindowsSelectorEventLoopPolicy = asyncio.WindowsProactorEventLoopPolicy
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

from fastapi import FastAPI
from app.api.chat import router as chat_router
from app.api.memory import router as memory_router

app = FastAPI(title="FRIDAY API")

# Register our API routers
app.include_router(chat_router, prefix="/api")
app.include_router(memory_router, prefix="/api/memory", tags=["Memory"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
