import logging
import logging.config
import threading
import socket
import time
import rpyc
import json
import os

from datetime import datetime
from time import gmtime, strftime

from server import ServerService
from rpyc.utils.server import ThreadedServer

from config.server import WHO_AM_I, ROUND_TIME, TIME_FORMAT, KING, WORKER

import models.chats as ChatModel
import models.users as UserModel
import models.groups as GroupModel
import models.contacts as ContactModel

import models.default_servers_list as Default_list_Model
import models.workers_servers_list as Workers_list_Model
import models.suspects_servers_list as Suspects_list_Model
import models.round_times as Round_times_Model


def server_sync_Users(SERVERCONNECTION, _newRound, _oldRound):
    allItensToSync = UserModel.atRound(
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
    allItensToSync = ContactModel.atRound(
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
    allItensToSync = ChatModel.chats_atRound(
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
    allItensToSync = ChatModel.messages_atRound(
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
    allItensToSync = GroupModel.groups_atRound(
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
    allItensToSync = GroupModel.usersAdd_atRound(
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
    allItensToSync = GroupModel.messages_atRound(
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
# #####################################################


def start():
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
                server['ip'],
                server['port'],
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
            logging.error('Server: ' + server['name'])
            logging.error('IP: ' + server['ip'])
            logging.error('Port:' + str(server['port']))
        print ('')
