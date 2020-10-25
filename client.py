import socketclass, socket
from functions import *


def handshake(conn):
    username = input('username: ')
    reply = recv(conn)
    if reply['msg'] == 'username':
        send(conn, {'timestamp': gentimestamp(), 'type': '01', 'msg': username})
        reply = recv(conn)
        if reply['msg'] == 'password':
            password = input('password: ')
            password = passwordhash(password)
            send(conn, {'timestamp': gentimestamp(), 'type': '01', 'msg': password})
            reply = recv(conn)
            if reply['msg'] == 'valid':
                return [True]
            else:
                conn.close()
                return [False]
        else:
            return [False]
    else:
        return [True]


def handle(conn):
    while True:
        try:
            data = recv(conn)
            print('reply from server took {}s: {}'. format(timedifference(data['timestamp']), data['msg']))
            print('>')
        except:
            print('disconnected')
            conn.close()
            break


def sender(conn):
    while True:
        try:
            data = input('>')

            if data[0] == '/':
                request = '02'
                data = data[1:]
            else:
                request = '03'

            send(conn, {'timestamp': gentimestamp(), 'type': request, 'msg': data})
        except:
            conn.close()
            break


client = socketclass.client(socket.gethostbyname(socket.gethostname()), 2020, handshake, handle, sender)
