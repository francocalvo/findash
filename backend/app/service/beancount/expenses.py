import duckdb
from typing import Any
from app.ledger import Ledger

# These utility functions should exist or be implemented elsewhere in your codebase:
# - create_table_from_types(table_name, con, types)
# - insert_rows(table_name, processed_rows, types, con)


def load_bc_data(
    query: str, table_name: str, ledger: Ledger, con: duckdb.DuckDBPyConnection
) -> None:
    """
    Load Beancount data into the database.
    """
    types, rows = ledger.run_query(query)

    # Create the table schema
    create_table_from_types(table_name, con, types)

    # Process and insert the rows
    processed_rows = []
    for row in rows:
        processed_row = {}
        for column_name, _ in types:
            value = getattr(row, column_name)
            if isinstance(value, (set, frozenset)):
                processed_row[column_name] = ",".join(sorted(value))
            else:
                processed_row[column_name] = value
        processed_rows.append(processed_row)

    insert_rows(table_name, processed_rows, types, con)


def load_expenses(ledger: Ledger, con: duckdb.DuckDBPyConnection) -> None:
    """
    Build the table in the database.
    """
    beancount_query = """
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

    load_bc_data(beancount_query, "expenses", ledger, con)
