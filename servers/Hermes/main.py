import logging
import logging.config
import threading
import time
import os

from datetime import datetime
from time import gmtime, strftime

from server import ServerService
from rpyc.utils.server import ThreadedServer

from logs.setup import setup_logging
from config.server import WHO_AM_I, ROUND_TIME, TIME_FORMAT, KING, WORKER

import controllers.syncContents as ContentSyncroniztion
import controllers.syncServers as ServerSyncronization

import models.round_times as Round_times_Model


def server_Syncronization():
    while True:
        time.sleep(ROUND_TIME)
        if WHO_AM_I["position"] == KING:
            ServerSyncronization.whoIsAlive()
            ServerSyncronization.sync_Servers_list()
            ContentSyncroniztion.start()
        elif WHO_AM_I['position'] == WORKER:
            lastRound = Round_times_Model.last()
            diffLastRound = (datetime.strptime(
                    strftime(
                        "%Y-%m-%d %H:%M:%S",
                        gmtime()
                    ), TIME_FORMAT
                    ) - datetime.strptime(
                        lastRound[1],
                        TIME_FORMAT
                    )).total_seconds()
            if diffLastRound > 3*ROUND_TIME:
                print (' >>>>>>>>>>> WHERE IS THE KING?')
                if not ServerSyncronization.theKingIsAlive():
                    ServerSyncronization.whoIsAlive()
                    ServerSyncronization.election()


if __name__ == "__main__":
    os.system('cls||clear')
    setup_logging()
    logging.info('*************** Iniciando Aplicacao ***************')
    logging.info('--------------- Iniciando Sincronização ---------------')
    SYNC = threading.Thread(target=server_Syncronization)
    SYNC.daemon = True
    SYNC.start()
    logging.info('--------------- Iniciando Servidor ---------------')
    SERVER = ThreadedServer(ServerService, port=WHO_AM_I['port'])
    SERVER.start()
    logging.info('*************** Finalizando Aplicacao ***************')
