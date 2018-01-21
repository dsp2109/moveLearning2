import io, re, socket, sys
import math
import time
import argparse # command line arguements parsing
import os.path # checking file existence, etc
import numpy as np
import tensorflow as tf 
import gym_poker_history
import gym

from baselines import deepq

#helper functions:
import server_parser
from baselines.deepq.experiments import transform_hands_for_gym, constants

DEBUGGING = True
if DEBUGGING:
	import pdb

parser = argparse.ArgumentParser(description='Play heads-up triple draw against a convolutional network. Or see two networks battle it out.')

# To connect with the server!
parser.add_argument('-address', '--address', default='localhost', help='ACPC server/dealer address')
parser.add_argument('-port', '--port', default='48777', help='ACPC server/dealer PORT')

args = parser.parse_args()

"""
Sample client to play ACPC Limit Holdem in Python!
"""

player  = None # no player yet, need to initialize...
address = args.address # 'localhost' # sys.argv[1] 
port	= args.port # 48777 #16177 # 48777 # int(sys.argv[2]) 16177

# Begin talking to the protocol...
if not DEBUGGING:
	sock	= socket.create_connection((address, port))
	sockin  = sock.makefile(mode='rb')

	sock.send('VERSION:2.0.0\r\n')

# MATCHSTATE:0:30:cc/r250c/r500c/r1250c:9s8h|9c6h/8c8d5c/6s/2d
#shit this is limit
matchstate_string = "MATCHSTATE:(\d*):(\d*):([^:]*)"
state_regex = re.compile(r"MATCHSTATE:(\d*):(\d*):([^:]*):([^|]*)\|([^|/]*)/?([^|/]*)/?([^|/]*)/?([^|/]*)")

#start playing
position = None
hand	 = None
now = time.time()
while 1:
	if not DEBUGGING:
		line = sockin.readline().strip()
	else:
		line = "MATCHSTATE:0:30:cc/r250c/r500c/r1250c:9s8h|9c6h/8c8d5c/6s/2d"
		
	if not line:
		break
	print('\n-------------------')
	print(line) # MATCHSTATE:0:998:r:Kc6h|:c

	position, this_hand = map(lambda x: int(x), state.group(1, 2))
	betting = state.group(3)
	cards = state.group(4, 5, 6, 7, 8)

	import pdb ;pdb.set_trace()

	print([position, this_hand, betting])
	if this_hand:
		time_diff = time.time() - now
		print('Took %.1f sec to process %d hands (%.2f average)' % (time_diff, this_hand, time_diff/this_hand))

	# Parse the cards. What is flop, turn, and river? asdf
	oop_hand = cards[0]
	pos_hand = cards[1]
	flop = cards[2]
	turn = cards[3]
	river = cards[4]

	#print([oop_hand, pos_hand, flop, turn, river])
	print([hand_string(x) for x in [oop_hand, pos_hand, flop, turn, river]])

	# Now turn this hand into our hand, and our community cards.

