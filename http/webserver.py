import socket
import datetime
import os
# from mercurial.dispatch import request

from part1.request import method

HOST, PORT = '', 8888

HTML_ROOT = "/home/naveen/workspace/WebServer/part1/public_html/"

def get_response_body(response_file):    
    try:
        with open(response_file, 'r') as response_file:
            return "".join([line for line in response_file.readlines()]), "200 OK"
    except:
        return "Invalid request", "404 Not Found"

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    
    request = method(request.split('\n')[0])
    print request, type(request), request.method, request.protocol, request.location

    response_time = str(datetime.datetime.now())
    
    response_body, response_status = get_response_body(os.path.join(HTML_ROOT+request.location[1:]))
            
    http_response_header = """\
HTTP/1.1 %s 
Date: %s
Content-Type: text/html

""" % (response_status, response_time)
    http_response = http_response_header+"""
        %s \n
         This is %s method request""" % (response_body, request.method)
        
    print http_response
    
    client_connection.sendall(http_response)
    client_connection.close()
