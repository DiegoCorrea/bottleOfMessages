# -*- coding: utf-8 -*-
from __future__ import print_function
from time import sleep
import os
import rpyc
import re
import socket
import copy

rpyc.core.protocol.DEFAULT_CONFIG['allow_pickle'] = True
LIVE_STATUS = 'live'
DEATH_STATUS = 'dinosaur'
SERVERCONNECTION = None
STORE = {
    'user': {},
    'contacts': {},
    'chats': {},
    'groups': {}
}
CONFIG = {
    'connected': False,
    'servers': [
        {
            'status': '',
            'name': 'Exu',
            'ip': '192.168.0.13',
            'port': 27000
        }, {
            'status': '',
            'name': 'Hermes',
            'ip': '192.168.0.14',
            'port': 27001
        }, {
            'status': '',
            'name': 'Thot',
            'ip': '192.168.0.14',
            'port': 27002
        }
    ]
}

# #############################################################################
# #############################################################################
# ############################## Shared Functions #############################
# #############################################################################
# #############################################################################


def readGroupIDFromKey():
    inText = ''
    while inText == '':
        try:
            inText = input("Group Code: ")
        except KeyboardInterrupt:
            exitProgramWithSuccess()
        except (NameError, SyntaxError, ValueError):
            print ('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print ('\tMessage: Wrong Input, try again!')
            inText = ''
    return inText


def readNameFromKey():
    inText = ''
    while inText == '':
        try:
            inText = input("Name: ")
        except KeyboardInterrupt:
            exitProgramWithSuccess()
        except (NameError, SyntaxError, ValueError):
            print ('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print ('\tMessage: Wrong Input, try again!')
            inText = ''
    return inText


def readEmailFromKey():
    inText = ''
    while inText == '':
        try:
            inText = input("Email: ")
            if re.match(r"[^@]+@[^@]+\.[^@]+", inText) is None:
                print ('+ + + + + + + + + + [Messages] + + + + + + + + + +')
                print ('\tMessage: Please type a valid email address')
                inText == ''
        except KeyboardInterrupt:
            exitProgramWithSuccess()
        except (NameError, SyntaxError, ValueError):
            print ('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print ('\tMessage: Wrong Input, try again!')
            inText = ''
    return inText


def readMenuChoiceFromKey():
    try:
        inText = int(input("Choice: "))
        return inText
    except KeyboardInterrupt:
        exitProgramWithSuccess()
    except (NameError, SyntaxError, ValueError):
        print ('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print ('\tMessage: Wrong Input, try again!')
        waitEnter()
        return 10


def waitEnter():
    inText = 'a'
    while inText != '':
        try:
            inText = input("Press Enter to continue... ")
            os.system('cls||clear')
            return inText
        except KeyboardInterrupt:
            exitProgramWithSuccess()
        except (NameError, SyntaxError):
            print ('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print ('\tMessage: Wrong Input, try again!')
            inText = 'a'


def printScreenHeader():
    global STORE
    os.system('cls||clear')
    print ('# ############################################## #')
    print (
        '# Session: ( '
        + STORE['user']['name']
        + ' - '
        + STORE['user']['email']
        + ' )'
    )
    print ('# ############################################## #')


def printErrorMessage(error):
    pass
# #############################################################################
# #############################################################################
# ########################### Exit program Functions ##########################
# #############################################################################
# #############################################################################


def exitProgramWithSuccess():
    os.system('cls||clear')
    global SERVERCONNECTION
    try:
        SERVERCONNECTION.close()
        print('# ################################### #')
        print('# Bottle of Messages Drop on the Sea! #')
        print('#\tTchuss!\t\t\t      #')
        print('# ################################### #')
        exit()
    except (IndexError, socket.error, EOFError, AttributeError):
        exitProgramWithError()


def exitProgramWithError():
    os.system('cls||clear')
    print('# ################################### #')
    print('# Sorry! All server is down           #')
    print('# ################################### #')
    exit(1)
# ########################################################################### #
# ########################################################################### #
# ######################## Server Connection Functions ###################### #
# ########################################################################### #
# ########################################################################### #


def startConnectWithServers():
    global SERVERCONNECTION
    global CONFIG
    SERVERS = None
    for server in CONFIG['servers']:
        try:
            SERVERCONNECTION = rpyc.connect(
                server['ip'],
                server['port']
            )
            SERVERS = copy.deepcopy(SERVERCONNECTION.root.getServerList())
            SERVERCONNECTION.close()
            break
        except (socket.error, AttributeError):
            continue
        print(str(SERVERS))
    CONFIG['servers'] = copy.deepcopy(SERVERS)
    for server in CONFIG['servers']:
        try:
            SERVERCONNECTION = rpyc.connect(
                server['ip'],
                server['port']
            )
            if not SERVERCONNECTION.root.isKing():
                SERVERCONNECTION.close()
                continue
            CONFIG['connected'] = True
            server['status'] = LIVE_STATUS
            print ('+ + + + + + + + + [CONNECTION SUCCESS] + + + + + + + + +')
            print ('Server: ' + server['name'])
            print ('Status: ' + server['status'])
            print ('IP: ' + server['ip'])
            print ('Port:' + str(server['port']))
            print ("\n\nLoad the program...")
            sleep(3)
            return ''
        except (socket.error, AttributeError):
            server['status'] = DEATH_STATUS
            print ('+ + + + + + + + + [CONNECTION ERROR] + + + + + + + + +')
            print ('Server: ' + server['name'])
            print ('Status: ' + server['status'])
            print ('IP: ' + server['ip'])
            print ('Port:' + str(server['port']))
            for i in range(3):
                print ("- Try again in: " + str(3-i))
                sleep(1)
                print ('\r', end='')
    exitProgramWithError()
# #############################################################################
# #############################################################################
# ############################### Group Functions #############################
# #############################################################################
# #############################################################################


def remoteGetAllUserGroups():
    try:
        data = SERVERCONNECTION.root.getAllUserGroups(
            user_id=STORE['user']['email']
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def getAllUserGroups():
    data = remoteGetAllUserGroups()
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == '@GROUP/DATA':
        STORE['groups'] = data['payload']
# #############################################################################


def printGroup(data):
    print('--------------------------------------------------')
    print('+ Code:', data['id'])
    print('+ Name:', data['name'])
    print('+ Join at:', data['join_at'])
    print('+ Since at:', data['created_at'])
    print('--------------------------------------------------')


def printAllGroups():
    global STORE
    if len(STORE['groups']) > 0:
        for group_id in STORE['groups']:
            printGroup(STORE['groups'][group_id])
    else:
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('+ + + + [Message] -> No groups added')
        print('# ############################################## #')


def screenPrintAllGroups():
    printScreenHeader()
    print('--------------------------------------------------')
    print('=================== Group List ===================')
    printAllGroups()
# #############################################################################


def remoteAddUserToAGroup(group_id):
    try:
        data = SERVERCONNECTION.root.addUserToAGroup(
            user_id=STORE['user']['email'],
            group_id=group_id
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {
                'message': ''
            }
        }


def addUserToAGroup(group_id):
    global STORE
    data = remoteAddUserToAGroup(group_id=group_id)
    if data['type'] == '@GROUP/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Group not found')
        return ''
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: ', data['payload']['message'])
        return ''
    if data['type'] == '@GROUP/DATA':
        STORE['groups'][data['payload']['id']] = data['payload']
        return data['payload']


def screenAddUserToAGroup():
    printScreenHeader()
    print('--------------------------------------------------')
    print('================== Join a Group ==================')
    print('--------------------------------------------------')
    payload = addUserToAGroup(group_id=readGroupIDFromKey())
    if len(payload) > 0:
        printGroup(payload)
# #############################################################################


def remoteCreateGroup(group_name):
    try:
        data = SERVERCONNECTION.root.createGroup(
            user_id=STORE['user']['email'],
            group_name=group_name
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def createGroup(group_name):
    try:
        global STORE
        data = remoteCreateGroup(group_name)
        if data['type'] == '@VALIDATION/SMALL_NAME':
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print('\tMessage: Name to small')
            return ''
        if data['type'] == '@GROUP/CANT_CREATE':
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print('\tMessage: Cant Create the group')
            return ''
        if data['type'] == '@USER/NOTFOUND':
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print('\tMessage: User not found')
            return ''
        if data['type'] == 'ERROR/CONNECTION':
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print('\tMessage: Connection Error!')
            return ''
        if data['type'] == '@GROUP/DATA':
            STORE['groups'][data['payload']['id']] = data['payload']
            return data['payload']
    except AttributeError:
        print('Algo de errado ocorreu: ')


def screenCreateGroup():
    printScreenHeader()
    print('--------------------------------------------------')
    print('================= Create a Group =================')
    print('--------------------------------------------------')
    payload = createGroup(readNameFromKey())
    if len(payload) > 0:
        printGroup(payload)
# #############################################################################


def printGroupMessages(group_id):
    printGroup(STORE['groups'][group_id])
    if len(STORE['groups'][group_id]['messages']) > 0:
        for message in STORE['groups'][group_id]['messages']:
            print (
                'De: '
                + STORE['groups'][group_id]['messages'][message]['sender_id']
                + ' '
                + STORE['groups'][group_id]['messages'][message]['created_at']
            )
            print(STORE['groups'][group_id]['messages'][message]['message'])
            print('--------------------------------------------------')
    else:
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No messages yet')
        print('# ############################################## #')


def remoteSendGroupMessage(group_id, message):
    try:
        data = SERVERCONNECTION.root.sendGroupMessage(
            user_id=STORE['user']['email'],
            group_id=group_id,
            message=message
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def sendGroupMessege(group_id, message):
    global STORE
    data = remoteSendGroupMessage(group_id, message)
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found!')
        return ''
    if data['type'] == '@GROUP/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Group not found!')
        return ''
    if data['type'] == '@GROUP/MESSAGE/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No message yet!')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@SERVER/ERROR':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Server Error!')
        return ''
    if data['type'] == '@GROUP/MESSAGE/DATA':
        STORE['groups'][group_id]['messages'] = data['payload']


def remoteGetGroupMessages(group_id):
    try:
        data = SERVERCONNECTION.root.groupMessageHistory(
            user_id=STORE['user']['email'],
            group_id=group_id
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError, TypeError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def getGroupMessages(group_id):
    global STORE
    data = remoteGetGroupMessages(group_id)
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found!')
        return ''
    if data['type'] == '@GROUP/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Group not found!')
        return ''
    if data['type'] == '@GROUP/MESSAGE/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No message yet!')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@SERVER/ERROR':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Server Error!')
        return ''
    if data['type'] == '@GROUP/MESSAGE/DATA':
        STORE['groups'][group_id]['messages'] = data['payload']


def screenGroupChat():
    group_id = readGroupIDFromKey()
    if group_id not in STORE['groups']:
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: You has no groupd added yet!')
        return ''
    text = ''
    while True:
        try:
            getGroupMessages(group_id)
            printScreenHeader()
            printGroupMessages(group_id)
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print("Commands:")
            print("\t[:q] to exit")
            print("\t[:u] to update chat")
            text = input("Text:\n")
            if text == ':q':
                return ''
            elif text == ':u' or text == '':
                pass
            else:
                sendGroupMessege(group_id, text)
        except KeyboardInterrupt:
            exitProgramWithSuccess()
        except (NameError, SyntaxError):
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print('\tMessage: Wrong Input, try again!')
            print('Error Message: ')
            text = ''
            waitEnter()
# #############################################################################


def screenGroup():
    global STORE
    getAllUserGroups()
    while True:
        printScreenHeader()
        menuChoice = 10
        print('1 - Create a Group')
        print('2 - Enter in a Group')
        print('3 - List All Your Groups')
        print('4 - Open Group Chat')
        print('0 - Back To Main Screen')
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            screenCreateGroup()
        elif menuChoice == 2:
            screenAddUserToAGroup()
        elif menuChoice == 3:
            screenPrintAllGroups()
        elif menuChoice == 4:
            screenGroupChat()
        elif menuChoice == 0:
            return ''
        waitEnter()
# #############################################################################
# #############################################################################
# ############################# Contact Functions #############################
# #############################################################################
# #############################################################################


def printContact(data):
    print('--------------------------------------------------')
    print('Name: ', data['name'])
    print('Email: ', data['email'])
    print('Added at: ', data['created_at'])
    print('--------------------------------------------------')


def printAllContacts():
    if len(STORE['contacts']) > 0:
        for contact in STORE['contacts']:
            printContact(STORE['contacts'][contact])
    else:
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No contacts yet')
        print('# ############################################## #')


def screenPrintAllContacts():
    printScreenHeader()
    print('--------------------------------------------------')
    print('================== All Contacts ==================')
    printAllContacts()
# #############################################################################


def remoteGetAllUserContacts():
    try:
        data = SERVERCONNECTION.root.getAllUserContacts(
            user_id=STORE['user']['email']
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def getAllContacts():
    data = remoteGetAllUserContacts()
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == '@USER/CONTACT/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No contacts')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@USER/CONTACT/DATA':
        STORE['contacts'] = data['payload']
# #############################################################################


def remoteaddContact(contact_id):
    try:
        data = SERVERCONNECTION.root.addContact(
            user_id=STORE['user']['email'],
            contact_id=contact_id
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def addContact(contact_id):
    data = remoteaddContact(contact_id=contact_id)
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == '@CONTACT/ISALREADY':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Contact is already your friend.')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@USER/CONTACT/DATA':
        STORE['contacts'][data['payload']['email']] = data['payload']
        return data['payload']


def screenAddContact():
    printScreenHeader()
    print('--------------------------------------------------')
    print('================= Add a Contact ==================')
    print('--------------------------------------------------')
    payload = addContact(contact_id=readEmailFromKey())
    if len(payload) > 0:
        printContact(payload)
# #############################################################################


def screenContacts():
    getAllContacts()
    menuChoice = 10
    global STORE
    while True:
        printScreenHeader()
        print('1 - Add Contact')
        print('2 - All Contacts')
        print('0 - Back to main screen')
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            screenAddContact()
        elif menuChoice == 2:
            screenPrintAllContacts()
        elif menuChoice == 0:
            return ''
        waitEnter()
# #############################################################################
# #############################################################################
# ######################## User Chat Functions ################################
# #############################################################################
# #############################################################################


def remoteCreateChat(contact_id):
    try:
        data = SERVERCONNECTION.root.createChat(
            user_id=STORE['user']['email'],
            contact_id=contact_id
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def createChat(email):
    global STORE
    data = remoteCreateChat(contact_id=email)
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@CHAT/MESSAGE/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No messages yet!')
        return ''
    if data['type'] == '@CHAT/DATA':
        STORE['chats'][data['payload']['email']] = copy.deepcopy(data['payload'])
        return copy.deepcopy(data['payload'])
# #############################################################################


def printChatMessages(contact_id):
    global STORE
    printChat(STORE['chats'][contact_id])
    if len(STORE['chats']) > 0 and len(STORE['chats'][contact_id]['messages']) > 0:
        for message in STORE['chats'][contact_id]['messages']:
            print (
                'De: '
                + STORE['chats'][contact_id]['messages'][message]['sender_id']
                + ' '
                + STORE['chats'][contact_id]['messages'][message]['created_at']
            )
            print(STORE['chats'][contact_id]['messages'][message]['message'])
            print('--------------------------------------------------')
    else:
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No messages yet!')
        print('# ############################################## #')


def remoteSendChatMessage(contact_id, message):
    try:
        data = SERVERCONNECTION.root.sendChatMessage(
            user_id=STORE['user']['email'],
            contact_id=contact_id,
            message=message
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def sendChatMessage(contact_id, message):
    global STORE
    data = remoteSendChatMessage(contact_id, message)
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == '@CHAT/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No chat found')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    STORE['chats'][contact_id]['messages'] = copy.deepcopy(data['payload'])


def remoteGetChatMessages(contact_id):
    try:
        data = SERVERCONNECTION.root.getChatMessageHistory(
            user_id=STORE['user']['email'],
            contact_id=contact_id
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError, TypeError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def getChatMessages(contact_id):
    global STORE
    data = remoteGetChatMessages(contact_id)
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    if data['type'] == '@CHAT/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: CHAT not found')
        return ''
    if data['type'] == '@CHAT/MESSAGE/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No message yet')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@SERVER/ERROR':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Server Error')
        return ''
    STORE['chats'][contact_id]['messages'] = copy.deepcopy(data['payload'])


def screenContactChat():
    contact_id = readEmailFromKey()
    if contact_id not in STORE['chats']:
        STORE['chats'][contact_id] = createChat(contact_id)
    text = ''
    while True:
        try:
            getChatMessages(contact_id)
            printScreenHeader()
            printChatMessages(contact_id)
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print("Commands:")
            print("\t[:q] to exit")
            print("\t[:u] to update chat")
            text = input("Text: \n")
            if text == ':q':
                return ''
            elif text == ':u' or text == '':
                pass
            else:
                sendChatMessage(contact_id, text)
        except KeyboardInterrupt:
            exitProgramWithSuccess()
        except (NameError, SyntaxError):
            print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
            print('\tMessage: Wrong Input, try again!')
            text = ''
            waitEnter()
# #############################################################################


def printChat(data):
    print('--------------------------------------------------')
    print('+ Chat With: ', data['name'])
    print('+ Email: ', data['email'])
    print('+ Since at: ', data['created_at'])
    print('--------------------------------------------------')


def printAllChats():
    global STORE
    if len(STORE['chats']) > 0:
        for chat in STORE['chats']:
            printChat(chat)
    else:
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: You have not chat yet')
    print('# ############################################## #')


def screenPrintAllChats():
    printScreenHeader()
    print('--------------------------------------------------')
    print('=================== Chat List ====================')
    printAllChats()
# #############################################################################


def remoteGetAllUserChats():
    try:
        data = SERVERCONNECTION.root.getAllUserChats(
            user_id=STORE['user']['email']
        )
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def getUserChats():
    global STORE
    data = remoteGetAllUserChats()
    if data['type'] == '@CHAT/ZERO':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: No chat found')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@CHAT/DATA':
        STORE['chats'] = copy.deepcopy(data['payload'])
# #############################################################################


def screenUserChat():
    menuChoice = 10
    global STORE
    while True:
        getUserChats()
        printScreenHeader()
        print('1 - All Chat')
        print('2 - Open Chat')
        print('0 - Back to main screen')
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            screenPrintAllChats()
        elif menuChoice == 2:
            screenContactChat()
        elif menuChoice == 0:
            return ''
        waitEnter()
# #############################################################################
# #############################################################################
# ############################### MAIN SCREEN #################################
# #############################################################################
# #############################################################################


def mainScreen():
    while True:
        printScreenHeader()
        print('1 - Contacts Screen')
        print('2 - Chats Screen')
        print('3 - Groups Screen')
        print('0 - Exit Bottle of Messages')
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            screenContacts()
        elif menuChoice == 2:
            screenUserChat()
        elif menuChoice == 3:
            screenGroup()
        elif menuChoice == 0:
            exitProgramWithSuccess()
        else:
            waitEnter()
# #############################################################################
# #############################################################################
# ################## LOGIN SYSTEM AND CREATE ACCOUNT SYSTEM ###################
# #############################################################################
# #############################################################################


def remoteLogOnSystem(email):
    try:
        data = SERVERCONNECTION.root.userLogin(user_id=email)
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def logIn(email):
    global STORE
    data = {}
    data = remoteLogOnSystem(email=email)
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!')
        return ''
    if data['type'] == '@USER/NOTFOUND':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: User not found')
        return ''
    STORE = data['payload']
    loginConfirmation()


def remoteCreateUser(email, name):
    try:
        data = SERVERCONNECTION.root.createUser(email=email, name=name)
        return copy.deepcopy(data)
    except (IndexError, socket.error, AttributeError, EOFError):
        startConnectWithServers()
        return {
            'type': 'ERROR/CONNECTION',
            'payload': {}
        }


def createAccount():
    print(' ______________________________________')
    print('|    Welcome To Bottle of Messages     |')
    print('|        Create new account            |')
    print(' --------------------------------------')
    email = readEmailFromKey()
    name = readNameFromKey()
    data = remoteCreateUser(email=email, name=name)
    if data['type'] == '@VALIDATION/NOT_EMAIL':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: It is not a valid email')
        return ''
    if data['type'] == '@VALIDATION/SMALL_NAME':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Name to small')
        return ''
    if data['type'] == '@VALIDATION/EXISTENT':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Choice another account id')
        return ''
    if data['type'] == 'ERROR/CONNECTION':
        print('+ + + + + + + + + + [Messages] + + + + + + + + + +')
        print('\tMessage: Connection Error!aa')
        return ''
    STORE['user'] = data['payload']


def loginScreen():
    menuChoice = 10
    while len(STORE['user']) == 0:
        os.system('cls||clear')
        print('# ################################################ #')
        print('# 1 - Login                                        #')
        print('# 2 - Join Us                                      #')
        print('# 0 - Exit Bottle of Messages                      #')
        print('# ################################################ #')
        menuChoice = readMenuChoiceFromKey()
        if menuChoice == 1:
            logIn(readEmailFromKey())
        elif menuChoice == 2:
            createAccount()
        elif menuChoice == 0:
            exitProgramWithSuccess()
        waitEnter()


def loginConfirmation():
    printScreenHeader()
    printAllContacts()
    printAllGroups()

# ########################################################################### #
# ########################################################################### #
# ############################ MAIN PROGRAM ################################# #
# ########################################################################### #
# ########################################################################### #


if __name__ == "__main__":
    startConnectWithServers()
    os.system('cls||clear')
    if CONFIG['connected'] is True:
        loginScreen()
        if len(STORE['user']) > 0:
            mainScreen()
    exitProgramWithSuccess()
