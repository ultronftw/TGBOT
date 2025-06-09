



import os
from telegram.ext import CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import get_pending_orders, update_order_status, get_db, get_user, update_credits
from config import get_plans

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
    try:
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
    except Exception as e:
        update.message.reply_text(f'Error fetching pending orders: {e}')

def stats(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.message.reply_text('Unauthorized.')
        return
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT COUNT(*) FROM users')
        users = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM orders WHERE status='confirmed'")
        confirmed_orders = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM orders WHERE status='pending'")
        pending_orders = c.fetchone()[0]
        c.execute('SELECT SUM(amount) FROM orders WHERE status="confirmed"')
        total_sales = c.fetchone()[0] or 0
        conn.close()
        update.message.reply_text(
            f'Users: {users}\nConfirmed Orders: {confirmed_orders}\nPending Orders: {pending_orders}\nTotal Sales: ${total_sales}'
        )
    except Exception as e:
        update.message.reply_text(f'Error fetching stats: {e}')

def confirm_payment(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.callback_query.answer('Unauthorized.')
        return
    query = update.callback_query
    order_id = int(query.data.split(':')[1])
    try:
        # Get order details
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT user_id, plan FROM orders WHERE order_id=?', (order_id,))
        row = c.fetchone()
        conn.close()
        if not row:
            query.edit_message_text(f'Order #{order_id} not found.')
            return
        user_id, plan_name = row
        # Deliver credits and expiry
        plans = get_plans()
        plan = next((p for p in plans if p['name'] == plan_name), None)
        if not plan:
            query.edit_message_text(f'Plan not found for order #{order_id}.')
            return
        # Calculate expiry
        from datetime import datetime, timedelta
        duration = plan.get('duration', '10 Days')
        days = int(duration.split()[0])
        expiry = (datetime.utcnow() + timedelta(days=days)).strftime('%Y-%m-%d')
        credits = plan['credits'] if isinstance(plan['credits'], int) else 9999999
        update_credits(user_id, credits, plan=plan['name'], expiry=expiry)
        update_order_status(order_id, 'confirmed')
        query.edit_message_text(f'Order #{order_id} confirmed. Credits delivered.')
        # Notify user
        try:
            context.bot.send_message(
                chat_id=user_id,
                text=f'Your KeyGenie order #{order_id} is confirmed!\nPlan: {plan["name"]}\nCredits: {plan["credits"]}\nExpiry: {expiry}'
            )
        except Exception as e:
            pass  # User may have blocked bot
    except Exception as e:
        query.edit_message_text(f'Error confirming order: {e}')

def reject_payment(update, context):
    if update.effective_user.id != ADMIN_USER_ID:
        update.callback_query.answer('Unauthorized.')
        return
    query = update.callback_query
    order_id = int(query.data.split(':')[1])
    try:
        # Get user_id for notification
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT user_id FROM orders WHERE order_id=?', (order_id,))
        row = c.fetchone()
        conn.close()
        update_order_status(order_id, 'rejected')
        query.edit_message_text(f'Order #{order_id} rejected.')
        if row:
            user_id = row[0]
            try:
                context.bot.send_message(
                    chat_id=user_id,
                    text=f'Your KeyGenie order #{order_id} was rejected. Please check your payment and try again.'
                )
            except Exception:
                pass
    except Exception as e:
        query.edit_message_text(f'Error rejecting order: {e}')
