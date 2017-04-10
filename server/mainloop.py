

import gameserver
from game import Game
from drawfield import DrawField
import argparse
import threading
import time
import os
import signal
import sys

WIDTH = 80
HEIGHT = 40


class TronGame:
    
    def __init__(self):
        
        self.server = gameserver.GameServer(self)
        self.players = {}
        
    def start(self, address="/tmp/adventurer_rpg.socket"):
        
        
        
        def cleanup(*args):
            print(args)
            print("cleaning")
            try:
                os.unlink(address)
            except FileNotFoundError:
                if os.path.exists(address):
                    raise
            sys.exit(0)
        
        signal.signal(signal.SIGTERM, cleanup)
        
        self.cv = threading.Condition()
        
        self.server.start(address)
        try:
            while True:
                self.game_round()
        except Exception:
            raise
        finally:
            try:
                os.unlink(address)
            except FileNotFoundError:
                print("catching")
                if os.path.exists(address):
                    raise
        
        
    
    def game_round(self):
        self.game = Game(WIDTH, HEIGHT)
        for name in self.players:
            self.game.makePlayer(name)
        
        self.game_loop()
    
    
    def game_loop(self):
        
        keepRunning = True
        while keepRunning:
            
            self.update()
            #keepRunning = self.game.countPlayers() > 0
            self.sendState()
            time.sleep(0.05)
    
    def update(self):
        
        for c in self.players.values():
            command = c.data
            player = c.name
            c.data = None
            if player not in self.game.players:
                self.game.makePlayer(player)
            if command and player in self.game.players:
                controller = self.game.getController(player)
                controller["action"] = command #if command in {"fd", "back", "right", "left"} else ""
        
        lastCount = self.game.countPlayers()
        self.game.update()
        if self.game.deaths:
            for name in self.game.players:
                self.players[name].score += 1
    
    def sendState(self):
        
        output = DrawField(self.game.field, 0, 0, WIDTH, HEIGHT).toString()
        
        self.server.sendState(self.game, WIDTH, HEIGHT)
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-s', '--socket', help='The socket file to listen to. Use this if the default socket exists already.\nWARNING: if the given file exists it will be overwritten.\nDefaults to /tmp/tron_socket', default="/tmp/tron_socket")
    args = parser.parse_args()
    
    TronGame().start(args.socket)
