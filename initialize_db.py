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
            password TEXT,
            coins INTEGER DEFAULT 0,
            last_sign_in TEXT
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
            total_course_time INTEGER,
            coins INTEGER DEFAULT 0
        )
    ''')
    # Add total_course_time column if it does not exist
    try:
        c.execute('ALTER TABLE profiles ADD COLUMN total_course_time INTEGER')
    except sqlite3.OperationalError:
        # The column already exists
        pass

    # Add coins column if it does not exist
    try:
        c.execute('ALTER TABLE users ADD COLUMN coins INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        # The column already exists
        pass

    # Add last_sign_in column if it does not exist
    try:
        c.execute('ALTER TABLE users ADD COLUMN last_sign_in TEXT')
    except sqlite3.OperationalError:
        # The column already exists
        pass




    # Create gangs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS gangs (
            gang_name TEXT PRIMARY KEY,
            leader TEXT,
            logo_url TEXT,
            size INTEGER
        )
    ''')
    # Add logo_url and size columns if they do not exist
    try:
        c.execute('ALTER TABLE gangs ADD COLUMN logo_url TEXT')
    except sqlite3.OperationalError:
        # The column already exists
        pass

    try:
        c.execute('ALTER TABLE gangs ADD COLUMN size INTEGER')
    except sqlite3.OperationalError:
        # The column already exists
        pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
