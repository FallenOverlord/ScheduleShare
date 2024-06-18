import sqlite3

def update_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Create users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT,
            name TEXT,
            password TEXT
        )
    ''')
    # Create profiles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            instagram TEXT,
            timetable BLOB,
            photo BLOB
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
