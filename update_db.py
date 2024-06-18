import sqlite3

def update_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    # Create profiles table
    c.execute('''
        CREATE TABLE IF NOT EXISTS profiles (
            username TEXT PRIMARY KEY,
            name TEXT,
            email TEXT,
            instagram TEXT,
            timetable BLOB
        )
    ''')
    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
