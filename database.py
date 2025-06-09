import sqlite3
import os
from datetime import datetime

DB_PATH = os.getenv('DB_PATH', 'keygenie.db')

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        credits INTEGER DEFAULT 0,
        expiry TEXT,
        plan TEXT
    )''')
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT,
        amount INTEGER,
        txid TEXT,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    # Transactions log
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        txid TEXT PRIMARY KEY,
        user_id INTEGER,
        order_id INTEGER,
        amount INTEGER,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )''')
    conn.commit()
    conn.close()

# User management
def add_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id, credits, expiry, plan FROM users WHERE user_id=?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_credits(user_id, credits, plan=None, expiry=None):
    conn = get_db()
    c = conn.cursor()
    if plan and expiry:
        c.execute('UPDATE users SET credits=?, plan=?, expiry=? WHERE user_id=?', (credits, plan, expiry, user_id))
    elif plan:
        c.execute('UPDATE users SET credits=?, plan=? WHERE user_id=?', (credits, plan, user_id))
    elif expiry:
        c.execute('UPDATE users SET credits=?, expiry=? WHERE user_id=?', (credits, expiry, user_id))
    else:
        c.execute('UPDATE users SET credits=? WHERE user_id=?', (credits, user_id))
    conn.commit()
    conn.close()

# Order management
def add_order(user_id, plan, amount, txid, status='pending'):
    conn = get_db()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute('''INSERT INTO orders (user_id, plan, amount, txid, status, created_at) VALUES (?, ?, ?, ?, ?, ?)''',
              (user_id, plan, amount, txid, status, created_at))
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id

def get_pending_orders():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT order_id, user_id, plan, amount, txid FROM orders WHERE status='pending'")
    orders = c.fetchall()
    conn.close()
    return orders

def update_order_status(order_id, status):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE orders SET status=? WHERE order_id=?', (status, order_id))
    conn.commit()
    conn.close()

# Transaction logging
def log_transaction(txid, user_id, order_id, amount, status):
    conn = get_db()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute('''INSERT OR REPLACE INTO transactions (txid, user_id, order_id, amount, status, created_at) VALUES (?, ?, ?, ?, ?, ?)''',
              (txid, user_id, order_id, amount, status, created_at))
    conn.commit()
    conn.close()
import os
from datetime import datetime

DB_PATH = os.getenv('DB_PATH', 'keygenie.db')

def get_db():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = get_db()
    c = conn.cursor()
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        credits INTEGER DEFAULT 0,
        expiry TEXT,
        plan TEXT
    )''')
    # Orders table
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        plan TEXT,
        amount INTEGER,
        txid TEXT,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id)
    )''')
    # Transactions log
    c.execute('''CREATE TABLE IF NOT EXISTS transactions (
        txid TEXT PRIMARY KEY,
        user_id INTEGER,
        order_id INTEGER,
        amount INTEGER,
        status TEXT,
        created_at TEXT,
        FOREIGN KEY(user_id) REFERENCES users(user_id),
        FOREIGN KEY(order_id) REFERENCES orders(order_id)
    )''')
    conn.commit()
    conn.close()

# User management
def add_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT OR IGNORE INTO users (user_id) VALUES (?)', (user_id,))
    conn.commit()
    conn.close()

def get_user(user_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT user_id, credits, expiry, plan FROM users WHERE user_id=?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def update_credits(user_id, credits, plan=None, expiry=None):
    conn = get_db()
    c = conn.cursor()
    if plan and expiry:
        c.execute('UPDATE users SET credits=?, plan=?, expiry=? WHERE user_id=?', (credits, plan, expiry, user_id))
    elif plan:
        c.execute('UPDATE users SET credits=?, plan=? WHERE user_id=?', (credits, plan, user_id))
    elif expiry:
        c.execute('UPDATE users SET credits=?, expiry=? WHERE user_id=?', (credits, expiry, user_id))
    else:
        c.execute('UPDATE users SET credits=? WHERE user_id=?', (credits, user_id))
    conn.commit()
    conn.close()

# Order management
def add_order(user_id, plan, amount, txid, status='pending'):
    conn = get_db()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute('''INSERT INTO orders (user_id, plan, amount, txid, status, created_at) VALUES (?, ?, ?, ?, ?, ?)''',
              (user_id, plan, amount, txid, status, created_at))
    order_id = c.lastrowid
    conn.commit()
    conn.close()
    return order_id

def get_pending_orders():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT order_id, user_id, plan, amount, txid FROM orders WHERE status='pending'")
    orders = c.fetchall()
    conn.close()
    return orders

def update_order_status(order_id, status):
    conn = get_db()
    c = conn.cursor()
    c.execute('UPDATE orders SET status=? WHERE order_id=?', (status, order_id))
    conn.commit()
    conn.close()

# Transaction logging
def log_transaction(txid, user_id, order_id, amount, status):
    conn = get_db()
    c = conn.cursor()
    created_at = datetime.utcnow().isoformat()
    c.execute('''INSERT OR REPLACE INTO transactions (txid, user_id, order_id, amount, status, created_at) VALUES (?, ?, ?, ?, ?, ?)''',
              (txid, user_id, order_id, amount, status, created_at))
    conn.commit()
    conn.close()
