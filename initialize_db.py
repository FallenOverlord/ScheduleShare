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
            last_sign_in TEXT,
            consecutive_sign_in_days INTEGER DEFAULT 0,
            achievement_money_master BOOLEAN DEFAULT 0,
            achievement_leader_of_gang BOOLEAN DEFAULT 0,
            achievement_loyal_guarddog BOOLEAN DEFAULT 0,
            achievement_iron_determination BOOLEAN DEFAULT 0,
            achievement_social_king BOOLEAN DEFAULT 0,
            search_enabled BOOLEAN DEFAULT 1,
            view_email BOOLEAN DEFAULT 1,
            view_instagram BOOLEAN DEFAULT 1,
            view_timetable BOOLEAN DEFAULT 1
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
            coins INTEGER DEFAULT 0,
            consecutive_sign_in_days INTEGER DEFAULT 0,
            achievement_money_master BOOLEAN DEFAULT 0,
            achievement_leader_of_gang BOOLEAN DEFAULT 0,
            achievement_loyal_guarddog BOOLEAN DEFAULT 0,
            achievement_iron_determination BOOLEAN DEFAULT 0,
            achievement_social_king BOOLEAN DEFAULT 0,
            search_enabled BOOLEAN DEFAULT 1,
            view_email BOOLEAN DEFAULT 1,
            view_instagram BOOLEAN DEFAULT 1,
            view_timetable BOOLEAN DEFAULT 1
        )
    ''')
    # Create friends table
    c.execute('''
        CREATE TABLE IF NOT EXISTS friends (
            user TEXT,
            friend TEXT,
            PRIMARY KEY (user, friend)
        )
    ''')

    # Add new columns if they do not exist
    columns = [
        "coins", "last_sign_in", "achievement_money_master", "achievement_leader_of_gang",
        "achievement_loyal_guarddog", "achievement_iron_determination", "achievement_social_king"
    ]
    for column in columns:
        try:
            c.execute(f'ALTER TABLE users ADD COLUMN {column} INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass
        try:
            c.execute(f'ALTER TABLE profiles ADD COLUMN {column} INTEGER DEFAULT 0')
        except sqlite3.OperationalError:
            pass

    conn.commit()
    conn.close()

if __name__ == "__main__":
    update_db()
