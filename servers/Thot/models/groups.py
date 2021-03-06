import sqlite3
import logging
import uuid

from time import gmtime, strftime
from config.server import APP_DB_PATH


def create(
    group_name,
    _id=None,
    created_at=None
):
    try:
        if _id is None:
            _id = str(uuid.uuid4())[:8]
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
        """, (_id, group_name, created_at,))
        conn.commit()
        conn.close()
        return _id
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def findBy_ID(group_id):
    try:
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def allUsers(group_id):
    try:
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def userGroups(user_id):
    try:
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def addUser(
    user_id,
    group_id,
    _id=None,
    created_at=None
):
    try:
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
            INSERT INTO user_groups (id, user_id, group_id, created_at)
            VALUES (?, ?, ?, ?)
        """, (_id, user_id, group_id, created_at))
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def getMessages(group_id, limit=20):
    try:
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def sendMessage(
    group_id,
    sender_id,
    message,
    _id=None,
    created_at=None
):
    try:
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
            INSERT INTO group_messages (id, group_id, sender_id, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
                _id,
                group_id,
                sender_id,
                message,
                created_at
            )
        )
        conn.commit()
        conn.close()
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def groups_atRound(_roundStarted, _roundFinished):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM groups
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def usersAdd_atRound(_roundStarted, _roundFinished):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM user_groups
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def messages_atRound(_roundStarted, _roundFinished):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM group_messages
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
    except Exception as e:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []
