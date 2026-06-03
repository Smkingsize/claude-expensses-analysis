import logging
from dotenv import load_dotenv
from .notion_client import get_week_expenses, get_month_expenses
from .claude_client import analyze_expenses
from .telegram_client import send_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def main():
    """Main orchestration function."""
    load_dotenv()

    logger.info("Starting weekly expense analysis...")

    try:
        logger.info("Fetching expenses from Notion...")
        week_expenses = get_week_expenses()
        month_expenses = get_month_expenses()
        logger.info(f"Fetched {len(week_expenses)} week expenses, {len(month_expenses)} month expenses")

        logger.info("Analyzing expenses with Claude...")
        analysis = analyze_expenses(week_expenses, month_expenses)

        logger.info("Sending analysis via Telegram...")
        success = send_message(analysis)

        if success:
            logger.info("Analysis sent successfully!")
        else:
            logger.error("Failed to send Telegram message")
            return 1

    except Exception as e:
        logger.error(f"Error during analysis: {e}", exc_info=True)
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
