"""Query builders for income-related queries."""

from datetime import date
from typing import Any

from sqlmodel import func, select

from app.models import Income


def build_income_query(
    from_date: date,
    to_date: date | None = None,
    origin: str | None = None,
) -> Any:
    """Build a query for filtering income."""
    query = select(Income)

    # Apply date filters
    query = query.where(Income.date >= from_date.isoformat())
    if to_date:
        query = query.where(Income.date <= to_date.isoformat())

    # Apply origin filter
    if origin:
        query = query.where(Income.origin == origin)

    return query


def build_income_aggregation_query(
    from_date: date, to_date: date | None = None, group_by: str = "origin"
) -> Any:
    """Build a query for aggregating income."""
    if group_by == "origin":
        query = select(
            Income.origin,
            func.sum(Income.amount_ars).label("total_ars"),
        ).group_by(Income.origin)
    else:  # group by month
        query = select(
            func.date_trunc("month", Income.date).label("month"),
            func.sum(Income.amount_ars).label("total_ars"),
        ).group_by("month")

    # Apply date filters
    query = query.where(Income.date >= from_date.isoformat())
    if to_date:
        query = query.where(Income.date <= to_date.isoformat())

    return query
