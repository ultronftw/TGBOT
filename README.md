# KeyGenie

KeyGenie is a comprehensive Telegram bot for selling digital service credits/keys. It features a clean, modern interface and supports manual crypto payments, user management, and admin controls.

## Features
- Interactive purchase flow with plan selection
- Manual payment verification (BTC, LTC, USDT)
- User profile and credit tracking
- Admin panel for order management
- SQLite database backend

## Setup
1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your details
3. Install dependencies: `pip install -r requirements.txt`
4. Run the bot: `python3 bot.py`

See [QUICK_START.md](QUICK_START.md) for a fast setup guide.

## Project Structure
- `bot.py` — Main bot application
- `config.py` — Configuration and message templates
- `database.py` — Database operations
- `admin.py` — Admin panel functionality
- `requirements.txt` — Dependencies
- `.env` — Environment variables
- `.env.example` — Environment template
- `README.md` — Full documentation
- `QUICK_START.md` — Quick setup guide
- `test_setup.py` — Verification script
- `demo.py` — Functionality demonstration
- `DELIVERY_SUMMARY.md` — Complete feature list

## License
MIT
