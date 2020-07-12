#!/usr/bin/env python3

import Socket
import threading
import message
import time
from wsgiref.handlers import format_date_time
import sys

requests = {}
lock = threading.Lock()

class Server:
    def __init__(self):
        sock = None

    def handle_new_conn(self, conn, addr):
        with conn:
            new_conn = Socket.Socket()
            serialised_data = new_conn.recv_data(conn)
            lock.acquire()
            try:
                data = message.Message().build_response(conn, serialised_data)
                if data['filename'] != 'errors.html':
                    request_uri = serialised_data['request_uri']
                    if request_uri not in requests:
                        requests[request_uri] = 1
                    else:
                        requests[request_uri] = requests[request_uri] + 1

                    stdout = ''.join('%s | %s | %s | %d' %  \
                        (request_uri, addr[0], addr[1] , requests[request_uri]))
                    print(stdout)
                self.sock.send_data(conn, data)
            finally:
                lock.release()
            sys.exit(1)

# Driver code
print("Initializing server")
server = Server()
master_sock = Socket.Socket()
master_sock.init_sock()
server.sock = master_sock

print('Server started on HOST-({}), Port-({})'.format(master_sock.host, master_sock.port))

connections = []
while True:
    conn, addr = master_sock.sock.accept()
    connections.append(conn)
    thread = threading.Thread(target=server.handle_new_conn, args=(conn,addr))
    thread.start()
master_sock.sock.close()