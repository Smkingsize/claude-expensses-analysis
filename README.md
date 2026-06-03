# Expense Analysis Automation

Automatically analyze your Notion expenses weekly. Claude provides spending insights and savings suggestions. Results sent via Telegram every Sunday morning.

## How It Works

1. **Fetch** expenses from Notion database (last 7 days + month-to-date)
2. **Analyze** with Claude API for patterns and insights
3. **Send** formatted analysis to Telegram

## Setup

### 1. Create Accounts & Tokens

- **Notion**: Create integration at https://www.notion.so/my-integrations, share with your expenses database
- **Anthropic**: Get API key at https://console.anthropic.com/account/keys
- **Telegram**: Message `@BotFather` → `/newbot` → get token. Message your bot, call `https://api.telegram.org/bot{TOKEN}/getUpdates` for chat ID

### 2. Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and populate with your tokens.

### 3. Test Locally

```bash
python -m src.main
```

Check Telegram for the analysis message.

### 4. Deploy to GitHub

Push to GitHub. Add secrets in **Settings → Secrets and variables → Actions**:
- `NOTION_TOKEN`
- `NOTION_DATABASE_ID`
- `ANTHROPIC_API_KEY`
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_CHAT_ID`

Workflow runs automatically every Sunday 8am UTC.

## Notion Database Schema

Required columns: `Expense`, `Date`, `Amount`, `Category`, `Accounts`

## Project Structure

```
src/
  main.py              # Orchestration
  notion_client.py     # Fetch expenses
  claude_client.py     # Generate analysis
  telegram_client.py   # Send message
  utils.py             # Helpers
```
