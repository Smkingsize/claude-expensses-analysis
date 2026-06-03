import os
from typing import List, Dict, Any
import requests
from .utils import get_week_date_range, get_month_start_date


def fetch_expenses(date_filter_start: str, date_filter_end: str) -> List[Dict[str, Any]]:
    """
    Fetch expenses from Notion database within date range.
    Returns list of expense dicts with keys: date, amount, category, expense_name, account.
    """
    token = os.getenv("NOTION_TOKEN")
    database_id = os.getenv("NOTION_DATABASE_ID")

    if not token or not database_id:
        raise ValueError("NOTION_TOKEN and NOTION_DATABASE_ID must be set in .env")

    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }

    # Filter for date range
    payload = {
        "filter": {
            "and": [
                {
                    "property": "Date",
                    "date": {"on_or_after": date_filter_start},
                },
                {
                    "property": "Date",
                    "date": {"on_or_before": date_filter_end},
                },
            ]
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        response.raise_for_status()
    except requests.RequestException as e:
        raise RuntimeError(f"Failed to fetch expenses from Notion: {e}")

    data = response.json()
    expenses = []

    for result in data.get("results", []):
        props = result.get("properties", {})

        # Extract properties - adjust property names to match your Notion schema
        date_obj = props.get("Date", {}).get("date", {})
        date = date_obj.get("start") if date_obj else None

        amount_obj = props.get("Amount", {}).get("number")
        amount = amount_obj if amount_obj is not None else 0

        category_obj = props.get("Category", {}).get("select", {})
        category = category_obj.get("name") if category_obj else "Uncategorized"

        # Expense name is in "Expense" or "Name" property
        expense_name_obj = props.get("Expense", {}).get("title", [])
        if not expense_name_obj:
            expense_name_obj = props.get("Name", {}).get("title", [])
        expense_name = expense_name_obj[0].get("text", {}).get("content", "Unknown") if expense_name_obj else "Unknown"

        account_obj = props.get("Accounts", {}).get("select", {})
        account = account_obj.get("name") if account_obj else "Unknown"

        if date and amount:
            expenses.append({
                "date": date,
                "amount": amount,
                "category": category,
                "expense_name": expense_name,
                "account": account,
            })

    return expenses


def get_week_expenses() -> List[Dict[str, Any]]:
    """Fetch expenses from last 7 days."""
    start_date, end_date = get_week_date_range()
    return fetch_expenses(start_date, end_date)


def get_month_expenses() -> List[Dict[str, Any]]:
    """Fetch expenses from first day of month to today."""
    start_date = get_month_start_date()
    end_date = get_week_date_range()[1]
    return fetch_expenses(start_date, end_date)
