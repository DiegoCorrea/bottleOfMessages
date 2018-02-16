import sqlite3
import uuid
import sys

from time import gmtime, strftime
from config.server import APP_DB_PATH

sys.path.append('..')


def create(
    user_id,
    contact_id,
    _id=None,
    created_at=None
):
    if _id is None:
        _id = str(uuid.uuid4())
    if created_at is None:
        created_at = strftime(
            "%Y-%m-%d %H:%M:%S",
            gmtime()
        )
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contacts (id, user_id, contact_id, created_at)
        VALUES (?, ?, ?, ?);
    """, (_id, user_id, contact_id, created_at,))
    conn.commit()
    conn.close()


def all(user_id):
    conn = sqlite3.connect(APP_DB_PATH)
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
    conn = sqlite3.connect(APP_DB_PATH)
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
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM contacts
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
