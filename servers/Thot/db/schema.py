import sqlite3
import os
import inspect
# conectando...
conn = sqlite3.connect(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '/whatsApp.db')
# definindo um cursor
cursor = conn.cursor()

# criando a tabela (schema)
print('Users')
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
        email CHAR(64) NOT NULL PRIMARY KEY,
        name VARCHAR(45) NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL
);
""")
print('...Ok!')
print('Contacts')
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(64) NOT NULL,
        contact_id CHAR(32) NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(email),
        FOREIGN KEY(contact_id) REFERENCES users(email)
);
""")
print('...Ok!')
print('Chats')
cursor.execute("""
CREATE TABLE IF NOT EXISTS chats (
        id CHAR(32) NOT NULL PRIMARY KEY,
        user_id CHAR(64) NOT NULL,
        contact_id CHAR(64) NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(email),
        FOREIGN KEY(contact_id) REFERENCES users(email)
);
""")
print('...Ok!')
print('Chat Message')
cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        chat_id CHAR(32) NOT NULL,
        sender_id CHAR(64) NOT NULL,
        message TEXT NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(sender_id) REFERENCES users(email),
        FOREIGN KEY(chat_id) REFERENCES chats(id)
);
""")
print('...Ok!')
print('Groups ')
cursor.execute("""
CREATE TABLE IF NOT EXISTS groups (
        id CHAR(32) NOT NULL PRIMARY KEY,
        name CHAR(32) NOT NULL,
        created_at TEXT NOT NULL
);
""")
print('...Ok!')

print('Users Groups ')
cursor.execute("""
CREATE TABLE IF NOT EXISTS user_groups (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        user_id CHAR(64)NOT NULL,
        group_id CHAR(32) NOT NULL,
        created_at TEXT NOT NULL,
        FOREIGN KEY(user_id) REFERENCES users(id),
        FOREIGN KEY(group_id) REFERENCES groups(id)
);
""")
print('...OK!')
print('Group Messages')
cursor.execute("""
CREATE TABLE IF NOT EXISTS group_messages (
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
        sender_id CHAR(64) NOT NULL,
        group_id CHAR(32) NOT NULL,
        created_at TEXT NOT NULL,
        message TEXT NOT NULL,
        FOREIGN KEY(sender_id) REFERENCES users(id),
        FOREIGN KEY(group_id) REFERENCES groups(id)
);
""")
print('...OK!')
print('Tabelas criadas com sucesso.')
# desconectando...
conn.close()
