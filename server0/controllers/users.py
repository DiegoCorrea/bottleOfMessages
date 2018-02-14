import sqlite3
import sys

from time import gmtime, strftime
from config.server import WHO_AM_I

sys.path.append('..')


def create(
    email,
    name,
    created_at=strftime(
        "%Y-%m-%d %H:%M:%S",
        gmtime()
    )
):
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (email, name, created_at, updated_at)
        VALUES (?, ?, ?, ?);
    """, (
            email,
            name,
            created_at,
            created_at
        )
    )
    conn.commit()
    conn.close()


def findBy_email(email):
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
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
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
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
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM users WHERE created_at >= ? AND created_at < ?;
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
