import sqlite3
import uuid

from time import gmtime, strftime
from config.server import APP_DB_PATH


def createChat(
    user_id,
    contact_id,
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
            INSERT INTO chats (id, user_id, contact_id, created_at)
            VALUES (?, ?, ?, ?)
        """, (
                _id,
                user_id,
                contact_id,
                created_at,
            )
        )
        conn.commit()
        conn.close()
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def allUserChat(user_id):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chats
            WHERE user_id = ? OR contact_id = ?;
        """, (user_id, user_id,))
        itens = cursor.fetchall()
        conn.close()
        if itens is None:
            return []
        data = []
        for linha in itens:
            data.append(linha)
        return data
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def getChatWith(user_id, contact_id):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chats
            WHERE (
                user_id = ? AND contact_id = ?) OR (user_id = ? AND contact_id = ?
            );
        """, (user_id, contact_id, contact_id, user_id,))
        data = cursor.fetchone()
        conn.close()
        if data is None:
            return []
        return data
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def getMessages(chat_id, limit=20):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chat_messages
            WHERE chat_id = ?
            ORDER BY date(created_at) DESC Limit ?;
        """, (chat_id, limit))
        itens = cursor.fetchall()
        conn.close()
        if itens is None:
            return []
        data = []
        for linha in itens:
            data.append(linha)
        return data
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def sendMessage(
    chat_id,
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
            INSERT INTO chat_messages (id, chat_id, sender_id, message, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (
                _id,
                chat_id,
                sender_id,
                message,
                created_at
            )
        )
        conn.commit()
        conn.close()
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def chats_atRound(_roundStarted, _roundFinished):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chats
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
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []


def messages_atRound(_roundStarted, _roundFinished):
    try:
        conn = sqlite3.connect(APP_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM chat_messages
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
    except Exception as 2:
        logging.error(' ^^^^^ Model Error ^^^^^ ')
        logging.error('error({0}): {1}'.format(e.errno, e.strerror))
        return []
