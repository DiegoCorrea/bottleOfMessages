import sqlite3
import sys

from time import gmtime, strftime
from config.server import SERVER_DB_PATH


def all():
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM workers_servers_list;
    """)
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data


def findBy_name(name):
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM workers_servers_list WHERE name = ?;
    """, (name,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data


def employed(name, ip, port):
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO workers_servers_list (name, ip, port)
        VALUES (?, ?, ?);
    """, (
            name,
            ip,
            port,
        )
    )
    conn.commit()
    conn.close()


def clean():
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM workers_servers_list;
    """, )
    conn.commit()
    conn.close()
