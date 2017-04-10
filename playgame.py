#! /usr/bin/python3

import sys

if sys.version_info[0] < 3:
    print("This game is written in python 3.\nRun 'python3 "+sys.argv[0]+"' or './"+sys.argv[0]+"'")
    sys.exit(-1)

sys.path.append(sys.path[0]+"/client/")
sys.path.append(sys.path[0]+"/shared/")

import argparse
import getpass
import client


parser = argparse.ArgumentParser(description="The Tron client. Run this to connecto to the tron server. See /home/troido/tron/instructions.txt for more information", epilog="""
Gameplay information:
    Control your player with the arrow keys or wasd. Press 'q' to exit.
    Try not to run in to anything. The last survivor wins the round.
    Currently, a round only restarts when there are no living players left. If you are the last survivor, consider killing yourself to restart the round.

Troubleshooting
    If the game crashes, this could be because the server is not online.
    Run `ps -e | grep hosttron.py` to see if this is the case.
    If the server is offline, try waiting a minute. Cron should restart the server.
    If this does not happen, contact me. See instruction.txt on how to start the server yourself

~Troido""", formatter_class=argparse.RawDescriptionHelpFormatter)
parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username', default=getpass.getuser())
parser.add_argument('-s', '--socket', help='The socket file to connect to. Defaults to /tmp/adventurer_rpg.socket', default="/tmp/adventurer_rpg.socket")
parser.add_argument('-p', '--spectate', help='Join as spectator', action="store_true")
args = parser.parse_args()

client.main(args.name, args.socket, args.spectate)
