LIVE_STATUS = 'live'
DEATH_STATUS = 'dinosaur'
ROUND_TIME = 3
SERVER_DB_PATH = './db/servers.db'

WHO_AM_I = {
    "name": "Thot",
    "db-name": 'Thot.db',
    "ip": "127.0.0.1",
    "port": 27001,
    "order": "Worker"
}

DEFAULT_SERVERS_LIST = [
    {
        "name": "Hermes",
        "db-name": 'Hermes.db',
        "ip": "127.0.0.1",
        "port": 27000,
        "order": "King",
        'status': ''
    }, {
        'status': '',
        'name': 'Exu',
        "db-name": "Exu.db",
        'ip': '127.0.0.1',
        'port': 27002,
        "order": "Worker"
    }
]
