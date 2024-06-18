import sqlite3
import pandas as pd

def backup_profiles():
    conn = sqlite3.connect('users.db')
    df = pd.read_sql_query('SELECT * FROM profiles', conn)
    conn.close()
    df.to_csv('profiles_backup.csv', index=False)

def restore_profiles():
    conn = sqlite3.connect('users.db')
    df = pd.read_csv('profiles_backup.csv')
    df.to_sql('profiles', conn, if_exists='replace', index=False)
    conn.close()

if __name__ == "__main__":
    backup_profiles()
