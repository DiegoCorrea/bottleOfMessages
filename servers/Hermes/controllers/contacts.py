import sqlite3
import sys
sys.path.append('..')
from time import gmtime, strftime

def create(user_id, contact_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (user_id, contact_id, created_at)
        VALUES (?, ?, ?);
    """, (user_id, contact_id, strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    conn.commit()
    conn.close()

def all(user_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts
        WHERE user_id = ?;
    """, (user_id,))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data

def findBy_ID(user_id, contact_id):
    conn = sqlite3.connect('./db/whatsApp.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts
        WHERE user_id = ? AND contact_id = ?;
    """, (user_id, contact_id,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data
