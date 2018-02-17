KING = "King"
WORKER = "Worker"
WHO_AM_I = {
    "name": "Hermes",
    "db-name": 'Hermes.db',
    "ip": "192.168.0.16",
    "port": 27001,
    "position": WORKER,
    "succession_order": 1
}

LIVE_STATUS = 'live'
DEATH_STATUS = 'dinosaur'
ROUND_TIME = 10
SERVER_DB_PATH = './db/servers.db'
APP_DB_PATH = './db/' + WHO_AM_I['db-name']

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
