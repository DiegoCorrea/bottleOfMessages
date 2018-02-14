import sqlite3
import sys

from time import gmtime, strftime
from config.server import SERVER_DB_PATH

sys.path.append('..')


def create(_round):
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO round_times (_round, created_at)
        VALUES (?, ?);
    """, (
            _round,
            strftime(
                "%Y-%m-%d %H:%M:%S",
                gmtime()
            )
        )
    )
    conn.commit()
    conn.close()


def all():
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM round_times;
    """)
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data


def last():
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM round_times
        ORDER BY _round DESC LIMIT 1;
    """)
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data