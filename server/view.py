
import grid

class View:
    
    
    def __init__(self, viewWidth, viewHeight):
        self.width = viewWidth
        self.height = viewHeight
        self.x = 0
        self.y = 0
    
    def move(self, x, y):
        self.x = x
        self.y = y
        
    def centerOn(self, x, y):
        self.x = x - int(self.width/2)
        self.y = y - (self.height/2)
    
    def view(self, ground):
        
        screen = grid.Grid(self.width, self.height)
        
        #for i in range(-math.pi/2, math.pi/2, .1):
        #heights = castRays(ground, self.x, self.y ,self.dir,self.width/2, screen.width, 30)
        
        for x in range(self.width):
            for y in range(self.height):
                screen.set(x, y, ground.get(self.x + x, self.y + y).getTopObj().char)
        
        return screen
