import sqlite3
import sys

from time import gmtime, strftime
from config.server import WHO_AM_I

sys.path.append('..')


def create(
    user_id,
    contact_id,
    created_at=strftime(
        "%Y-%m-%d %H:%M:%S",
        gmtime()
    )
):
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (user_id, contact_id, created_at)
        VALUES (?, ?, ?);
    """, (user_id, contact_id, created_at))
    conn.commit()
    conn.close()


def all(user_id):
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
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
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
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


def atRound(_roundStarted, _roundFinished):
    conn = sqlite3.connect('./db/' + str(WHO_AM_I['db-name']))
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts WHERE created_at >= ? AND created_at < ?;
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
