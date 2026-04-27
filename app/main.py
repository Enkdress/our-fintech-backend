from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.db.seed import seed_system_categories
from app.db.session import create_db_and_tables, engine
from sqlmodel import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    with Session(engine) as session:
        seed_system_categories(session)
    yield


app = FastAPI(title=settings.app_name, debug=settings.debug, lifespan=lifespan)

app.include_router(v1_router, prefix=settings.api_v1_prefix)
