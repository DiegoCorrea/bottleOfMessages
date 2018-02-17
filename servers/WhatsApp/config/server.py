KING = "King"
WORKER = "Worker"
WHO_AM_I = {
    "name": "WhatsApp",
    "db-name": 'WhatsApp.db',
    "ip": "127.0.0.1",
    "port": 27003,
    "position": WORKER,
    "succession_order": 3
}

LIVE_STATUS = 'live'
DEATH_STATUS = 'dinosaur'
ROUND_TIME = 10
SERVER_DB_PATH = './db/servers.db'
APP_DB_PATH = './db/' + WHO_AM_I['db-name']

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
