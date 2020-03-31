#!/usr/bin/python3 

import socket       
import random 
import signal
import sys
from os import system, name 
from termios import tcflush, TCIFLUSH

# Box design string
box = "   +   +   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   +   +   \n"

head_message = """
    Welcome to tic-tac-toe
    For Server: O
    For client: X
    Press ctrl+c to exit
"""

# Server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

def intHandler(sig, frame):
    print('\nClosing...')
    serversocket.close()
    sys.exit(0)
signal.signal(signal.SIGINT, intHandler)

def changeBox(sign, position):
   # Pass the position by counting from zero
   if position in {13, 17, 21, 61, 65, 69, 109, 113, 117}:
      return box[0:position] + str(sign) + box[(position+1):]

def clear(): 
    # for windows 
    if name == 'nt': 
        _ = system('cls') 
    # for mac and linux(here, os.name is 'posix') 
    else: 
        _ = system('clear') 

if __name__ == "__main__":

   # get local machine name 
   host = socket.gethostname()                           
   port = 9991
                      
   # bind to the port
   serversocket.bind((host, port))                                  
   # queue up to 5 requests
   serversocket.listen(5)         
   clientsocket,addr = serversocket.accept() 

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

   # Record filled boxes
   box_record = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

   # Who will play first; 0 for server and 1 for client
   first_play = random.choice(["1", "0"])
   print("First play: ", first_play)
   # send variable; if 1 send message; if 0 recieve message
   if first_play == "0":
      send = 1
   else:
      send = 0
   

   # Tell client who will play first
   clientsocket.send(first_play.encode('ascii'))

   while True:
      
      if send == 1:
         # Clear input buffer
         tcflush(sys.stdin, TCIFLUSH)
         input_recieved = str(input(">"))
         if input_recieved in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and box_record[int(input_recieved)] == -1:
            box = changeBox("X", postion_to_index[input_recieved])
            clientsocket.send(input_recieved.encode('ascii'))
            clear()
            print(head_message)
            print(box)
            print("\nNow client's turn...\n")
            send = 0
         else:
            continue
      
      if send != 1:
         msg = clientsocket.recv(1024)
         msg = str(msg.decode('ascii'))
         box = changeBox("O", postion_to_index[msg])
         clear()
         print(head_message)
         print(box)   
         send = 1

    
   clientsocket.close()

