#!/usr/bin/python3           # This is client.py file

import socket

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999

# connection to hostname on the port.
s.connect((host, port))       

# Gaming stuff
box = "   +   +   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   +   +   \n"


while True:

    # Receive no more than 1024 bytes
    msg = s.recv(1024)  
    print(msg.decode('ascii'))                                   

    msg = input(">")
    s.send(msg.encode('ascii'))

s.close()
print (msg.decode('ascii'))