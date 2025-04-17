"""Expense-related routes."""

from datetime import date, datetime

from fastapi import APIRouter, Query
from sqlmodel import func, select

from app.api.deps import SessionDep
from app.db.queries.expense_queries import (
    build_expense_aggregation_query,
    build_expense_query,
)
from app.models import ExpensePublic, ExpensesPublic

router = APIRouter(prefix="/expenses", tags=["expenses"])


@router.get("/", response_model=ExpensesPublic)
def get_expenses(
    session: SessionDep,
    from_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    to_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    currencies: list[str] = Query(["ARS"], description="Currencies to convert to"),
    category: str | None = Query(None, description="Filter by category"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
) -> ExpensesPublic:
    """Retrieve expenses with filtering and pagination."""
    # Build base query
    query = build_expense_query(
        from_date=from_date, to_date=to_date or datetime.now().date(), category=category
    )

    # Get total count for pagination
    count_query = select(func.count()).select_from(query.subquery())
    total_count = session.exec(count_query).one()

    # Apply pagination
    query = query.offset(skip).limit(limit)

    # Execute query
    expenses = session.exec(query).all()

    # Filter currencies in response
    expenses_data = []
    for expense in expenses:
        expense_dict = expense.model_dump()
        filtered_expense = {
            k: v
            for k, v in expense_dict.items()
            if not k.startswith("amount_")
            or any(k == f"amount_{curr.lower()}" for curr in currencies)
        }
        expenses_data.append(ExpensePublic(**filtered_expense))

    return ExpensesPublic(
        data=expenses_data,
        count=total_count,
        pagination={
            "skip": skip,
            "limit": limit,
            "total_pages": (total_count + limit - 1) // limit,
        },
    )


@router.get("/summary")
def get_expense_summary(
    session: SessionDep,
    from_date: date = Query(..., description="Start date (YYYY-MM-DD)"),
    to_date: date | None = Query(None, description="End date (YYYY-MM-DD)"),
    currencies: list[str] = Query(["ARS"], description="Currencies to convert to"),
    group_by: str = Query("category", description="Group by 'category' or 'month'"),
) -> dict:
    """Get expense summaries grouped by category or month."""
    query = build_expense_aggregation_query(
        from_date=from_date, to_date=to_date or datetime.now().date(), group_by=group_by
    )

    results = session.exec(query).all()

    # Convert currencies for aggregated amounts
    data = []
    for r in results:
        item = {group_by: r[0], "amount_ars": float(r[1] or 0)}

        # Filter currencies
        filtered_item = {
            k: v
            for k, v in item.items()
            if not k.startswith("amount_")
            or any(k == f"amount_{curr.lower()}" for curr in currencies)
        }
        data.append(filtered_item)

    return {
        "data": data,
        "period": {
            "from": from_date.isoformat(),
            "to": (to_date or datetime.now().date()).isoformat(),
        },
    }
