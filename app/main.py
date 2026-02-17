from fastapi import FastAPI

from .config import get_settings
from .database import Base, engine
from .routers import media

settings = get_settings()

app = FastAPI(title=settings.PROJECT_NAME)


@app.on_event("startup")
async def on_startup() -> None:
    # Ensure database tables are created
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.get("/health", tags=["health"])
async def health_check() -> dict:
    return {"status": "ok"}


app.include_router(media.router)


