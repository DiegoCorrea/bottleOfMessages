import logging
import logging.config
import threading
import socket
import time
import rpyc
import json
import os
from server import ServerService
from rpyc.utils.server import ThreadedServer
from config.server import WHO_AM_I, ROUND_TIME
from time import gmtime, strftime
import controllers.chats as ChatController
import controllers.users as UserController
import controllers.groups as GroupController
import controllers.contacts as ContactController

import models.default_servers_list as Default_list_Model
import models.workers_servers_list as Workers_list_Model
import models.suspects_servers_list as Suspects_list_Model
import models.round_times as Round_times_Model


def whoIsAlive():
    Workers_list_Model.clean()
    Suspects_list_Model.clean()
    for server in Default_list_Model.all():
        try:
            SERVERCONNECTION = rpyc.connect(
                server[1],
                server[2]
            )
            SERVERCONNECTION.close()
            if len(Workers_list_Model.findBy_name(name=server[0])) == 0:
                Workers_list_Model.employed(
                    name=server[0],
                    ip=server[1],
                    port=server[2]
                )
                logging.info(' $$$$$ WORKER: ' + str(server[0]))
        except(socket.error, AttributeError, EOFError):
            if len(Suspects_list_Model.findBy_name(name=server[0])) == 0:
                Suspects_list_Model.breathTime(
                    name=server[0],
                    ip=server[1],
                    port=server[2]
                )
            logging.error(
                '+ + + + + + + + [CONNECTION ERROR] + + + + + + + +'
            )
            logging.error('Server: ' + server[0])
            logging.error('IP: ' + server[1])
            logging.error('Port:' + str(server[2]))
        print ('')


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
            _id=item[0],
            user_id=item[1],
            contact_id=item[2],
            created_at=item[3]
        )


def server_sync_Chats(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = ChatController.chats_atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ Chats Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceCreateChat(
            _id=item[0],
            user_id=item[1],
            contact_id=item[2],
            created_at=item[3]
        )


def server_sync_Chat_Messages(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = ChatController.messages_atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ Chats Message Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceSendChatMessage(
            _id=item[0],
            chat_id=item[1],
            sender_id=item[2],
            message=item[3],
            created_at=item[4]
        )


def server_sync_Groups(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = GroupController.groups_atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ Groups Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceCreateGroup(
            _id=item[0],
            group_name=item[1],
            created_at=item[2]
        )


def server_sync_User_Groups(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = GroupController.usersAdd_atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ User Groups Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceAddUserToAGroup(
            _id=item[0],
            user_id=item[1],
            group_id=item[2],
            created_at=item[3]
        )


def server_sync_Group_Messages(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = GroupController.messages_atRound(
        _roundStarted=_oldRound[1],
        _roundFinished=_newRound[1]
    )
    print ('+++ Group Message Total to sync: ', str(len(allItensToSync)))
    for item in allItensToSync:
        SERVERCONNECTION.root.serverReplaceSendGroupMessage(
            _id=item[0],
            group_id=item[1],
            sender_id=item[2],
            message=item[3],
            created_at=item[4]
        )


def sync_Content():
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
    print ('\n... new round ' + str(_newRound))
    for server in Workers_list_Model.all():
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
                print ('\tDiferença no banco')
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
            server_sync_Chats(
                SERVERCONNECTION,
                _newRound,
                _oldRound
            )
            server_sync_Chat_Messages(
                SERVERCONNECTION,
                _newRound,
                _oldRound
            )
            server_sync_Groups(
                SERVERCONNECTION,
                _newRound,
                _oldRound
            )
            server_sync_User_Groups(
                SERVERCONNECTION,
                _newRound,
                _oldRound
            )
            server_sync_Group_Messages(
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
        print ('')


def sync_Servers_list():
    pass


def server_Syncronization():
    while True:
        time.sleep(ROUND_TIME)
        if WHO_AM_I["order"] == "King":
            whoIsAlive()
            sync_Servers_list()
            sync_Content()


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
