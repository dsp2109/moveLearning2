# If you create your own bot, it should take two commandline arguments, the IP address and the port of the dealer to connect to.

# Code needs
# -1- Open a socket to the proper IP/port
# -2- Read in Message like "MATCHSTATE:0:30:cc/:9s8h|/8c8d5c"
# -3- Parse the above message to obtain the state information your bot needs to act
# -4- Give the state information to your bot 
# -5- Wait for your bot to supply a decision/action
# -6- Encode the action into a String the ACPC server expects
# -7- Send your "action message" to the ACPC server over the socket.

from sys import argv
print(argv)  # Note the first argument is always the script filename.

import argparse

parser = argparse.ArgumentParser(description='Get IP and port for poker bot.')
parser.add_argument('ip', type=str,
                   help='The IP address to connect to for the dealer')
parser.add_argument('port', help='port of the dealer to connect to')

args = parser.parse_args()
print(args.ip, args.port)

import socket
s = socket.socket()

ip = argv[1] #
port = argv[2] # to be read in from server

# s.connect((ip,port))
# s.send("my request\r")
# print(s.recv(4096))
# s.close()


# testing a connection
s = socket.socket()
address = '127.0.0.1'
port = 80  # port number is a number, not string
try:
    s.connect((address, port)) 
    # originally, it was 
    # except Exception, e: 
    # but this syntax is not supported anymore. 
except Exception as e: 
    print("something's wrong with %s:%d. Exception is %s" % (address, port, e))
finally:
    s.close()