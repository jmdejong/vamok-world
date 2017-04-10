
import random
import ground
import player
#import gameobjects
from gameobjects import Wall



class Game:
    
    field = None
    width = 0
    height = 0
    deaths = 0
    
    def __init__(self, width, height):
        self.players = {}
        self.field = ground.Ground()
        self.width = width
        self.height = height
        for x in range(width):
            self.field.addObj(x, 0, Wall())
            self.field.addObj(x, height-1, Wall())
        for y in range(2,height-2):
            self.field.addObj(0, y, Wall())
            self.field.addObj(width-1, y, Wall())
    
    def makePlayer(self,name=None, x=None, y=None ):
        #logging.debug("%s, %s"%(x,y))
        if (name in self.players):
            raise Exception("A player with that name already exists")
        if x == None:
            x = random.randint(5, self.width-5)
        if y == None:
            y = random.randint(5, self.height-5)
        p = player.Player(x, y, self.field, self, name)
        self.players[p.name] = p
        return p.getControlInterface()
    
    def removePlayer(self, name):
        if name in self.players:
            player = self.players[name]
            self.field.removeObj(player.x, player.y, player)
            del self.players[name]
    
    def countPlayers(self):
        return len(self.players)
    
    def getController(self, name):
        return self.players[name].getControlInterface()
    
    def update(self):
        self.deaths = 0
        for player in frozenset(self.players.values()):
            player.update()
