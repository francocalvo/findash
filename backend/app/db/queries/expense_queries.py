"""Query builders for expense-related queries."""

from datetime import date
from typing import Any

from sqlmodel import func, select

from app.models import Expense


def build_expense_query(
    from_date: date,
    to_date: date | None = None,
    category: str | None = None,
) -> Any:
    """Build a query for filtering expenses."""
    query = select(Expense)

    # Apply date filters (from_date inclusive, to_date exclusive)
    query = query.where(Expense.date >= from_date.isoformat())
    if to_date:
        query = query.where(Expense.date < to_date.isoformat())

    # Apply category filter
    if category:
        query = query.where(Expense.category == category)

    return query


def build_expense_aggregation_query(
    from_date: date, to_date: date | None = None, group_by: str = "category"
) -> Any:
    """Build a query for aggregating expenses."""
    if group_by == "category":
        query = select(
            Expense.category,
            func.sum(Expense.amount_ars).label("amount_ars"),
            func.sum(Expense.amount_usd).label("amount_usd"),
            func.sum(Expense.amount_cars).label("amount_cars"),
        ).group_by(Expense.category)
    else:  # group by month
        query = select(
            func.date_trunc("month", Expense.date).label("month"),
            func.sum(Expense.amount_ars).label("amount_ars"),
            func.sum(Expense.amount_usd).label("amount_usd"),
            func.sum(Expense.amount_cars).label("amount_cars"),
        ).group_by("month")

    # Apply date filters (from_date inclusive, to_date exclusive)
    query = query.where(Expense.date >= from_date.isoformat())
    if to_date:
        query = query.where(Expense.date < to_date.isoformat())

    return query
