



class Player:
    
    char = 'player'
    size = 2
    direction = None
    attributes = {}
    
    def __init__(self, x, y, field, game, name=None):
        self.controller = {}
        self.game = game
        self.name = name or str(id(self))
        #self.char = self.name[0]
        self.x = x
        self.y = y
        self.ground = None
        self.field = field
        self.place(x, y)
        self.holding = None
        #self.direction = random.choice(["north", "south", "east", "west"])
    
    def getControlInterface(self):
        return self.controller
    
    def place(self, x, y):
        if self.field:
            self.field.removeObj(self.x, self.y, self)
            self.field.addObj(x, y, self)
            self.ground = self.field.get(x,y)
        self.x = x
        self.y = y
            
    
    def update(self):
        
        #dx = bool("east" in self.controller and self.controller["east"]) - bool("west" in self.controller and self.controller["west"])
        #dy = bool("south" in self.controller and self.controller["south"]) - bool("north" in self.controller and self.controller["north"])
        
        if "action" in self.controller:
            if self.controller["action"] in {"north", "east", "south", "west"}:
                direction = self.controller["action"]
                dx = (direction == "east") - (direction == "west")
                dy = (direction == "south") - (direction == "north")
                
                newx = self.x + dx
                newy = self.y + dy
                
                if self.field.get(newx, newy).accesible():
                    self.place(newx, newy)
            
            
            if self.controller["action"] in {"fastnorth", "fasteast", "fastsouth", "fastwest"}:
                direction = self.controller["action"]
                dx = (direction == "fasteast") - (direction == "fastwest")
                dy = (direction == "fastsouth") - (direction == "fastnorth")
                
                dx *= 10
                dy *= 10
                
                newx = self.x + dx
                newy = self.y + dy
                
                if self.field.get(newx, newy).accesible():
                    self.place(newx, newy)
            
            place = self.field.get(self.x, self.y)
            
            if self.controller["action"] == "drop" and self.holding:
                place.addObj(self.holding)
                self.holding = None
            
            if self.controller["action"] == "take" and not self.holding:
                #place = self.field.get(self.x, self.y)
                for obj in place.getObjs():
                    if "takable" in obj.attributes:
                        place.removeObj(obj)
                        self.holding = obj
                        break
            
            del self.controller["action"]
    
    def die(self):
        self.game.removePlayer(self.name)
        self.game.deaths += 1
        


