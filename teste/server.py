# -*- coding: utf-8 -*-
import rpyc
import sys
import re
import socket
import logging
import collections
import copy

import controllers.chats as ChatController
import controllers.users as UserController
import controllers.groups as GroupController
import controllers.contacts as ContactController

from config.server import SERVERS_LIST, LIVE_STATUS, DEATH_STATUS, WHO_AM_I

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
sys.path.append('..')
CONNECTION_COUNT = 0
HIGH_LIST = []
FIRST_TIME = True


class ServerService(rpyc.Service):

    def __init__(self, how):
        global CONNECTION_COUNT
        global FIRST_TIME
        if CONNECTION_COUNT % 10 == 0:
            self.checkServers()
        if FIRST_TIME is True:
            self.requireToEnter()
            FIRST_TIME = False

    def requireToEnter(self):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.debug("[Require To Enter] - " + str(server['name']))
                SERVERCONNECTION.root.letMeEnter(WHO_AM_I)
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    def exposed_letMeEnter(self, newService):
        global HIGH_LIST
        HIGH_LIST.append(copy.deepcopy(newService))
        logging.debug("[Let Me Enter] - New Service" + str(newService['name']))

    def checkServers(self):
        global HIGH_LIST
        del HIGH_LIST[:]
        SERVERCONNECTION = None
        for server in SERVERS_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                server['status'] = LIVE_STATUS
                HIGH_LIST.append(server)
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    def exposed_live(self):
        return str('@CONNECTED')

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        global CONNECTION_COUNT
        CONNECTION_COUNT += 1
        logging.debug('Connection count: ' + str(CONNECTION_COUNT))
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceCreateUser(self, name, email):
        UserController.create(email=email, name=name)

    @classmethod
    def broadcast_replaceCreateUser(self, name, email):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info("[Replace Create User] - " + str(server['name']))
                SERVERCONNECTION.root.serverReplaceCreateUser(name, email)
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_createUser(self, name, email):
        logging.info('Start [Create User]')
        # Validate
        if re.match(r"[^@]+@[^@]+\.[^@]+", email) is None:
            logging.info('Finish [Create User] - return: @VALIDATION/ERROR')
            return {
                'type': '@VALIDATION/NOT_EMAIL',
                'payload': {}
            }
        if len(name) == 0:
            logging.info(
                'Finish [Create User] - return: @VALIDATION/SMALL_NAME'
            )
            return {
                'type': '@VALIDATION/SMALL_NAME',
                'payload': {}
            }
        if len(UserController.findBy_email(email)) != 0:
            logging.info('Finish [Create User] - return: @VALIDATION/EXISTENT')
            return {
                'type': '@VALIDATION/EXISTENT',
                'payload': {}
            }
        # Persiste
        UserController.create(email=email, name=name)
        user = UserController.findBy_email(email=email)
        # Return
        logging.info('Finish [Create User] - return: @USER/DATA')
        self.broadcast_replaceCreateUser(name=str(name), email=str(email))
        return {
            'type': '@USER/DATA',
            'payload': {
                'email': user[0],
                'name': user[1]
            }
        }
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_findUserByEmail(self, email):
        logging.info('Start [FIND USER BY EMAIL]')
        user = UserController.findBy_email(email)
        if len(user) == 0:
            logging.info('Finish [FIND USER BY EMAIL] - return @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        logging.info('Finish [FIND USER BY EMAIL] - return @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'email': user[0],
                'name': user[1]
            }
        }
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_userLogin(self, user_id):
        logging.info('Start [User Login]')
        user = UserController.findBy_email(user_id)
        if len(user) == 0:
            logging.info('Finish [User Login] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        chatList = self.exposed_getAllUserChats(user_id)
        userGroups = self.exposed_getAllUserGroups(user_id)
        contactList = self.exposed_getAllUserContacts(user_id)
        logging.info('Finish [User Login] - return: @USER/DATA')
        return {
            'type': '@USER/DATA',
            'payload': {
                'user': {
                    'email': user[0],
                    'name': user[1]
                },
                'contacts': contactList['payload'],
                'chats': chatList['payload'],
                'groups': userGroups['payload']
            }
        }
# ########################################################################## #

# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceCreateChat(self, user_id, contact_id):
        ChatController.createChat(user_id=user_id, contact_id=contact_id)

    @classmethod
    def broadcast_replaceCreateChat(self, user_id, contact_id):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info(
                    "[Replace Create Chat] - Send to -> "
                    + str(server['name'])
                )
                SERVERCONNECTION.root.serverReplaceCreateChat(
                    user_id,
                    contact_id
                )
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_createChat(self, user_id, contact_id):
        logging.info('Start [Create Chat]')
        contact = UserController.findBy_ID(contact_id)
        if len(contact) == 0 or len(UserController.findBy_ID(user_id)) == 0:
            logging.info('Finish [Create Chat] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        chat = ChatController.getChatWith(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(chat) == 0:
            ChatController.createChat(user_id=user_id, contact_id=contact_id)
            chat = ChatController.getChatWith(
                user_id=user_id,
                contact_id=contact_id
            )
        logging.info('Finish [Create Chat] - return: @CHAT/DATA')
        self.broadcast_replaceCreateChat(user_id, contact_id)
        return {
            'type': '@CHAT/DATA',
            'payload': {
                'id': chat[0],
                'email': contact[0],
                'name': contact[1],
                'created_at': chat[3],
                'messages': self.exposed_getChatMessageHistory(
                    user_id=user_id,
                    contact_id=contact[0]
                )['payload']
            }
        }
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_getAllUserChats(self, user_id):
        logging.info('Start [All Chats]')
        userChatList = {}
        if len(UserController.findBy_ID(user_id)) == 0:
            logging.info('Finish [All Chats] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        for chat in ChatController.allUserChat(user_id=user_id):
            if chat[1] == user_id:
                contact = UserController.findBy_ID(chat[2])
            else:
                contact = UserController.findBy_ID(chat[1])
            userChatList.setdefault(contact[0], {
                'email': contact[0],
                'name': contact[1],
                'created_at': chat[3],
                'messages': self.exposed_getChatMessageHistory(
                    user_id=user_id,
                    contact_id=contact[0]
                )['payload']
            })
        if len(userChatList) == 0:
            logging.info('Finish [All Chat] - return: @CHAT/ZERO')
            return {
                'type': '@CHAT/ZERO',
                'payload': {}
            }
        logging.info('Finish [All Chat] - return: @CHAT/DATA')
        return {
            'type': '@CHAT/DATA',
            'payload': userChatList
        }
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_getChatMessageHistory(self, user_id, contact_id):
        logging.info('Start [CHAT MESSAGE HISTORY]')
        try:
            contact = UserController.findBy_ID(contact_id)
            chatMessageHistory = {}
            chat = ChatController.getChatWith(user_id, contact_id)
            if len(chat) == 0:
                logging.info(
                    'Finish [CHAT MESSAGE HISTORY] - return: @CHAT/NOTFOUND'
                )
                return {
                    'type': '@CHAT/NOTFOUND',
                    'payload': {}
                }
            for chat_message in ChatController.getMessages(chat[0]):
                chatMessageHistory.setdefault(chat_message[4], {
                    'sender_id': chat_message[2],
                    'message': chat_message[3],
                    'created_at': chat_message[4]
                })
            if len(chatMessageHistory) == 0:
                logging.info(
                    'Finish [CHAT MESSAGE HISTORY] - '
                    + 'return: @CHAT/MESSAGE/ZERO'
                )
                return {
                    'type': '@CHAT/MESSAGE/ZERO',
                    'payload': {}
                }
            logging.info(
                'Finish [CHAT MESSAGE HISTORY] - return: @CHAT/MESSAGE/DATA'
            )
            return {
                'type': '@CHAT/MESSAGE/DATA',
                'payload': {
                    'email': contact[0],
                    'name': contact[1],
                    'created_at': chat[3],
                    'messages': collections.OrderedDict(
                        sorted(chatMessageHistory.items())
                    )
                }
            }
        except TypeError:
            logging.error(
                'Finish [CHAT MESSAGE HISTORY] - return: @SERVER/ERROR'
            )
            return {
                'type': '@SERVER/ERROR',
                'payload': {}
            }
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceSendChatMessage(
        self, user_id, contact_id, message
    ):
        chat = ChatController.getChatWith(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(chat) == 0:
            ChatController.createChat(
                user_id=user_id,
                contact_id=contact_id
            )
            chat = ChatController.getChatWith(
                user_id=user_id,
                contact_id=contact_id
            )
        ChatController.sendMessage(
            chat_id=chat[0],
            sender_id=user_id,
            message=message
        )

    @classmethod
    def broadcast_replaceSendChatMessage(self, user_id, contact_id, message):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info(
                    "[Replace Send Chat Message] - Send to -> "
                    + str(server['name'])
                )
                SERVERCONNECTION.root.serverReplaceSendChatMessage(
                    user_id, contact_id, message
                )
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_sendChatMessage(self, user_id, contact_id, message):
        logging.info('Start [SEND MESSAGE USER]')
        if len(
            UserController.findBy_ID(
                contact_id
                )
                ) == 0 or len(UserController.findBy_ID(user_id)) == 0:
            logging.info('Finish [Create Chat] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        chat = ChatController.getChatWith(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(chat) == 0:
            ChatController.createChat(
                user_id=user_id,
                contact_id=contact_id
            )
            chat = ChatController.getChatWith(
                user_id=user_id,
                contact_id=contact_id
            )
        ChatController.sendMessage(
            chat_id=chat[0],
            sender_id=user_id,
            message=message
        )
        logging.info(
            'Finish [SEND MESSAGE USER] - '
            + 'return: self.exposed_chatMessageHistory(user_id, contact_id)'
        )
        self.broadcast_replaceSendChatMessage(user_id, contact_id, message)
        return self.exposed_getChatMessageHistory(user_id, contact_id)
# ########################################################################## #

# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceCreateGroup(
        self, user_id, group_name
    ):
        group_id = GroupController.create(group_name=group_name)
        GroupController.addUser(user_id=user_id, group_id=group_id)

    @classmethod
    def broadcast_replaceCreateGroup(self, user_id, group_name):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info(
                    "[Replace Create Group] - Send to -> "
                    + str(server['name'])
                )
                SERVERCONNECTION.root.serverReplaceCreateGroup(
                    user_id, group_name
                )
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_createGroup(self, user_id, group_name):
        logging.info('Start [CREATE GROUP]')
        if len(UserController.findBy_ID(user_id=user_id)) == 0:
            logging.info('Finish [User All Groups] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        if len(group_name) == 0:
            logging.info(
                'Finish [CREATE GROUP] - return: @VALIDATION/SMALL_NAME'
            )
            return {
                'type': '@VALIDATION/SMALL_NAME',
                'payload': {}
            }
        group_id = GroupController.create(group_name=group_name)
        if len(group_id) == 0:
            logging.info('Finish [CREATE GROUP] - return: @GROUP/CANT_CREATE')
            return {
                'type': '@GROUP/CANT_CREATE',
                'payload': {}
            }
        GroupController.addUser(user_id=user_id, group_id=group_id)
        logging.info('Finish [CREATE GROUP] - return: @GROUP/DATA')
        self.broadcast_replaceCreateGroup(user_id, group_name)
        group = GroupController.findBy_ID(group_id=group_id)
        return {
            'type': '@GROUP/DATA',
            'payload': {
                'id': group[0],
                'name': group[1],
                'join_at': group[2],
                'created_at': group[2],
                'messages': {}
            }
        }
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_getAllUserGroups(self, user_id):
        logging.info('Start [User All Groups]')
        if len(UserController.findBy_ID(user_id=user_id)) == 0:
            logging.info('Finish [User All Groups] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        groupList = GroupController.userGroups(user_id=user_id)
        if len(groupList) == 0:
            logging.info('Finish [User All Groups] - return: @GROUP/ZERO')
            return {
                'type': '@GROUP/ZERO',
                'payload': {}
            }
        groupData = {}
        for userGroup in groupList:
            group = GroupController.findBy_ID(userGroup[2])
            groupData.setdefault(userGroup[2], {
                'id': userGroup[2],
                'name': group[1],
                'join_at': userGroup[3],
                'created_at': group[2],
                'messages': self.exposed_groupMessageHistory(
                    user_id=user_id,
                    group_id=userGroup[2]
                )['payload']
            })
        logging.info('Finish [User All Groups] - return: @GROUP/DATA')
        return {
            'type': '@GROUP/DATA',
            'payload': groupData
        }
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceAddUserToAGroup(
        self, user_id, group_id
    ):
        GroupController.addUser(user_id=user_id, group_id=group_id)

    @classmethod
    def broadcast_replaceAddUserToAGroup(self, user_id, group_id):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info(
                    "[Replace Add User To A Group] - Send to -> "
                    + str(server['name'])
                )
                SERVERCONNECTION.root.serverReplaceAddUserToAGroup(
                    user_id, group_id
                )
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_addUserToAGroup(self, user_id, group_id):
        logging.info('Start [Add User To a Group]')
        if len(UserController.findBy_ID(user_id=user_id)) == 0:
            logging.info(
                'Finish [Add User To a Group] - return: @USER/NOTFOUND'
            )
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        if len(GroupController.findBy_ID(group_id=group_id)) == 0:
            logging.info(
                'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/NOTFOUND'
            )
            return {
                'type': '@GROUP/NOTFOUND',
                'payload': {}
            }
        GroupController.addUser(user_id, group_id)
        logging.info(
            'Finish [Add User To a Group] - '
            + 'return: self.exposed_getAllUserGroups(user_id)'
        )
        group = GroupController.findBy_ID(group_id=group_id)
        self.broadcast_replaceAddUserToAGroup(user_id, group_id)
        return {
            'type': '@GROUP/DATA',
            'payload': {
                'id': group[0],
                'name': group[1],
                'join_at': group[2],
                'created_at': group[2],
                'messages': self.exposed_groupMessageHistory(
                    user_id=user_id,
                    group_id=group_id
                )['payload']
            }
        }
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_groupMessageHistory(self, user_id, group_id):
        logging.info('Start [GROUP MESSAGE HISTORY]')
        try:
            messageHistory = {}
            group = GroupController.findBy_ID(group_id=group_id)
            if len(group) == 0:
                logging.info(
                    'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/NOTFOUND'
                )
                return {
                    'type': '@GROUP/NOTFOUND',
                    'payload': {}
                }
            for message in GroupController.getMessages(group_id=group[0]):
                messageHistory.setdefault(message[3], {
                    'sender_id': message[1],
                    'message': message[4],
                    'created_at': message[3]
                })
            if len(messageHistory) == 0:
                logging.info(
                    'Finish [GROUP MESSAGE HISTORY] - '
                    + 'return: @GROUP/MESSAGE/ZERO'
                )
                return {
                    'type': '@GROUP/MESSAGE/ZERO',
                    'payload': {}
                }
            logging.debug('[GROUP MESSAGE HISTORY] - ', messageHistory)
            logging.info(
                'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/MESSAGE/DATA'
            )
            return {
                'type': '@GROUP/MESSAGE/DATA',
                'payload': collections.OrderedDict(
                    sorted(messageHistory.items())
                )
            }
        except TypeError:
            logging.error(
                'Finish [GROUP MESSAGE HISTORY] - return: @SERVER/ERROR'
            )
            return {
                'type': '@SERVER/ERROR',
                'payload': {}
            }
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceSendGroupMessage(
        self, user_id, group_id, message
    ):
        GroupController.sendMessage(
            group_id=group_id,
            sender_id=user_id,
            message=message
        )

    @classmethod
    def broadcast_replaceSendGroupMessage(self, user_id, group_id, message):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info(
                    "[Replace Send Chat Message] - Send to -> "
                    + str(server['name'])
                )
                SERVERCONNECTION.root.serverReplaceSendGroupMessage(
                    user_id, group_id, message
                )
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_sendGroupMessage(self, user_id, group_id, message):
        logging.info('Start [SEND GROUP MESSAGE]')
        group = GroupController.findBy_ID(group_id=group_id)
        if len(group) == 0:
            logging.info(
                'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/NOTFOUND'
            )
            return {
                'type': '@GROUP/NOTFOUND',
                'payload': {}
            }
        GroupController.sendMessage(
            group_id=group[0],
            sender_id=user_id,
            message=message
        )
        logging.info(
            'Finish [SEND GROUP MESSAGE] - '
            + 'return: self.exposed_groupMessageHistory(user_id, group_id)'
        )
        self.broadcast_replaceSendGroupMessage(
            group_id=group[0],
            user_id=user_id,
            message=message
        )
        return self.exposed_groupMessageHistory(user_id, group_id)
# ########################################################################## #

# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceAddContact(self, user_id, contact_id):
        ContactController.create(user_id=user_id, contact_id=contact_id)

    @classmethod
    def broadcast_replaceAddContact(self, user_id, contact_id):
        global HIGH_LIST
        SERVERCONNECTION = None
        for server in HIGH_LIST:
            try:
                SERVERCONNECTION = rpyc.connect(
                    server['ip'],
                    server['port']
                )
                logging.info(
                    "[Replace Create Contact] - Send to -> "
                    + str(server['name'])
                )
                SERVERCONNECTION.root.serverReplaceAddContact(
                    user_id,
                    contact_id
                )
                SERVERCONNECTION.close()
            except(socket.error, AttributeError, EOFError):
                server['status'] = DEATH_STATUS
                logging.error(
                    '+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + + +'
                )
                logging.error('Server: ' + server['name'])
                logging.error('IP: ' + server['ip'])
                logging.error('Port:' + str(server['port']))
                logging.error('Status: ' + server['status'])

    @classmethod  # this is an exposed method
    def exposed_addContact(self, user_id, contact_id):
        logging.info('Start [Add Contact]')
        userData = UserController.findBy_ID(user_id=user_id)
        contactData = UserController.findBy_ID(user_id=contact_id)
        if len(contactData) == 0 or len(userData) == 0:
            logging.info('Finish [Add Contact] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        contact = ContactController.findBy_ID(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(contact) != 0:
            logging.info('Finish [Add Contact] - return: @CONTACT/ISALREADY')
            return {
                'type': '@CONTACT/ISALREADY',
                'payload': {}
            }
        ContactController.create(user_id=user_id, contact_id=contact_id)
        logging.info('Finish [Add Contact] - return: @USER/CONTACT/DATA')
        contact = ContactController.findBy_ID(
            user_id=user_id,
            contact_id=contact_id
        )
        self.broadcast_replaceAddContact(user_id, contact_id)
        userContact = UserController.findBy_ID(user_id=contact[2])
        return {
            'type': '@USER/CONTACT/DATA',
            'payload': {
                'email': userContact[0],
                'name': userContact[1],
                'created_at': contact[3]
            }
        }

    @classmethod  # this is an exposed method
    def exposed_getAllUserContacts(self, user_id):
        user = UserController.findBy_ID(user_id=user_id)
        if len(user) == 0:
            logging.info('Finish [User All Groups] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        contacts = ContactController.all(user_id=user_id)
        if len(contacts) == 0:
            logging.info(
                'Finish [User All Groups] - return: @USER/CONTACT/ZERO'
            )
            return {
                'type': '@USER/CONTACT/ZERO',
                'payload': {}
            }
        userContactList = {}
        for contact in contacts:
            contactData = UserController.findBy_email(contact[2])
            userContactList.setdefault(contact[2], {
                'email': contactData[0],
                'name': contactData[1],
                'created_at': contact[3],
            })
        logging.info('Finish [User All Groups] - return: @USER/CONTACT/DATA')
        return {
            'type': '@USER/CONTACT/DATA',
            'payload': userContactList
        }
