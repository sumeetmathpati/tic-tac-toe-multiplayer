#!/usr/bin/python3 

import socket       
import random 
import signal
import sys
from os import system, name 
from termios import tcflush, TCIFLUSH

# Box design string
box = "   +   +   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   +   +   \n"

# Record filled boxes; 0 for server; 1 for client;s
box_record = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

head_message = """
Welcome to tic-tac-toe
For Server: O
For client: X
Press ctrl+c to exit
"""

# Server socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

def checkWinner():
   if box_record[0] == box_record[1] == box_record[2]:
      printWinner(box_record[0])
   elif box_record[3] == box_record[4] == box_record[5]:
      printWinner(box_record[3])
   elif box_record[6] == box_record[7] == box_record[8]:
      printWinner(box_record[6])
   elif box_record[0] == box_record[3] == box_record[6]:
      printWinner(box_record[0])
   elif box_record[1] == box_record[4] == box_record[7]:
      printWinner(box_record[1])
   elif box_record[2] == box_record[5] == box_record[8]:
      printWinner(box_record[2])
   elif box_record[0] == box_record[4] == box_record[8]:
      printWinner(box_record[0])
   elif box_record[6] == box_record[4] == box_record[2]:
      printWinner(box_record[6])

def printWinner(sign):
   if sign == 0:
      print("Server is winner...")
      sys.exit()
   elif sign == 1:
      print("Client is winner...")
      sys.exit()

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
      "0": 13,
      "1": 17,
      "2": 21,
      "3": 61,
      "4": 65,
      "5": 69,
      "6": 109,
      "7": 113,
      "8": 117
   }

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
         input_recieved = str(int(input(">")))
         if input_recieved in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and box_record[int(input_recieved) - 1] == -1:
            input_recieved = str(int(input_recieved) - 1)
            box = changeBox("O", postion_to_index[input_recieved])
            box_record[int(input_recieved)] = 0
            clientsocket.send(input_recieved.encode('ascii'))
            clear()
            print(head_message)
            print(box)
            checkWinner()
            print("\nNow client's turn...\n")
            send = 0
         else:
            continue
      
      if send != 1:
         msg = clientsocket.recv(1024)
         msg = str(msg.decode('ascii'))
         box = changeBox("X", postion_to_index[msg])
         box_record[int(msg)] = 1
         clear()
         print(head_message)
         print(box)   
         checkWinner()
         send = 1

    
   clientsocket.close()

