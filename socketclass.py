import socket, threading


class server:
    @property
    def port(self):
        return self.__port

    @property
    def host(self):
        return self.__host

    def __init__(self, port):
        self.__HOST = socket.gethostbyname(socket.gethostname())
        self.__PORT = port

        self.__connections = []
        self.__threads = []

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.bind((self.__HOST, self.__PORT))
        print('socket server started from {} on port {}'.format(self.__HOST, self.__PORT))

    def run(self, handshake, handle):
        self.__socket.listen()
        print('server listening for connections')

        while True:
            conn, addr = self.__socket.accept()
            print('accepted connection from {} on port {}'.format(addr[0], addr[1]))
            response = handshake(conn, addr)

            if response[0]:
                print('validated connection with {}'.format(addr[0]))
                self.__connections.append(conn)
                self.__threads.append(threading.Thread(target=handle, args=[conn, addr, response[1]], daemon=True))
                self.__threads[-1].start()

            else:
                print('invalid connection from {}'.format(addr[0]))


class client:
    @property
    def rhost(self):
        return self.__RHOST

    @property
    def rport(self):
        return self.__RPORT

    def __init__(self, rhost, rport, handshake, handle, sender):
        self.__RHOST = rhost
        self.__RPORT = rport

        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__socket.connect((self.__RHOST, self.__RPORT))

        response = handshake(self.__socket)

        if response[0]:
            print('socket connected to server at {} on port {}'.format(self.__RHOST, self.__RPORT))
            self.__THREAD = threading.Thread(target=handle, args=[self.__socket], daemon=True)
            self.__THREAD.start()
            sender(self.__socket)

            del self

        else:
            print('connection not validated')
            del self
