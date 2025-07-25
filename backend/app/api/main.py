from fastapi import APIRouter

from app.api.routes import accounts, analytics, items, login, private, transactions, users, utils
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(transactions.expenses.router)
api_router.include_router(transactions.income.router)
api_router.include_router(accounts.router)
api_router.include_router(analytics.router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private.router)
