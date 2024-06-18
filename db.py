import sqlite3

def get_db_connection():
    conn = sqlite3.connect('users.db')
    return conn

def load_users():
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, email, name, password FROM users')
    rows = c.fetchall()
    conn.close()
    users = {
        'usernames': {}
    }
    for row in rows:
        users['usernames'][row[0]] = {
            'email': row[1],
            'name': row[2],
            'password': row[3]
        }
    return users

def save_user(username, email, name, password):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT INTO users (username, email, name, password) VALUES (?, ?, ?, ?)',
              (username, email, name, password))
    conn.commit()
    conn.close()

def save_profile(username, name, email, instagram, timetable):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO profiles (username, name, email, instagram, timetable) VALUES (?, ?, ?, ?, ?)',
              (username, name, email, instagram, timetable))
    conn.commit()
    conn.close()

def load_profile(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, name, email, instagram, timetable FROM profiles WHERE username=?', (username,))
    profile = c.fetchone()
    conn.close()
    return profile

def search_profiles(name):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, name, email, instagram FROM profiles WHERE name=?', (name,))
    profiles = c.fetchall()
    conn.close()
    return profiles
