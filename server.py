import socketclass
from functions import *


def loadusers():
    try:
        with open('users.csv', 'r') as f:
            users = f.read().split('\n')
            f.close()
        users = [users[0].split(','), users[1].split(','), users[2].split(',')]
        return users
    except:
        return False


def saveusers(users):
    try:
        text = ''
        for line in users:
            for user in line:
                text += user + ','
            text = text[:-1] + '\n'
        with open('users.csv', 'w') as f:
            f.write(text)
            f.close()
        return True
    except:
        return False


def command(command, userid):
    command = command.split(' ')
    try:
        if command[0] == 'adduser':
            users = loadusers()
            if users[2][userid] == '5':
                if not(command[1] in users[0]):
                    if 0 <= int(command[3]) <= 5:
                        users[0].append(command[1])
                        users[1].append(passwordhash(command[2]))
                        users[2].append(command[3])

                        saveusers(users)

                        return 'command executed'
                    else:
                        return 'invalid permissions value'
                else:
                    return 'username already in use'
            else:
                return 'you do not have the permissions for this'
        else:
            return 'invalid command'
    except:
        return 'invalid command syntax'


def handshake(conn, addr):
    users = loadusers()

    send(conn, {'timestamp': gentimestamp(), 'type': '01', 'msg': 'username'})
    reply = recv(conn)

    if reply['msg'] in users[0]:
        userid = users[0].index(reply['msg'])
        send(conn, {'timestamp': reply['timestamp'], 'type': '01', 'msg': 'password'})
        reply = recv(conn)

        if reply['msg'] == users[1][userid]:
            send(conn, {'timestamp': reply['timestamp'], 'type': '01', 'msg': 'valid'})
            return [True, userid]

        else:
            conn.close()
            return [False]
    else:
        conn.close()
        return [False]


def handle(conn, addr, info):
    while True:
        try:
            data = recv(conn)

            if data['type'] == '02':
                data['msg'] = command(data['msg'], info)
                data['type'] = '03'
            else:
                data['msg'] = 'message recieved'
                data['type'] = '03'

            send(conn, data)
        except:
            print('{} disconnected'.format(addr[0]))
            conn.close()
            break


server = socketclass.server(2020)
server.run(handshake, handle)
