import sqlite3
from datetime import datetime

def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn

def initialize_coins(username, amount=100):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET coins = ? WHERE username = ?', (amount, username))
    conn.commit()
    conn.close()

def get_coins(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT coins FROM users WHERE username = ?', (username,))
    coins = c.fetchone()[0]
    conn.close()
    return coins

def add_coins(username, amount):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET coins = coins + ? WHERE username = ?', (amount, username))
    conn.commit()
    conn.close()

def daily_sign_in(username):
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.today().date()
    c.execute('SELECT last_sign_in FROM users WHERE username = ?', (username,))
    last_sign_in = c.fetchone()[0]
    
    if last_sign_in is None or datetime.strptime(last_sign_in, '%Y-%m-%d').date() < today:
        add_coins(username, 10)  # Add 10 coins for daily sign-in
        c.execute('UPDATE users SET last_sign_in = ? WHERE username = ?', (today, username))
        conn.commit()
    conn.close()
