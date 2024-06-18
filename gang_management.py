import sqlite3
import requests
from db import load_profile

def create_gang(gang_name, leader, logo_url, size):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO gangs (gang_name, leader, logo_url, size) VALUES (?, ?, ?, ?)', 
              (gang_name, leader, logo_url, size))
    conn.commit()
    conn.close()

def join_gang(gang_name, username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO gang_members (gang_name, username) VALUES (?, ?)', 
              (gang_name, username))
    c.execute('UPDATE gangs SET size = size + 1 WHERE gang_name = ?', (gang_name,))
    conn.commit()
    conn.close()

def search_gang(gang_name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM gangs WHERE gang_name = ?', (gang_name,))
    gang = c.fetchone()
    c.execute('SELECT username FROM gang_members WHERE gang_name = ?', (gang_name,))
    members = c.fetchall()
    conn.close()
    return gang, members

def generate_gang_logo(gang_name):
    # Dummy function to generate a logo URL based on the gang name
    response = requests.get(f"https://dummyimage.com/600x400/000/fff&text={gang_name}")
    return response.url

def get_gang_size(gang_name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT size FROM gangs WHERE gang_name = ?', (gang_name,))
    size = c.fetchone()
    conn.close()
    return size

def get_gang_members_profiles(gang_name):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT username FROM gang_members WHERE gang_name = ?', (gang_name,))
    members = c.fetchall()
    profiles = [load_profile(member[0]) for member in members]
    conn.close()
    return profiles