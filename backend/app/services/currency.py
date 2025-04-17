"""Currency conversion utilities."""

from collections.abc import Sequence
from typing import Any

from app.models import TransactionBase


class CurrencyService:
    """Service for handling currency conversions."""

    def convert_amount(
        self, amount: float, from_currency: str, to_currency: str
    ) -> float:
        """Convert an amount from one currency to another."""
        # TODO: Implement actual conversion logic
        # For now, using placeholder conversion rates
        if from_currency == to_currency:
            return amount

        rates = {
            "ARS_TO_USD": 0.0012,  # Example rate
            "USD_TO_ARS": 850,  # Example rate
            "ARS_TO_CARS": 1.20,  # Example rate - cARS is ARS adjusted for inflation
        }

        if from_currency == "ARS" and to_currency == "USD":
            return amount * rates["ARS_TO_USD"]
        elif from_currency == "USD" and to_currency == "ARS":
            return amount * rates["USD_TO_ARS"]
        elif from_currency == "ARS" and to_currency == "cARS":
            return amount * rates["ARS_TO_CARS"]

        return amount

    def convert_transaction(
        self, transaction: TransactionBase, currencies: list[str]
    ) -> dict[str, Any]:
        """Convert a transaction's amounts to requested currencies."""
        result = transaction.model_dump()

        # Add converted amounts for each requested currency
        for currency in currencies:
            if currency != "ARS" and currency in ["USD", "cARS"]:
                result[f"amount_{currency.lower()}"] = self.convert_amount(
                    transaction.amount_ars, "ARS", currency
                )

        return result

    def convert_transactions(
        self, transactions: Sequence[TransactionBase], currencies: list[str]
    ) -> list[dict[str, Any]]:
        """Convert a list of transactions to requested currencies."""
        return [self.convert_transaction(t, currencies) for t in transactions]


currency_service = CurrencyService()
