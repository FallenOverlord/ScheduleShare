import sqlite3
from ics_processing import extract_events, calculate_total_course_time

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
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    total_course_time = None
    if timetable:
        events, _ = extract_events(timetable)
        total_course_time = calculate_total_course_time(events)['Total Hours'].sum()
    c.execute('''
        INSERT OR REPLACE INTO profiles (username, name, email, instagram, timetable, total_course_time)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (username, name, email, instagram, timetable, total_course_time))
    conn.commit()
    conn.close()

def load_profile(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT username, name, email, instagram, timetable, total_course_time FROM profiles WHERE username=?', (username,))
    profile = c.fetchone()
    conn.close()
    return profile


def user_exists(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT 1 FROM users WHERE username = ?', (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def get_total_course_time(username):
    conn = get_db_connection()
    c = conn.cursor()
    c.execute('SELECT total_course_time FROM profiles WHERE username=?', (username,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None


def get_user_gangs(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT gang_name FROM gang_members WHERE username=?', (username,))
    gangs = c.fetchall()
    conn.close()
    return [gang[0] for gang in gangs]

def load_gang_members(username):
    gangs = get_user_gangs(username)
    gang_members = {}
    conn = get_db_connection()
    c = conn.cursor()
    for gang in gangs:
        c.execute('SELECT username FROM gang_members WHERE gang_name=?', (gang,))
        members = c.fetchall()
        gang_members[gang] = [member[0] for member in members]
    conn.close()
    return gang_members
