

class Grid:
    
    
    def __init__(self, width, height, default=0):
        self.width = width
        self.height = height
        self.clear(default)
    
    def clear(self, value):
        self.grid = [value for i in range(self.width*self.height)];
    
    def isValid(self, x, y):
        return x>=0 and y>=0 and x<self.width and y<self.height
    
    def get(self, x, y):
        if self.isValid(x, y):
            return self.grid[x+y*self.width]
        else:
            return None
    
    def set(self, x, y, value):
        if self.isValid(x, y):
            self.grid[x+y*self.width] = value
            return True
        else:
            return False
    
    
    def toString(self):
        return '\n'.join(
            ''.join(
                self.get(x, y) for x in range(self.width)
                ) for y in range(self.height)
            )
    
    def toDict(self):
        data = []
        valuesById = []
        idsByValue = {}
        for char in self.grid:
            if char not in idsByValue:
                charId = len(valuesById)
                valuesById.append(char)
                idsByValue[char] = charId
            charId = idsByValue[char]
            data.append(charId)
        return {
            "width": self.width,
            "height": self.height,
            "data": data,
            "mapping": valuesById
            }
    
