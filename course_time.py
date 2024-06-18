import sqlite3

def get_total_course_time(username):
    """Fetch the total course time for a specific user from the database."""
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    
    try:
        c.execute('SELECT total_course_time FROM profiles WHERE username = ?', (username,))
        result = c.fetchone()
        
        if result:
            return result[0]
        else:
            return None
    
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    
    finally:
        conn.close()
