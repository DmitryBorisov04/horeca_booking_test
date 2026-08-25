from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.config import settings
from app.database import engine, Base
from app.api.bookings import router as bookings_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API для бронирования столиков в ресторане",
    lifespan=lifespan,
)

app.include_router(bookings_router)
