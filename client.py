import socket
import signal
import sys
from os import system, name
from termios import tcflush, TCIFLUSH

# Exit if IP not provided

if len(sys.argv) != 2:
    print("USAGE: provide server IP address")
    exit(0)


# ---------- SOCKET DATA ----------

# Create socket
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# ---------- GAME DATA ----------

# Box design string
box = "   +   +   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   |   |   \n+--+---+--+\n   |   |   \n   |   |   \n   +   +   \n"

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
        return  box[0:position] + str(sign) + box[(position+1):]


def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')
    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')


# ---------- INSTRUCTIONS ----------

# Connect to server
socket.connect((sys.argv[1], 8000))

# Receive message about who will play first; 0 for server and 1 for client
msg = socket.recv(1024)
first_play = (msg.decode('ascii'))

# Set send variable; if 1 send message; if 0 recieve message
if first_play == "0":
    send = 0
    print("Server will play first.")
else:
    send = 1
    print("You will play first.")

# ---------- SUPER LOOP ----------

while(True):

    if send == 1:
        # Clear input buffer
        tcflush(sys.stdin, TCIFLUSH)

        # Get input from console
        input_recieved = str(int(input(">")))

        print(input_recieved)
        if input_recieved in ["1", "2", "3", "4", "5", "6", "7", "8", "9"] and box_record[int(input_recieved) - 1] == -1:

            # Subtract 1 beacuse index start from 0
            input_recieved = str(int(input_recieved) - 1)

            # Add "X" to the box for client
            box = changeBox("X", postion_to_index[input_recieved])

            # Mark the record for that input position
            box_record[int(input_recieved)] = 1

            # Send the recieved input
            socket.send(input_recieved.encode('ascii'))

            # Clear console before printing next box
            clear()

            # Print help text and box
            print(head_message)
            print(box)

            # Check if there is any winner in updated box
            checkWinner()

            print("\nNow server's turn...\n")
            send = 0
        else:
            continue

    if send != 1:

        # Recieve message from server
        msg = socket.recv(1024)
        msg = str(msg.decode('ascii'))

        # Add "O" to the box for server
        box = changeBox("O", postion_to_index[msg])

        # Mark the record for that recieved input
        box_record[int(msg)] = 0

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
