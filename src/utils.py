from datetime import datetime, timedelta
from typing import Tuple


def get_week_date_range() -> Tuple[str, str]:
    """Return ISO date strings for last 7 days: (start_date, end_date)."""
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=7)
    return start_date.isoformat(), end_date.isoformat()


def get_month_start_date() -> str:
    """Return ISO date string for first day of current month."""
    today = datetime.now().date()
    month_start = today.replace(day=1)
    return month_start.isoformat()


def format_currency(amount: float) -> str:
    """Format amount as currency string in euros."""
    return f"€{amount:,.2f}"


def format_expense_data(expenses: list) -> str:
    """Format expense list for Claude prompt."""
    if not expenses:
        return "No expenses recorded."

    lines = []
    for exp in expenses:
        line = f"- {exp['date']}: {exp['expense_name']} ({exp['category']}) - {format_currency(exp['amount'])}"
        lines.append(line)
    return "\n".join(lines)
