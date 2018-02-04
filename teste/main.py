import logging
import logging.config
import sys
import os
import json
from server import ServerService
from rpyc.utils.server import ThreadedServer
from config.server import WHO_AM_I

sys.path.append('..')


def setup_logging(
    default_path='logs/logging.json',
    default_level=logging.DEBUG,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    config = {}
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)


if __name__ == "__main__":
    os.system('cls||clear')
    setup_logging()
    logging.info('*************** Iniciando Aplicacao ***************')
    t = ThreadedServer(ServerService, port=WHO_AM_I['port'])
    t.start()
    logging.info('*************** Finalizando Aplicacao ***************')
