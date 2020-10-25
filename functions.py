import time, hashlib


def send(conn, data):
    data = data['timestamp'] + data['type'] + data['msg']
    return conn.send(bytes(data, 'utf-8'))


def recv(conn):
    data = conn.recv(1024).decode('utf-8')
    data = {'timestamp': data[:6], 'type': data[6:8], 'msg': data[8:]}
    return data


def gentimestamp():
    timestamp = round(time.time(), 2)
    timestamp = str(timestamp).replace('.', '')
    timestamp = timestamp[-6:]
    return timestamp


def timedifference(timestamp):
    timestamp = float(timestamp) / 100
    current = float(gentimestamp()) / 100
    return round(current - timestamp, 2)


def passwordhash(password):
    return hashlib.sha256(bytes(password, 'utf-8')).hexdigest()
