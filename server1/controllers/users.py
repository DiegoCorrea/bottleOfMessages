import sqlite3
import sys

from time import gmtime, strftime
from config.server import APP_DB_PATH

sys.path.append('..')


def create(
    email,
    name,
    created_at=None
):
    if created_at is None:
        created_at = strftime(
            "%Y-%m-%d %H:%M:%S",
            gmtime()
        )
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, name, created_at)
        VALUES (?, ?, ?);
    """, (
            email,
            name,
            created_at,
        )
    )
    conn.commit()
    conn.close()


def findBy_email(email):
    conn = sqlite3.connect(APP_DB_PATH)
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
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE email = ?;
    """, (user_id, ))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data


def atRound(_roundStarted, _roundFinished):
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users
        WHERE created_at BETWEEN ? AND ?;
    """, (_roundStarted, _roundFinished, )
    )
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data
