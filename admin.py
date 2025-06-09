



# KeyGenie Admin Panel

# KeyGenie Admin Panel
import os
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_pending_orders, update_order_status, get_db

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
CONFIRM_PAYMENT = 'confirm_payment'
REJECT_PAYMENT = 'reject_payment'

def admin_handlers(app):
    app.add_handler(CommandHandler('pending', pending))
    app.add_handler(CommandHandler('stats', stats))
    app.add_handler(CallbackQueryHandler(confirm_payment, pattern=f'^{CONFIRM_PAYMENT}'))
    app.add_handler(CallbackQueryHandler(reject_payment, pattern=f'^{REJECT_PAYMENT}'))

def pending(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.message.reply_text('Unauthorized.')
        return
    orders = get_pending_orders()
    if not orders:
        update.message.reply_text('No pending orders.')
        return
    for order in orders:
        order_id, user_id, plan, amount, txid = order
        buttons = [
            [InlineKeyboardButton('Confirm', callback_data=f'{CONFIRM_PAYMENT}:{order_id}')],
            [InlineKeyboardButton('Reject', callback_data=f'{REJECT_PAYMENT}:{order_id}')]
        ]
        update.message.reply_text(
            f'Order #{order_id}\nUser: {user_id}\nPlan: {plan}\nAmount: {amount}\nTXID: {txid}',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def stats(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.message.reply_text('Unauthorized.')
        return
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM orders')
    orders = c.fetchone()[0]
    conn.close()
    update.message.reply_text(f'Users: {users}\nOrders: {orders}')

def confirm_payment(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.callback_query.answer('Unauthorized.')
        return
    query = update.callback_query
    order_id = int(query.data.split(':')[1])
    update_order_status(order_id, 'confirmed')
    query.edit_message_text(f'Order #{order_id} confirmed. Credits will be delivered.')

def reject_payment(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.callback_query.answer('Unauthorized.')
        return
    query = update.callback_query
    order_id = int(query.data.split(':')[1])
    update_order_status(order_id, 'rejected')
    query.edit_message_text(f'Order #{order_id} rejected.')

import os
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_pending_orders, update_order_status

ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
CONFIRM_PAYMENT = 'confirm_payment'
REJECT_PAYMENT = 'reject_payment'

def admin_handlers(app):
    app.add_handler(CommandHandler('pending', pending))
    app.add_handler(CommandHandler('stats', stats))
    app.add_handler(CallbackQueryHandler(confirm_payment, pattern=f'^{CONFIRM_PAYMENT}'))
    app.add_handler(CallbackQueryHandler(reject_payment, pattern=f'^{REJECT_PAYMENT}'))

def pending(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.message.reply_text('Unauthorized.')
        return
    orders = get_pending_orders()
    if not orders:
        update.message.reply_text('No pending orders.')
        return
    for order in orders:
        order_id, user_id, plan, amount, txid = order
        buttons = [
            [InlineKeyboardButton('Confirm', callback_data=f'{CONFIRM_PAYMENT}:{order_id}')],
            [InlineKeyboardButton('Reject', callback_data=f'{REJECT_PAYMENT}:{order_id}')]
        ]
        update.message.reply_text(
            f'Order #{order_id}\nUser: {user_id}\nPlan: {plan}\nAmount: {amount}\nTXID: {txid}',
            reply_markup=InlineKeyboardMarkup(buttons)
        )

def stats(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.message.reply_text('Unauthorized.')
        return
    from database import get_db
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM users')
    users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM orders')
    orders = c.fetchone()[0]
    conn.close()
    update.message.reply_text(f'Users: {users}\nOrders: {orders}')

def confirm_payment(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.callback_query.answer('Unauthorized.')
        return
    query = update.callback_query
    order_id = int(query.data.split(':')[1])
    update_order_status(order_id, 'confirmed')
    query.edit_message_text(f'Order #{order_id} confirmed. Credits will be delivered.')

def reject_payment(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.callback_query.answer('Unauthorized.')
        return
    query = update.callback_query
    order_id = int(query.data.split(':')[1])
    update_order_status(order_id, 'rejected')
    query.edit_message_text(f'Order #{order_id} rejected.')
