
import random
import mapgenerator
from gameobjects import objectdict

class Ground:
    
    field = []
    #ground = []
    width = 0
    height = 0
    
    def __init__(self):
        
        self.field = {}
        self.mapGenerator = mapgenerator.MapGenerator(scale=8)
    
    def get(self, x, y):
        if (x, y) not in self.field:
            groundPatch = GroundPatch(char=self.mapGenerator.getGrass(x, y))
            for objecttype in self.mapGenerator.getObjects(x, y):
                groundPatch.addObj(objectdict[objecttype]())
            self.field[(x,y)] = groundPatch
        return self.field[(x, y)]
    
    def addObj(self, x, y, obj):
        p = self.get(x, y).addObj(obj)
        
    def removeObj(self, x, y, obj):
        self.get(x, y).removeObj(obj)


    
class GroundPatch:
    
    #height = 0
    size = 0
    char = ' '
    objects = None
    
    def __init__(self, char=' '):
        #self.height = height
        # objects is actually a set, but because its elements are mutable
        # it is implemented as a dictionary with the id as index
        self.objects = {}
        self.char = char
    
    def accesible(self):
        return not any("solid" in obj.attributes for obj in self.objects.values())
    
    def addObj(self, obj):
        self.objects[id(obj)] = obj
    
    def removeObj(self, obj):
        if id(obj) in self.objects:
            del self.objects[id(obj)]
    
    def getObjs(self):
        return self.objects.values()
    
    def getTopObj(self):
        topObj = self
        for obj in self.getObjs():
            if obj.size > topObj.size:
                topObj = obj
        return topObj
