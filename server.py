import socket
import random
import signal
import sys
from os import system, name
from termios import tcflush, TCIFLUSH

# ---------- SOCKET DATA ----------

# Create socket
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Frees the socket to reuse
serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# Bind socket with port
serversocket.bind(("0.0.0.0", 8000))


# ---------- GAME DATA ----------

# Box design string
box = "1  |2  |3  \n   |   |   \n   |   |   \n+--+---+--+\n4  |5  |1  \n   |   |   \n   |   |   \n+--+---+--+\n7  |8  |9  \n   |   |   \n   |   |   \n"

# Record filled boxes; 0 for server; 1 for client;s
box_record = [-1, -1, -1, -1, -1, -1, -1, -1, -1]

# Position of box in the box string
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


# ---------- OTHER DATA ----------

head_message = """
Welcome to tic-tac-toe
   For Server: O
   For client: X
   Press ctrl+c to exit
"""


# ---------- UTIL FUNCTIONS ----------


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


# ---------- INSTRUCTIONS ----------

# Listen for clients
serversocket.listen(5)

# Start listening on socket
serversocket.listen(2)

# Accept clients
(clientsocket, (ip, port)) = serversocket.accept()

# Who will play first; 0 for server and 1 for client
first_play = random.choice(["1", "0"])

# send variable; if 1 client will play first; if 0 server wil play first
if first_play == "0":
    send = 1
    print("You will play first.")
else:
    send = 0
    print("Client will play first.")


# Tell client who will play first
clientsocket.send(first_play.encode('ascii'))


# ---------- SUPER LOOP ----------

print(box)

while(True):

    if send == 1:

        # Clear input buffer
        tcflush(sys.stdin, TCIFLUSH)

        # Get input from console
        input_recieved = str(int(input(">")))

        if input_recieved in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and box_record[int(input_recieved) - 1] == -1:

            # Subtract 1 beacuse index start from 0
            input_recieved = str(int(input_recieved) - 1)

            # Add "O" to the box for server
            box = changeBox("O", postion_to_index[input_recieved])

            # Mark the record for that input position
            box_record[int(input_recieved)] = 0

            # Send the recieved input
            clientsocket.send(input_recieved.encode('ascii'))

            # Clear console before printing next box
            clear()

            # Print help text and box
            print(head_message)
            print(box)

            # Check if there is any winner in updated box
            checkWinner()

            print("\nNow client's turn...\n")
            send = 0
        else:
            continue

    if send != 1:

        # Recieve message from client
        msg = clientsocket.recv(1024)
        msg = str(msg.decode('ascii'))

        # Add "X" to the box for client
        box = changeBox("X", postion_to_index[msg])

        # Mark the record for that recieved input
        box_record[int(msg)] = 1

        # Clear console before printing next box
        clear()

        # Print helo text and box
        print(head_message)
        print(box)

        # Check if there is any winner in updated box
        checkWinner()
        send = 1


# ---------- END PROGRAM ----------

tcpSocket.close()
client.close()
