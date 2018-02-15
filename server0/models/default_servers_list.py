import sqlite3
import sys

from time import gmtime, strftime
from config.server import SERVER_DB_PATH


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
    data = []
    for linha in itens:
        data.append(linha)
    return data
