# Configuration and message templates for KeyGenie
import os

BOT_NAME = "KeyGenie"

WELCOME_MSG = f"""
👋 Welcome to {BOT_NAME}!
Your trusted genie for digital credits and keys.
Type /cmds to see all commands.
"""

COMMANDS_LIST = """
Available Commands:
/start — Welcome message
/cmds — List all commands
/buy — Purchase credits/keys
/info — Your profile
/help — How to use KeyGenie
/terms — Terms and conditions
/status — Fun status report
"""

HELP_MSG = """
How to use KeyGenie:
1. Use /buy to purchase credits or keys.
2. Follow the instructions to complete your payment.
3. Submit your TXID for admin verification.
4. Receive your credits/keys after confirmation.
"""

TERMS_MSG = """
Terms & Conditions:
- All sales are final.
- No refunds after delivery.
- Misuse will result in a ban.
"""

STATUS_MSG = "KeyGenie is running smoothly! 🧞‍♂️✨"

# Payment addresses
BTC_ADDRESS = os.getenv('BTC_ADDRESS', 'your_btc_address')
LTC_ADDRESS = os.getenv('LTC_ADDRESS', 'your_ltc_address')
USDT_ADDRESS = os.getenv('USDT_ADDRESS', 'your_usdt_address')

# Credit/Key plans
def get_plans():
    return [
        {"name": "Daily Plan", "price": 50, "credits": "Unlimited", "duration": "1 Day"},
        {"name": "Test Plan", "price": 10, "credits": 250, "duration": "10 Days"},
        {"name": "Minor Plan", "price": 20, "credits": 500, "duration": "10 Days"},
        {"name": "Basic Plan", "price": 40, "credits": 1000, "duration": "10 Days"},
        {"name": "Pro Plan", "price": 180, "credits": 5000, "duration": "20 Days"},
        {"name": "Premium Plan", "price": 250, "credits": "Unlimited", "duration": "30 Days"},
    ]

MINIMUM_PURCHASE = 400
