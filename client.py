#!/usr/bin/python3

import socket
import signal
import sys
from os import system, name 
from termios import tcflush, TCIFLUSH

# Box design string
box = "   +   +   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   +   +   \n"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

head_message = """
    Welcome to tic-tac-toe
    For Server: O
    For client: X
    Press ctrl+c to exit
"""

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

def intHandler(sig, frame):
    print('Closing...')
    s.close()
    sys.exit(0)
signal.signal(signal.SIGINT, intHandler)

def changeBox(sign, position):
   # Pass the position by counting from zero
   if position in {13, 17, 21, 61, 65, 69, 109, 113, 117}:
      return  box[0:position] + str(sign) + box[(position+1):]

def receiveSignal(signalNumber, frame):
    print('\nClosing...',)
    return

if __name__ == "__main__":

    # create a socket object
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

    # get local machine name
    host = socket.gethostname()                           
    port = 9991

    # connection to hostname on the port.
    s.connect((host, port))       

    # Gaming stuff stuff
    postion_to_index = {
      "1": 13,
      "2": 17,
      "3": 21,
      "4": 61,
      "5": 65,
      "6": 69,
      "7": 109,
      "8": 113,
      "9": 117
    }
    # Record filled boxes; 0 for server; 1 for client; We're not using index 0
    box_record = [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1]

    # Receive message about who will play first; 0 for server and 1 for client
    msg = s.recv(1024)  
    first_play = (msg.decode('ascii'))

    # Set send variable; if 1 send message; if 0 recieve message
    if first_play == "0":
        send = 0
    else:
        send = 1

    while True:

        if send != 1:
            msg = s.recv(1024)
            msg = str(msg.decode('ascii'))
            box = changeBox("O", postion_to_index[msg])
            box_record[int(msg)] = 1
            clear()
            print(head_message)
            print(box)  
            send = 1                                 

        if send == 1:
            # Clear input buffer
            tcflush(sys.stdin, TCIFLUSH)
            input_recieved = str(input(">"))
            print(input_recieved)
            if input_recieved in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and box_record[int(input_recieved)] == -1:
                box = changeBox("X", postion_to_index[input_recieved])
                box_record[int(input_recieved)] = 0
                s.send(input_recieved.encode('ascii'))
                clear()
                print(head_message)
                print(box)
                print("\nNow server's turn...\n")
                send = 0
            else:
                continue
        

    s.close()

