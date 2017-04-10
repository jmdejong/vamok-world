
from lib.opensimplex import OpenSimplex
import time
import random


class MapGenerator:
    
    
    def __init__(self, seed=None, scale=4):
        
        self.seed = seed or int(time.time())
        self.scale = scale
        
        self.random = random.Random()
        
        self.biomes = {
            #"grassheight": OpenSimplex(seed = self.seed),
            #"grasssize": OpenSimplex(seed = self.seed+1),
            "height": OpenSimplex(seed = self.seed)
            }
    
    def getGrass(self, x, y):
        self.random.seed(map(str, (self.seed, x, y)))
        return "grass"+self.random.choice("1234")
    #".,'\""[(self.biomes["grassheight"].noise2d(x/self.scale, y/self.scale)>0)+2*(self.biomes["grasssize"].noise2d(x/self.scale, y/self.scale)>0)]
    
    def getObjects(self, x, y):
        self.random.seed(map(str, (self.seed, x, y, 2)))
        objects = []
        if self.random.random()<0.008:
            objects.append('tree')
        if self.random.random()<0.009:
            objects.append('stone')
        if self.biomes["height"].noise2d(x/400, y/400) > .3:
            objects.append('rock')
        return objects
        
