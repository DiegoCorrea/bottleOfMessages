import sqlite3
import sys
sys.path.append('..')
from time import gmtime, strftime

def create(email, name):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, name, created_at, updated_at)
        VALUES (?, ?, ?, ?);
    """, (email, name, strftime("%Y-%m-%d %H:%M:%S", gmtime()), strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    conn.commit()
    conn.close()

def findBy_email(email):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE email = ?;
    """, (email,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data

def findBy_ID(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE email = ?;
    """, (user_id, ))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data
