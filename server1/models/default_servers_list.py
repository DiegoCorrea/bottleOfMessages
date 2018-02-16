import sqlite3
import sys

from time import gmtime, strftime
from config.server import SERVER_DB_PATH


def create(
    name,
    ip,
    port
):
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO default_servers_list (name, ip, port)
        VALUES (?, ?, ?);
    """, (
            name,
            ip,
            port,
        )
    )
    conn.commit()
    conn.close()


def all():
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM default_servers_list;
    """)
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    return [
        {
            'name': data[0],
            'ip': data[1],
            'port': data[2],
            'succession_order': data[3]
        } for data in itens
    ]


def clean():
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM default_servers_list;
    """, )
    conn.commit()
    conn.close()
