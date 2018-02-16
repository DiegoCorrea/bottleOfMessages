# -*- coding: utf-8 -*-
import rpyc
import copy
import sys
import re
import socket
import logging
import collections

from config.server import WHO_AM_I, KING

import models.chats as ChatModel
import models.users as UserModel
import models.groups as GroupModel
import models.contacts as ContactModel

import models.default_servers_list as Default_list_Model
import models.workers_servers_list as Workers_list_Model
import models.suspects_servers_list as Suspects_list_Model
import models.round_times as Round_times_Model

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
sys.path.append('..')


class ServerService(rpyc.Service):

    def on_connect(self):
        # code that runs when a connection is created
        # (to init the serivce, if needed)
        pass

    def on_disconnect(self):
        # code that runs when the connection has already closed
        # (to finalize the service, if needed)
        pass
# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceCreateUser(self, name, email, created_at):
        logging.info(' _____ Replace User ' + str(email))
        UserModel.create(email=email, name=name, created_at=created_at)

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
        if len(UserModel.findBy_email(email)) != 0:
            logging.info('Finish [Create User] - return: @VALIDATION/EXISTENT')
            return {
                'type': '@VALIDATION/EXISTENT',
                'payload': {}
            }
        # Persiste
        UserModel.create(email=email, name=name)
        user = UserModel.findBy_email(email=email)
        # Return
        logging.info('Finish [Create User] - return: @USER/DATA')
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
        user = UserModel.findBy_email(email)
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
        user = UserModel.findBy_email(user_id)
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
    def exposed_serverReplaceCreateChat(
        self,
        _id,
        user_id,
        contact_id,
        created_at
    ):
        logging.info(
            ' _____ Replace Chat: ' + str(user_id)
            + ' with ' + str(contact_id)
        )
        ChatModel.createChat(
            _id=_id,
            user_id=user_id,
            contact_id=contact_id,
            created_at=created_at
        )

    @classmethod  # this is an exposed method
    def exposed_createChat(self, user_id, contact_id):
        logging.info('Start [Create Chat]')
        contact = UserModel.findBy_ID(contact_id)
        if len(contact) == 0 or len(UserModel.findBy_ID(user_id)) == 0:
            logging.info('Finish [Create Chat] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        chat = ChatModel.getChatWith(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(chat) == 0:
            ChatModel.createChat(user_id=user_id, contact_id=contact_id)
            chat = ChatModel.getChatWith(
                user_id=user_id,
                contact_id=contact_id
            )
        logging.info('Finish [Create Chat] - return: @CHAT/DATA')
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
        if len(UserModel.findBy_ID(user_id)) == 0:
            logging.info('Finish [All Chats] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        for chat in ChatModel.allUserChat(user_id=user_id):
            if chat[1] == user_id:
                contact = UserModel.findBy_ID(chat[2])
            else:
                contact = UserModel.findBy_ID(chat[1])
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
            contact = UserModel.findBy_ID(contact_id)
            chatMessageHistory = {}
            chat = ChatModel.getChatWith(user_id, contact_id)
            if len(chat) == 0:
                logging.info(
                    'Finish [CHAT MESSAGE HISTORY] - return: @CHAT/NOTFOUND'
                )
                return {
                    'type': '@CHAT/NOTFOUND',
                    'payload': {}
                }
            for chat_message in ChatModel.getMessages(chat[0]):
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
                'payload': chatMessageHistory
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
        self,
        _id,
        chat_id,
        sender_id,
        message,
        created_at
    ):
        logging.info(
            ' _____ Replace Chat Message: ' + str(chat_id)
            + ' sender ' + str(sender_id)
        )
        ChatModel.sendMessage(
            _id=_id,
            chat_id=chat_id,
            sender_id=sender_id,
            message=message,
            created_at=created_at
        )

    @classmethod  # this is an exposed method
    def exposed_sendChatMessage(self, user_id, contact_id, message):
        logging.info('Start [SEND MESSAGE USER]')
        if len(
            UserModel.findBy_ID(
                contact_id
                )
                ) == 0 or len(UserModel.findBy_ID(user_id)) == 0:
            logging.info('Finish [Create Chat] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        chat = ChatModel.getChatWith(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(chat) == 0:
            ChatModel.createChat(
                user_id=user_id,
                contact_id=contact_id
            )
            chat = ChatModel.getChatWith(
                user_id=user_id,
                contact_id=contact_id
            )
        ChatModel.sendMessage(
            chat_id=chat[0],
            sender_id=user_id,
            message=message
        )
        logging.info(
            'Finish [SEND MESSAGE USER] - '
            + 'return: self.exposed_chatMessageHistory(user_id, contact_id)'
        )
        return self.exposed_getChatMessageHistory(user_id, contact_id)
# ########################################################################## #

# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceCreateGroup(
        self,
        _id,
        group_name,
        created_at
    ):
        logging.info(
            ' _____ Replace Group: ' + str(_id)
            + ' name ' + str(group_name)
        )
        GroupModel.create(
            _id=_id,
            group_name=group_name,
            created_at=created_at
        )

    @classmethod  # this is an exposed method
    def exposed_createGroup(self, user_id, group_name):
        logging.info('Start [CREATE GROUP]')
        if len(UserModel.findBy_ID(user_id=user_id)) == 0:
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
        group_id = GroupModel.create(group_name=group_name)
        if len(group_id) == 0:
            logging.info('Finish [CREATE GROUP] - return: @GROUP/CANT_CREATE')
            return {
                'type': '@GROUP/CANT_CREATE',
                'payload': {}
            }
        GroupModel.addUser(user_id=user_id, group_id=group_id)
        logging.info('Finish [CREATE GROUP] - return: @GROUP/DATA')
        group = GroupModel.findBy_ID(group_id=group_id)
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
        if len(UserModel.findBy_ID(user_id=user_id)) == 0:
            logging.info('Finish [User All Groups] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        groupList = GroupModel.userGroups(user_id=user_id)
        if len(groupList) == 0:
            logging.info('Finish [User All Groups] - return: @GROUP/ZERO')
            return {
                'type': '@GROUP/ZERO',
                'payload': {}
            }
        groupData = {}
        for userGroup in groupList:
            group = GroupModel.findBy_ID(userGroup[2])
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
        self,
        user_id,
        group_id,
        _id,
        created_at
    ):
        logging.info(
            ' _____ Replace Add User to a Group: ' + str(user_id)
            + ' to group ' + str(group_id)
        )
        GroupModel.addUser(
            _id=_id,
            user_id=user_id,
            group_id=group_id,
            created_at=created_at
        )

    @classmethod  # this is an exposed method
    def exposed_addUserToAGroup(self, user_id, group_id):
        logging.info('Start [Add User To a Group]')
        if len(UserModel.findBy_ID(user_id=user_id)) == 0:
            logging.info(
                'Finish [Add User To a Group] - return: @USER/NOTFOUND'
            )
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        if len(GroupModel.findBy_ID(group_id=group_id)) == 0:
            logging.info(
                'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/NOTFOUND'
            )
            return {
                'type': '@GROUP/NOTFOUND',
                'payload': {}
            }
        GroupModel.addUser(user_id, group_id)
        logging.info(
            'Finish [Add User To a Group] - '
            + 'return: self.exposed_getAllUserGroups(user_id)'
        )
        group = GroupModel.findBy_ID(group_id=group_id)
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
            group = GroupModel.findBy_ID(group_id=group_id)
            if len(group) == 0:
                logging.info(
                    'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/NOTFOUND'
                )
                return {
                    'type': '@GROUP/NOTFOUND',
                    'payload': {}
                }
            for message in GroupModel.getMessages(group_id=group[0]):
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
        self,
        _id,
        group_id,
        sender_id,
        message,
        created_at
    ):
        logging.info(
            ' _____ Replace Group Message: ' + str(group_id)
            + ' sender ' + str(sender_id)
        )
        GroupModel.sendMessage(
            _id=_id,
            group_id=group_id,
            sender_id=sender_id,
            message=message,
            created_at=created_at
        )

    @classmethod  # this is an exposed method
    def exposed_sendGroupMessage(self, user_id, group_id, message):
        logging.info('Start [SEND GROUP MESSAGE]')
        group = GroupModel.findBy_ID(group_id=group_id)
        if len(group) == 0:
            logging.info(
                'Finish [GROUP MESSAGE HISTORY] - return: @GROUP/NOTFOUND'
            )
            return {
                'type': '@GROUP/NOTFOUND',
                'payload': {}
            }
        GroupModel.sendMessage(
            group_id=group[0],
            sender_id=user_id,
            message=message
        )
        logging.info(
            'Finish [SEND GROUP MESSAGE] - '
            + 'return: self.exposed_groupMessageHistory(user_id, group_id)'
        )
        return self.exposed_groupMessageHistory(user_id, group_id)
# ########################################################################## #

# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod
    def exposed_serverReplaceAddContact(
        self,
        _id,
        user_id,
        contact_id,
        created_at
    ):
        logging.info(
            ' _____ Replace Contacts: ' + str(user_id)
            + ' To ' + str(contact_id)
        )
        ContactModel.create(
            _id=_id,
            user_id=user_id,
            contact_id=contact_id,
            created_at=created_at
        )

    @classmethod  # this is an exposed method
    def exposed_addContact(self, user_id, contact_id):
        logging.info('Start [Add Contact]')
        userData = UserModel.findBy_ID(user_id=user_id)
        contactData = UserModel.findBy_ID(user_id=contact_id)
        if len(contactData) == 0 or len(userData) == 0:
            logging.info('Finish [Add Contact] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        contact = ContactModel.findBy_ID(
            user_id=user_id,
            contact_id=contact_id
        )
        if len(contact) != 0:
            logging.info('Finish [Add Contact] - return: @CONTACT/ISALREADY')
            return {
                'type': '@CONTACT/ISALREADY',
                'payload': {}
            }
        ContactModel.create(user_id=user_id, contact_id=contact_id)
        logging.info('Finish [Add Contact] - return: @USER/CONTACT/DATA')
        contact = ContactModel.findBy_ID(
            user_id=user_id,
            contact_id=contact_id
        )
        userContact = UserModel.findBy_ID(user_id=contact[2])
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
        user = UserModel.findBy_ID(user_id=user_id)
        if len(user) == 0:
            logging.info('Finish [User All Groups] - return: @USER/NOTFOUND')
            return {
                'type': '@USER/NOTFOUND',
                'payload': {}
            }
        contacts = ContactModel.all(user_id=user_id)
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
            contactData = UserModel.findBy_email(contact[2])
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

# ########################################################################## #
# ########################################################################## #
# ########################################################################## #

    @classmethod  # this is an exposed method
    def exposed_newRound(self, _round):
        logging.info(' +++++ SYNCRONIZATION - NEW ROUND +++++ ' + str(_round))
        lastRound = Round_times_Model.last()
        if _round[0] - lastRound[0] > 1:
            return False
        Round_times_Model.create(
                _round=_round[0],
                created_at=_round[1]
        )
        return True

    @classmethod  # this is an exposed method
    def exposed_sync_default_servers(self, servers_list):
        Default_list_Model.clean()
        for server in copy.deepcopy(servers_list):
            Default_list_Model.create(
                name=server['name'],
                ip=server['ip'],
                port=server['port'],
                succession_order=server['succession_order']
            )
            logging.info(' _____| Replace Default Server: ' + str(server))

    @classmethod
    def exposed_sync_workers_servers(self, king, servers_list):
        Workers_list_Model.clean()
        Workers_list_Model.create(
            name=copy.deepcopy(king['name']),
            ip=copy.deepcopy(king['ip']),
            port=copy.deepcopy(king['port']),
            succession_order=copy.deepcopy(king['succession_order'])
        )
        logging.info(' _____| Replace Worker King: ' + str(king))
        for server in copy.deepcopy(servers_list):
            if server['name'] == WHO_AM_I['name']:
                continue
            Workers_list_Model.create(
                name=server['name'],
                ip=server['ip'],
                port=server['port'],
                succession_order=server['succession_order']
            )
            logging.info(' _____| Replace Worker Server: ' + str(server))

    @classmethod
    def exposed_sync_suspects_servers(self, servers_list):
        Suspects_list_Model.clean()
        for server in copy.deepcopy(servers_list):
            if server['name'] == WHO_AM_I['name']:
                continue
            Suspects_list_Model.create(
                name=server['name'],
                ip=server['ip'],
                port=server['port']
            )
            logging.info(' _____| Replace Suspects Servers: ' + str(server))

    @classmethod
    def exposed_isKing(self):
        global KING
        global WHO_AM_I
        if WHO_AM_I['position'] == KING:
            return True
        return False

    @classmethod
    def exposed_getServerList(self):
        return Default_list_Model.all()

    @classmethod
    def exposed_newWorker(self, identification):
        if len(Default_list_Model.findBy_name(
            name=identification['name'])
        ) > 0:
            return False
        Default_list_Model.create(
            name=identification['name'],
            ip=identification['ip'],
            port=identification['port'],
            succession_order=identification['succession_order']
        )
        return True

    @classmethod
    def exposed_lastRoundSync(self):
        return Round_times_Model.last()
