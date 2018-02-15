import logging
import logging.config
import threading
import socket
import time
import rpyc
import json
import sys
import os
from server import ServerService
from rpyc.utils.server import ThreadedServer
from config.server import WHO_AM_I, ROUND_TIME
from time import gmtime, strftime
import controllers.chats as ChatController
import controllers.users as UserController
import controllers.groups as GroupController
import controllers.contacts as ContactController

import models.servers.default_servers_list as Default_list_Model
import models.servers.round_times as Round_times_Model

sys.path.append('..')


def server_sync_Users(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = UserController.atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ Users Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceCreateUser(
            email=item[0],
            name=item[1],
            created_at=item[2]
        )


def server_sync_Contacts(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = ContactController.atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ Contacts Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceAddContact(
            user_id=item[0],
            contact_id=item[1],
            created_at=item[2]
        )


def server_Syncronization():
    while True:
        time.sleep(ROUND_TIME)
        if WHO_AM_I["order"] == "King":
            _oldRound = Round_times_Model.last()
            Round_times_Model.create(
                    _round=(
                        int(
                            _oldRound[0]
                        ) + 1
                    ),
                    created_at=strftime(
                        "%Y-%m-%d %H:%M:%S",
                        gmtime()
                    )
            )
            _newRound = Round_times_Model.last()
            print ('&&&&& new round ' + str(_newRound))
            for server in Default_list_Model.all():
                try:
                    SERVERCONNECTION = rpyc.connect(
                        server[1],
                        server[2],
                        config={
                            'allow_public_attrs': True,
                            "allow_pickle": True
                        }
                    )
                    vote = SERVERCONNECTION.root.newRound(_newRound)
                    if not vote:
                        print ('Diferença no banco')
                    server_sync_Users(
                        SERVERCONNECTION,
                        _newRound,
                        _oldRound
                    )
                    server_sync_Contacts(
                        SERVERCONNECTION,
                        _newRound,
                        _oldRound
                    )
                    SERVERCONNECTION.close()
                except(socket.error, AttributeError, EOFError):
                    logging.error(
                        '+ + + + + + + + [CONNECTION ERROR] + + + + + + + +'
                    )
                    logging.error('Server: ' + server[0])
                    logging.error('IP: ' + server[1])
                    logging.error('Port:' + str(server[2]))
                print ('\n')


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
    logging.info('--------------- Iniciando Sincronização ---------------')
    SYNC = threading.Thread(target=server_Syncronization)
    SYNC.daemon = True
    SYNC.start()
    logging.info('--------------- Iniciando Servidor ---------------')
    SERVER = ThreadedServer(ServerService, port=WHO_AM_I['port'])
    SERVER.start()
    logging.info('*************** Finalizando Aplicacao ***************')
