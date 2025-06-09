# KeyGenie Telegram Bot
# Main bot application

import logging
from config import BOT_NAME, WELCOME_MSG, COMMANDS_LIST, HELP_MSG, TERMS_MSG, STATUS_MSG
from database import init_db
from admin import admin_handlers
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
import os

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(WELCOME_MSG)

async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(COMMANDS_LIST)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MSG)

async def terms(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TERMS_MSG)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(STATUS_MSG)


# --- /buy command: Interactive purchase flow ---
from database import add_user, get_user, add_order, log_transaction, update_credits
from config import get_plans, BTC_ADDRESS, LTC_ADDRESS, USDT_ADDRESS, MINIMUM_PURCHASE

from telegram.ext import ConversationHandler, MessageHandler, filters

SELECT_PLAN, SELECT_PAYMENT, WAIT_TXID = range(3)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    plans = get_plans()
    buttons = [[InlineKeyboardButton(f"{p['name']} - ${p['price']}", callback_data=str(i))] for i, p in enumerate(plans)]
    reply_markup = InlineKeyboardMarkup(buttons)
    await update.message.reply_text("Select a plan:", reply_markup=reply_markup)
    return SELECT_PLAN

async def select_plan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    plan_idx = int(query.data)
    context.user_data['plan_idx'] = plan_idx
    plans = get_plans()
    plan = plans[plan_idx]
    payment_msg = f"You selected: {plan['name']} (${plan['price']})\nChoose payment method:"
    buttons = [
        [InlineKeyboardButton('BTC', callback_data='BTC')],
        [InlineKeyboardButton('LTC', callback_data='LTC')],
        [InlineKeyboardButton('USDT', callback_data='USDT')]
    ]
    await query.edit_message_text(payment_msg, reply_markup=InlineKeyboardMarkup(buttons))
    return SELECT_PAYMENT

async def select_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    method = query.data
    context.user_data['payment_method'] = method
    address = BTC_ADDRESS if method == 'BTC' else LTC_ADDRESS if method == 'LTC' else USDT_ADDRESS
    await query.edit_message_text(f"Send payment to this address:\n<code>{address}</code>\nAfter payment, send your TXID.", parse_mode='HTML')
    return WAIT_TXID

async def wait_txid(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    txid = update.message.text.strip()
    plan_idx = context.user_data['plan_idx']
    plans = get_plans()
    plan = plans[plan_idx]
    order_id = add_order(user_id, plan['name'], plan['price'], txid, status='pending')
    log_transaction(txid, user_id, order_id, plan['price'], 'pending')
    await update.message.reply_text("Thank you! Your order is pending admin confirmation. You'll be notified soon.")
    # Notify admin
    admin_id = int(os.getenv('ADMIN_USER_ID', '0'))
    context.bot.send_message(
        chat_id=admin_id,
        text=f"New order pending:\nUser: {user_id}\nPlan: {plan['name']}\nAmount: {plan['price']}\nTXID: {txid}"
    )
    return ConversationHandler.END

# --- /info command: Show user profile ---
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)
    if not user:
        await update.message.reply_text("No profile found. Use /buy to get started!")
        return
    _, credits, expiry, plan = user
    msg = f"<b>KeyGenie Profile</b>\nPlan: {plan or 'None'}\nCredits: {credits}\nExpiry: {expiry or 'N/A'}"
    await update.message.reply_text(msg, parse_mode='HTML')

def main():
    init_db()
    token = os.getenv('BOT_TOKEN')
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('cmds', cmds))
    app.add_handler(CommandHandler('help', help_cmd))
    app.add_handler(CommandHandler('terms', terms))
    app.add_handler(CommandHandler('status', status))
    app.add_handler(CommandHandler('info', info))
    # /buy conversation
    buy_conv = ConversationHandler(
        entry_points=[CommandHandler('buy', buy)],
        states={
            SELECT_PLAN: [CallbackQueryHandler(select_plan)],
            SELECT_PAYMENT: [CallbackQueryHandler(select_payment)],
            WAIT_TXID: [MessageHandler(filters.TEXT & ~filters.COMMAND, wait_txid)]
        },
        fallbacks=[]
    )
    app.add_handler(buy_conv)
    # Register admin handlers
    admin_handlers(app)
    app.run_polling()

if __name__ == '__main__':
    main()
