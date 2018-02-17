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

import controllers.syncContents as ContentSyncroniztion

import models.default_servers_list as Default_list_Model
import models.workers_servers_list as Workers_list_Model
import models.suspects_servers_list as Suspects_list_Model
import models.round_times as Round_times_Model


def whoIsAlive():
    logging.info(" **************** How is Alive?")
    Workers_list_Model.clean()
    Suspects_list_Model.clean()
    print(str(Default_list_Model.all()))
    for server in Default_list_Model.all():
        if WHO_AM_I['name'] == server['name']:
            continue
        try:
            SERVERCONNECTION = rpyc.connect(
                server['ip'],
                server['port']
            )
            SERVERCONNECTION.close()
            Workers_list_Model.employed(
                name=server['name'],
                ip=server['ip'],
                port=server['port'],
                succession_order=server["succession_order"]
            )
            logging.info(
                '+ + + + + + + + [ALIVE] + + + + + + + +'
                + '\n+ + + + + + + + ' + str(server['name'])
                + '\n+ + + + + + + + ' + str(server['ip'])
                + '\n+ + + + + + + + ' + str(server['port'])
                + '\n+ + + + + + + + ' + str(server['succession_order'])
            )
        except(socket.error, AttributeError, EOFError):
            Suspects_list_Model.breathTime(
                name=server['name'],
                ip=server['ip'],
                port=server['port']
            )
            logging.error(
                '+ + + + + + + + [CONNECTION ERROR] + + + + + + + +'
            )
            logging.error('Server: ' + server['name'])
            logging.error('IP: ' + server['ip'])
            logging.error('Port:' + str(server['port']))


def sync_Servers_list():
    for server in Workers_list_Model.all():
        try:
            SERVERCONNECTION = rpyc.connect(
                server['ip'],
                server['port']
            )
            SERVERCONNECTION.root.sync_default_servers(
                servers_list=Default_list_Model.all()
            )
            SERVERCONNECTION.root.sync_workers_servers(
                king=WHO_AM_I,
                servers_list=Workers_list_Model.all()
            )
            SERVERCONNECTION.root.sync_suspects_servers(
                servers_list=Suspects_list_Model.all()
            )
            SERVERCONNECTION.close()
        except(socket.error, AttributeError, EOFError):
            logging.error(
                '+ + + + + + + + [CONNECTION ERROR] + + + + + + + +'
            )
            logging.error('Server: ' + server['name'])
            logging.error('IP: ' + server['ip'])
            logging.error('Port:' + str(server['port']))


def election():
    logging.info(' + + + + + + + + ( ELECTION ) + + + + + + + + ')
    votes = sorted(
        [server['succession_order'] for server in Workers_list_Model.all()]
    )
    logging.info(' + + + + + + + + Votes: '+str(votes))
    if len(votes) == 0:
        logging.warning('@ @ @ @ @ @ @ @ Can\'t Vote!!!!!')
        return ''
    if votes[0] > WHO_AM_I['succession_order']:
        logging.info(' > > > > > > > > > I AM THE NEW KING')
        WHO_AM_I['position'] = KING
    else:
        logging.info(' - - - - - - - - - - WORK WORK WORK')
        WHO_AM_I['position'] = WORKER


def theKingIsAlive():
    king = Workers_list_Model.first()
    try:
        SERVERCONNECTION = rpyc.connect(
            king['ip'],
            king['port']
        )
        SERVERCONNECTION.close()
        return True
    except(socket.error, AttributeError, EOFError):
        logging.error(
            '+ + + + + + + + [KING IS OFFICIAL DEAD] + + + + + + + +'
        )
        logging.error('Server: ' + king['name'])
        logging.error('IP: ' + king['ip'])
        logging.error('Port:' + str(king['port']))
        return False
    except(TypeError):
        logging.error(
            '+ + + + + + + + [THE FIRST KING] + + + + + + + +'
        )
        return False


def youKnowMe():
    for server in Default_list_Model.all():
        try:
            if WHO_AM_I['name'] == server['name']:
                continue
            SERVERCONNECTION = rpyc.connect(
                server['ip'],
                server['port']
            )
            if SERVERCONNECTION.root.isKing():
                SERVERCONNECTION.root.newWorker(WHO_AM_I)
            SERVERCONNECTION.close()
        except(socket.error, AttributeError, EOFError):
            logging.error(
                '+ + + + + + + + [] + + + + + + + +'
            )
            logging.error('Server: ' + server['name'])
            logging.error('IP: ' + server['ip'])
            logging.error('Port:' + str(server['port']))
