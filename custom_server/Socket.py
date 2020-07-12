#!/usr/bin/env python3

import socket
import threading
import struct
import os

class Socket:
    def __init__(self):
        host = None
        port = None
        sock = None
    
    def init_sock(self):
        host_name = socket.gethostname()
        self.host = socket.gethostbyname(host_name)
        self.port = 8080 # default port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.sock.listen()
        return self

    def recv_data(self, sock):
        try:
            data = sock.recv(4096)
            normalised_data = self.normalize_line_endings(data.decode('utf-8'))

            if normalised_data is not None:
                request_head, request_body = normalised_data.split('\n\n', 1)
                request_head = request_head.splitlines()
                request_headline = request_head[0]
                request_headers = dict(x.split(': ', 1) for x in request_head[1:])
                request_method, request_uri, request_proto = request_headline.split(' ', 3)
            serialised_data = {
                'request_headers': request_headers,
                'request_uri': request_uri,
                'request_headline': request_headline
            }
        except:
            os._exit(1)
        return serialised_data

    def normalize_line_endings(self, s):
        return ''.join((line + '\n') for line in s.splitlines())

    def send_data(self, sock, data):
        try:
            sock.send(data['top_header'])
            sock.send(data['response_headers'])
            sock.send('\n'.encode('utf-8'))
            sock.send(data['response_body'])
            sock.close()
        except:
            os._exit(1)