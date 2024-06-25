import sqlite3
from datetime import datetime
import streamlit as st

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

def use_coins(username, amount):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('UPDATE users SET coins = coins - ? WHERE username = ?', (amount, username))
    conn.commit()
    conn.close()

def daily_sign_in(username):
    conn = get_db_connection()
    c = conn.cursor()
    today = datetime.now().date()
    c.execute('SELECT last_sign_in, consecutive_sign_in_days FROM users WHERE username = ?', (username,))
    row = c.fetchone()

    if row:
        last_sign_in, consecutive_sign_in_days = row
        last_sign_in = datetime.strptime(last_sign_in, '%Y-%m-%d').date() if last_sign_in else None

        if last_sign_in is None or (today - last_sign_in).days > 1:
            consecutive_sign_in_days = 0

        if last_sign_in != today:
            consecutive_sign_in_days += 1
            c.execute('UPDATE users SET coins = coins + 10, last_sign_in = ?, consecutive_sign_in_days = ? WHERE username = ?', (today, consecutive_sign_in_days, username))
            conn.commit()

            # Check for achievements
            c.execute('SELECT coins, achievement_iron_determination FROM users WHERE username = ?', (username,))
            coins, iron_determination = c.fetchone()

            if coins >= 120:
                c.execute('UPDATE users SET achievement_money_master = 1 WHERE username = ?', (username,))
            
            if consecutive_sign_in_days >= 3 and not iron_determination:
                c.execute('UPDATE users SET achievement_iron_determination = 1 WHERE username = ?', (username,))
            
            conn.commit()
    conn.close()