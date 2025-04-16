import sentry_sdk
from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.ledger import Ledger
from app.core.config import settings
from app.core.db import SessionLocal
from app.service.beancount.sync import BeancountSyncService
from app.service.beancount.handlers import LedgerWatcher
from fastapi.routing import APIRoute
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


if settings.SENTRY_DSN and settings.ENVIRONMENT != "local":
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles FastAPI startup and shutdown events using the lifespan protocol.
    See: https://fastapi.tiangolo.com/advanced/events/#lifespan
    """
    ledger = Ledger(settings.LEDGER_PATH)
    db = SessionLocal()
    sync_service = BeancountSyncService(ledger, db)
    sync_service.sync_all()
    watcher = LedgerWatcher(settings.LEDGER_PATH, sync_service)
    watcher.start()
    app.state.ledger_watcher = watcher

    yield

    if app.state.ledger_watcher:
        app.state.ledger_watcher.stop()

# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)
