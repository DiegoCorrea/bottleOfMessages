import sqlite3
import uuid

from time import gmtime, strftime
from config.server import APP_DB_PATH


def create(
    group_name,
    group_id=None,
    created_at=None
):
    if group_id is None:
        group_id = str(uuid.uuid4())[:8]
    if created_at is None:
        created_at = strftime(
            "%Y-%m-%d %H:%M:%S",
            gmtime()
        )
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO groups (id, name, created_at)
        VALUES (?, ?, ?)
    """, (group_id, group_name, created_at))
    conn.commit()
    conn.close()
    return group_id


def findBy_ID(group_id):
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM groups
        WHERE id = ?;
    """, (group_id,))
    data = cursor.fetchone()
    conn.close()
    if data is None:
        return []
    return data


def allUsers(group_id):
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM user_groups
        WHERE group_id = ?;
    """, (group_id,))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data


def userGroups(user_id):
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM user_groups
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


def addUser(
    user_id,
    group_id,
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
        INSERT INTO user_groups (user_id, group_id, created_at)
        VALUES (?, ?, ?)
    """, (user_id, group_id, created_at))
    conn.commit()
    conn.close()


def getMessages(group_id, limit=20):
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM group_messages
        WHERE group_id = ?
        ORDER BY date(created_at) DESC Limit ?;
    """, (group_id, limit))
    itens = cursor.fetchall()
    conn.close()
    if itens is None:
        return []
    data = []
    for linha in itens:
        data.append(linha)
    return data


def sendMessage(group_id, sender_id, message, created_at=None):
    if created_at is None:
        created_at = strftime(
            "%Y-%m-%d %H:%M:%S",
            gmtime()
        )
    conn = sqlite3.connect(APP_DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO group_messages (group_id, sender_id, message, created_at)
        VALUES (?, ?, ?, ?)
    """, (
            group_id,
            sender_id,
            message,
            created_at
        )
    )
    conn.commit()
    conn.close()
