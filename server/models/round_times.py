import sqlite3
import sys

from time import gmtime, strftime
from config.server import SERVER_DB_PATH



def create(
    _round,
    created_at=None
):
    if created_at is None:
        created_at = strftime(
            "%Y-%m-%d %H:%M:%S",
            gmtime()
        )
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO round_times (_round, created_at)
        VALUES (?, ?);
    """, (
            _round,
            created_at
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


def findBy_round(_round_id):
    conn = sqlite3.connect(SERVER_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM round_times
        WHERE _round = ?;
    """, (_round_id,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data
