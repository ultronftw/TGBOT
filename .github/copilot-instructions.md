<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

This project is a Telegram bot called KeyGenie for selling digital service credits/keys.

**Coding Guidelines:**
- Use clean, modern messaging and ensure all references are to 'KeyGenie' only.
- Project structure includes: bot.py, config.py, database.py, admin.py, requirements.txt, .env, .env.example, README.md, QUICK_START.md, test_setup.py, demo.py, DELIVERY_SUMMARY.md.
- Use Python, SQLite, python-telegram-bot, and dotenv.
- No media assets are included by default.
- All user-facing messages should be clear, concise, and branded as KeyGenie.
- All code should be modular, readable, and follow PEP8 style.
- Use environment variables for sensitive data (tokens, admin ID, wallet addresses).
- Database operations must be safe and use parameterized queries.
- Admin features must be protected by admin user ID.
- All references to other brands (e.g., 'Trex Killer') must be replaced with 'KeyGenie'.

**Bot Features:**
- /start — Welcome message with branding.
- /cmds — List all available commands.
- /buy — Interactive purchase flow with plan selection.
- /info — Show user profile (credits and expiry).
- /help — Instructions on how to use the bot.
- /terms — Terms and conditions.
- /status — Fun status report.

**Admin Features:**
- /pending — View pending orders.
- /stats — Bot statistics.
- Inline buttons for confirming/rejecting payments.
- Automatic notifications for new orders.

**Database:**
- User management with credits tracking.
- Order management with status tracking.
- Transaction logging.
- Plan expiry management.

**Testing:**
- test_setup.py must verify all modules import and database initializes.

**Deployment:**
- Run the bot with `python3 bot.py` after configuring .env.

**Future Improvements:**
- Automated payment verification, analytics, web dashboard, multi-language, referral system, and more.
