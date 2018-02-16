import sqlite3
import sys
import os
import inspect
from time import gmtime, strftime
from config.server import APP_DB_PATH, SERVER_DB_PATH

sys.path.append('..')

# conectando...
conn = sqlite3.connect(
    os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()
            )
        )
    ) + APP_DB_PATH[1:]
)
# definindo um cursor
cursor = conn.cursor()


print('Deletando Tabelas se Existe')
cursor.execute("""
    DROP TABLE IF EXISTS users;
""")
cursor.execute("""
    DROP TABLE IF EXISTS contacts;
""")
cursor.execute("""
    DROP TABLE IF EXISTS chats;
""")
cursor.execute("""
    DROP TABLE IF EXISTS chat_messages;
""")
cursor.execute("""
    DROP TABLE IF EXISTS groups;
""")
cursor.execute("""
    DROP TABLE IF EXISTS user_groups;
""")
cursor.execute("""
    DROP TABLE IF EXISTS group_messages;
""")
print('...Ok!')


# #########################################################3 #
# criando a tabela (schema)
print('Users')
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
        email CHAR(64) NOT NULL PRIMARY KEY,
        name VARCHAR(45) NOT NULL,
        created_at TEXT NOT NULL
);
""")
print('...Ok!')
print('Contacts')
cursor.execute("""
CREATE TABLE IF NOT EXISTS contacts (
        id CHAR(32) NOT NULL PRIMARY KEY,
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
        id CHAR(32) NOT NULL PRIMARY KEY,
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
        id CHAR(32) NOT NULL PRIMARY KEY,
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
        id CHAR(32) NOT NULL PRIMARY KEY,
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


# ##################################################################### #
print ('\n\n')
# conectando...
conn = sqlite3.connect(
    os.path.dirname(
        os.path.abspath(
            inspect.getfile(
                inspect.currentframe()
            )
        )
    ) + SERVER_DB_PATH[1:]
)
# definindo um cursor
cursor = conn.cursor()
print('Deletando Tabelas de Servers se Existe')
cursor.execute("""
    DROP TABLE IF EXISTS default_servers_list;
""")
cursor.execute("""
    DROP TABLE IF EXISTS worker_servers_list;
""")
cursor.execute("""
    DROP TABLE IF EXISTS suspect_servers_list;
""")
cursor.execute("""
    DROP TABLE IF EXISTS round_times;
""")
print('...Ok!')
print('Default Server List')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS default_servers_list (
        name CHAR(64) NOT NULL,
        ip VARCHAR(32) NOT NULL,
        port INTEGER NOT NULL,
        succession_order INTEGER NOT NULL
    );
""")
conn.commit()

cursor.execute("""
    INSERT INTO default_servers_list
        (ip, name, port, succession_order)
        VALUES ('127.0.0.1', 'Thot', 27001, 0);
""")
conn.commit()

cursor.execute("""
    INSERT INTO default_servers_list
        (ip, name, port, succession_order)
        VALUES ('127.0.0.1', 'Thot', 27001, 1);
""")
conn.commit()

cursor.execute("""
    INSERT INTO default_servers_list
        (ip, name, port, succession_order)
        VALUES ('127.0.0.1', 'Exu', 27002, 2);
""")
conn.commit()
print('...OK!')

print('Worker Server List')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS workers_servers_list (
        name CHAR(64) NOT NULL,
        ip VARCHAR(32) NOT NULL,
        port INTEGER NOT NULL,
        succession_order INTEGER NOT NULL
    );
""")
conn.commit()
print('...OK!')

print('Suspect Server List')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS suspects_servers_list (
        name CHAR(64) NOT NULL,
        ip VARCHAR(32) NOT NULL,
        port INTEGER NOT NULL
    );
""")
conn.commit()
print('...OK!')

print('Round Times')
cursor.execute("""
    CREATE TABLE IF NOT EXISTS round_times (
        _round INTEGER NOT NULL PRIMARY KEY,
        created_at TEXT NOT NULL
    );
""")
conn.commit()

cursor.execute("""
    INSERT INTO round_times
        (_round, created_at)
        VALUES (?, ?);
""", (
        0,
        strftime(
            "%Y-%m-%d %H:%M:%S",
            gmtime()
        )
    )
)
conn.commit()
print('...OK!')
# desconectando...
conn.close()
