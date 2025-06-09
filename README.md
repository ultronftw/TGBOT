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

## Deployment

### Local
Run the bot with:
```bash
python3 bot.py
```
after configuring your `.env` file.

### Heroku
1. Commit all changes and push to GitHub.
2. Create a Heroku app and connect your GitHub repo.
3. Set your environment variables in the Heroku dashboard (Settings > Reveal Config Vars).
4. Deploy. Heroku will use the `Procfile` to start the bot.

### Vercel (Experimental)
> Note: Vercel is not ideal for long-running bots, but you can deploy for demo/testing.
1. Install Vercel CLI: `npm i -g vercel`
2. Run `vercel` and follow the prompts.
3. Set your environment variables in the Vercel dashboard.
4. The bot will attempt to start via `api/index.py`.

---
For both platforms, ensure your `.env` or environment variables are set correctly (see `.env.example`).

## License
MIT
