#! /usr/bin/python3

import sys

import curses
import threading
#import logging
import json
import getpass
import argparse
from connection import Connection
from screen import Screen

# todo: remove references to tron

#logging.basicConfig(filename="client.log", filemode='w', level=logging.DEBUG)


class Client:
    
    def __init__(self, stdscr, name="___", address="/tmp/tron_socket", spectate=False):
        self.stdscr = stdscr
        self.screen = Screen(stdscr)
        
        self.name = name
        
        self.keepalive = True
        
        self.connection = Connection()
        self.connection.connect(address)
        if not spectate:
            self.connection.send(json.dumps({"name":name}))
        
        self.fieldWidth = 0
        self.fieldHeight = 0
        
        with open("client/characters.json") as f:
            self.characters = json.load(f)['ascii']
        
        threading.Thread(target=self.listen, daemon=True).start()
        self.command_loop()
    
    def listen(self):
        self.connection.listen(self.update, self.close)
    
    def close(self, err=None):
        self.keepalive = False
        sys.exit()
    
    def update(self, databytes):
        if not self.keepalive:
            sys.exit()
        datastr = databytes.decode('utf-8')
        data = json.loads(datastr)
        if 'error' in data:
            if data['error'] == "nametaken":
                print("error: name is already taken", file=sys.stderr)
                self.close()
        if 'field' in data:
            self.fieldWidth = data['field']['width']
            self.fieldHeight = data['field']['height']
            fieldCells = data['field']['data']
            mapping = data['field']['mapping']
            self.screen.put('\n'.join(
                ''.join(
                    self.characters.get(mapping[fieldCells[x + y*self.fieldWidth]], '?') for x in range(self.fieldWidth)
                    ) for y in range(self.fieldHeight)
                ))
        if 'info' in data:
            self.screen.putPlayers(json.dumps(data['info'], indent=2), self.fieldWidth+2)
        self.screen.refresh()
    
    def command_loop(self):
        
        commands = {
            ord("w"): "north",
            curses.KEY_UP: "north",
            ord("s"): "south",
            curses.KEY_DOWN: "south",
            ord("d"): "east",
            curses.KEY_RIGHT: "east",
            ord("a"): "west",
            curses.KEY_LEFT: "west",
            ord("e"): "take",
            ord("q"): "drop",
            ord("W"): "fastnorth",
            ord("S"): "fastsouth",
            ord("D"): "fasteast",
            ord("A"): "fastwest"
        }
        
        while self.keepalive:
            key = self.stdscr.getch()
            if key == 27:
                self.keepalive = False
            if key in commands:
                self.connection.send(json.dumps({"input":commands[key]}))


def main(name, socket, spectate=False):
    
    
    def start(stdscr):
        client = Client(stdscr, name, socket, spectate)
    
    curses.wrapper(start)
    

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help='Your player name (must be unique!). Defaults to username', default=getpass.getuser())
    parser.add_argument('-s', '--socket', help='The socket file to connect to. Defaults to /tmp/tron_socket', default="/tmp/tron_socket")
    parser.add_argument('-p', '--spectate', help='Join as spectator', action="store_true")
    args = parser.parse_args()
    
    main(args.name, args.socket, args.spectate)
    

