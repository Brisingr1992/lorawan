#!/usr/bin/env python3

from mimetypes import MimeTypes
import time
import os.path
from wsgiref.handlers import format_date_time

class Message:
    def build_response(self, sock, serialised_data):
        request_headline = serialised_data['request_headline']
        request_method, request_uri, request_proto = request_headline.split(' ', 3)
        file_name = 'www' + request_uri

        try:
            file_timestamp = os.path.getmtime(file_name)
            file_present = True
        except:
            file_present = False

        if file_present is True:
            top_header = self.build_top('200', 'OK')
            response_body = self.build_body(file_name)
            response_headers = self.build_header(file_name, response_body, file_timestamp)
        else:
            file_name = 'errors.html'
            top_header = self.build_top('404', 'Not Found')
            response_body = self.build_body(file_name)
            response_headers = self.build_header(file_name, response_body, None)

        data = {
            'filename': file_name,
            'top_header': top_header,
            'response_headers': response_headers,
            'response_body': response_body
        }
        
        return data

    def build_top(self, status, text):
        return ''.join('%s %s %s\n' % ('HTTP/1.1', status, text)).encode('utf-8')
    
    def build_body(self, filename):
        f = open(filename,'rb')
        return f.read()

    def build_header(self, filename, body, timestamp):
        type = MimeTypes().guess_type(filename)
        access_time = format_date_time(timestamp) if timestamp is not None else None
        response_headers = {
            'Content-Type': (type[0] if type[0] is not None else 'application/octet-stream') \
                + '; encoding=utf8',
            'Content-Length': len(body),
            'Connection': 'close',
            'Date': format_date_time(time.time()),
            'Server': 'ssaxena3Server',
            'Last-Modified': access_time
        }
        return ''.join('%s: %s\n' % (k, v) for k, v \
            in response_headers.items()).encode('utf-8')
        
