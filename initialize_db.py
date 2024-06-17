import sqlite3

def initialize_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            email TEXT,
            name TEXT,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
