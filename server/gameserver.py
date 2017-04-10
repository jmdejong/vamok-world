#! /usr/bin/python3



import json
import server
from view import View


class PlayerConnection:
    
    name = ""
    initialized = False
    data = ""
    score = 0 # todo: store this somewhere else
    
    def getPlayer(self, game):
        if self.name in game.players:
            return game.players[self.name]
        else:
            return None


class GameServer:
    
    
    def __init__(self, game):
        
        self.serv = server.Server(self.newConnection, self.receive, self.close)
        self.connections = {}
        
        self.game = game
    
    def start(self, address):
        self.serv.start(address)
    
    def sendState(self, game, width, height):
        
        
        
        
        for connection, pc in list(self.connections.items()):
            
            player = pc.getPlayer(game)
            if not player:
                continue
            
            view = View(width, height)
            view.centerOn(player.x, player.y)
            
            screen = view.view(game.field)
            
            output = screen.toString()
            
            field = screen.toDict()
            
            data = {
                "type": "update",
                "field": field,
                "info":{
                    "holding": player.holding.char if player.holding else "nothing",
                    "ground": [obj.char for obj in player.ground.getObjs()]
                }
            }
            
            databytes = bytes(json.dumps(data), 'utf-8')
            self.serv.send(connection, databytes)
    
    def newConnection(self, n):
        self.connections[n] = PlayerConnection()
        with self.game.cv:
            self.game.cv.notify()
    
    def receive(self, n, data):
        data = json.loads(data.decode('utf-8'))
        c = self.connections[n]
        if "name" in data:
            name = data["name"]
            if name in self.game.players:
                self.serv.send(n, bytes(json.dumps({"error":"nametaken"}), "utf-8"))
            else:
                c.name = name
                c.initialized = True
                self.game.players[name] = c
                print("new player: "+name)
        if "input" in data:
            c.data = data["input"]
    
    def close(self, connection):
        if connection in self.connections:
            name = self.connections[connection].name
            del self.connections[connection]
            if name in self.game.players:
                del self.game.players[name]
            if self.game.game:
                self.game.game.removePlayer(name)
            print("player "+name+" left")
    
