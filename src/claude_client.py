import os
from typing import List, Dict, Any
from anthropic import Anthropic
from .utils import format_expense_data


def analyze_expenses(week_expenses: List[Dict[str, Any]], month_expenses: List[Dict[str, Any]]) -> str:
    """
    Send expense data to Claude and get spending analysis and insights.
    Returns formatted analysis string.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY must be set in .env")

    client = Anthropic()

    # Calculate totals
    week_total = sum(exp["amount"] for exp in week_expenses)
    month_total = sum(exp["amount"] for exp in month_expenses)

    # Build category breakdown for week
    week_by_category = {}
    for exp in week_expenses:
        cat = exp["category"]
        week_by_category[cat] = week_by_category.get(cat, 0) + exp["amount"]

    # Build category breakdown for month
    month_by_category = {}
    for exp in month_expenses:
        cat = exp["category"]
        month_by_category[cat] = month_by_category.get(cat, 0) + exp["amount"]

    # Format data for prompt
    week_data_str = format_expense_data(week_expenses)
    month_data_str = format_expense_data(month_expenses)

    prompt = f"""Analyze my spending and provide insights.

**Last 7 Days:**
Total: €{week_total:,.2f}
Breakdown by category:
{chr(10).join(f'- {cat}: €{amt:,.2f}' for cat, amt in week_by_category.items())}

**Month-to-Date:**
Total: €{month_total:,.2f}
Breakdown by category:
{chr(10).join(f'- {cat}: €{amt:,.2f}' for cat, amt in month_by_category.items())}

Please format response for Telegram with:
- Use *bold* for key numbers
- Use short sentences (max 15 words each)
- Structure with clear sections (use headers)
- Include: weekly summary, month summary, top spender, 2-3 savings tips
- Keep it concise and actionable
- Use emoji where appropriate (💰 💸 📊 ⚠️)

Make it visually clear and easy to scan."""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    return response.content[0].text
