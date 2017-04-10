

import player

class Wall:
    
    char = 'wall'
    size = 2
    attributes = {
        "solid",
        }


class Rock:
    
    char = 'rock'
    size = 10
    attributes = {
        "solid",
        }
    


class Tree:
    
    char = 'tree'# 🌳♣♠𐇲𐂷
    size = 3
    attributes = {
        "solid",
        }


class Stone:
    
    char = 'stone' # •
    size = 0.2
    attributes = {
        "takable",
        }

class Deer:
    
    char = 'deer'
    size = 1
    



objectdict = {
    "wall": Wall,
    "tree": Tree,
    "player": player.Player,
    "stone": Stone,
    "rock": Rock
    }
