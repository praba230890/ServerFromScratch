# http.webserver
# usage : python -m http.webserver 80
# where 80 is the port number and is optional, if not given it will try to take the port number from settings file
# by default the server will run on port 8888 if nothing is specified in settings file and parameter

import socket
import os
import sys
import time
from datetime import datetime
import SimpleHTTPServer
# from mercurial.dispatch import request

from .request import Request
from .response import Response

_UNKNOWN = 'UNKNOWN'

# connection states
_CS_IDLE = 'Idle'
_CS_REQ_STARTED = 'Request-started'
_CS_REQ_SENT = 'Request-sent'

# trying to fetch HTML_ROOT, host and port from settings file
# if not found then default values will be set
# HTML_ROOT = current directory + public_html, HOST = '', PORT = 8888 

try:
    from .settings import HTML_ROOT
except:
    HTML_ROOT = os.path.join(os.getcwd(), 'public_html')

try:
    from .settings import HOST
except:
    HOST = ''

HTTPS_PORT = 443

try:
    try:
        HTTP_PORT = int(sys.argv[1])
    except:
        try:
            from .settings import PORT as HTTP_PORT
        except:
            pass
except:
    HTTP_PORT = 8888

def main():
    listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    listen_socket.bind((HOST, HTTP_PORT))
    listen_socket.listen(50)
    print 'Serving HTTP on port %s ...' % HTTP_PORT
    serve(listen_socket)
    
def serve(listen_socket):
    try:
        while True:
            client_connection, client_address = listen_socket.accept()
            raw_request = client_connection.recv(1024)
            raw_request_list = raw_request.split('\n')
            
            print "\n Raw request: " + raw_request
            request = Request(raw_request_list[0])
            print "\n Request: \n", request.method, request.protocol, request.location
            
            response = Response(request)
#             print "Response: \n", response.http_response
            
            client_connection.sendall(response.http_response)
            client_connection.close()
    except KeyboardInterrupt:
        print "Exit"
    except:
        client_connection.sendall("""\
HTTP/1.1 %s 
Date: %s
Content-Type: text/html

500 Internal Server Error
"""% ('500 Internal Server Error', datetime.now()))
        client_connection.close()
        time.sleep(2)
        serve(listen_socket)
    
if __name__ == "__main__":
    main()