import logging
from typing import Any

from sqlmodel import Session

from app.ledger import Ledger
from app.models import Expense, Income

logger = logging.getLogger(__name__)


class BeancountSyncService:
    def __init__(self, ledger: Ledger, db_session: Session):
        self.ledger = ledger
        self.db = db_session

    def _run_query_and_map(self, query: str, model_cls: type) -> list[Any]:
        """Execute Beancount query and map results to SQLModel instances."""
        res: tuple[list[tuple[str, type]], list[tuple]] = self.ledger.run_query(query)  # type: ignore
        types, rows = res

        col_names = [col[0] for col in types]
        logger.info(f"Loaded {len(rows)} rows. Columns: {col_names}")

        mapped = []
        for row in rows:
            row_dict = {}
            for idx, value in enumerate(row):
                column_name = col_names[idx]
                if isinstance(value, set | frozenset):
                    row_dict[column_name] = ",".join(sorted(value))
                else:
                    row_dict[column_name] = value
            mapped.append(model_cls(**row_dict))
        logger.info(f"Mapped {len(mapped)} rows.")
        return mapped

    def sync_table(self, query: str, model_cls: type) -> None:
        """Sync a table by truncating existing data and loading fresh data."""
        self.db.query(model_cls).delete()
        self.db.commit()
        objects = self._run_query_and_map(query, model_cls)
        self.db.bulk_save_objects(objects)
        self.db.commit()

    def sync_expenses(self) -> None:
        """Sync expenses from Beancount to database."""
        query = """
        SELECT
            date AS date,
            account AS account,
            LEAF(ROOT(account, 2)) as category,
            LEAF(ROOT(account, 3)) as subcategory,
            payee AS payee,
            narration AS narration,
            NUMBER(CONVERT(POSITION, 'ARS', DATE)) AS amount_ars,
            NUMBER(CONVERT(POSITION, 'USD', DATE)) AS amount_usd,
            tags
        WHERE account ~ '^Expenses'
        ORDER BY date DESC
        """
        self.sync_table(query, Expense)

    def sync_income(self) -> None:
        """Sync income from Beancount to database."""
        query = """
        SELECT
            date AS date,
            account AS account,
            LEAF(ROOT(account, 3)) AS origin,
            payee AS payee,
            narration AS narration,
            NUMBER(CONVERT(ABS(POSITION), 'ARS', DATE)) AS amount_ars,
            NUMBER(CONVERT(ABS(POSITION), 'USD', DATE)) AS amount_usd
        WHERE account ~ '^Income'
        ORDER BY date DESC
        """
        self.sync_table(query, Income)

    def sync_all(self) -> None:
        """Sync all tables from Beancount to database."""
        self.sync_expenses()
        self.sync_income()
