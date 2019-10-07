from math import *
from tkinter import *

class moleculeJunction:
    def __init__(self, x=0, y=0, sourceJunction = None, direction = 0, distance = 0, atom = "", label = "", chainExtention = 0):
        self.outJunctions = []
        if sourceJunction == None:
            self.x = x
            self.y = y
        else:
            self.x = sourceJunction.x + cos(direction * pi/180) * distance
            self.y = sourceJunction.y + sin(direction * pi/180) * distance
            self.outJunctions += [(direction + 180) % 360]
            sourceJunction.outJunctions += [direction]
        
        self.atom = atom
        self.label = label
        self.chainExtention = 0
    
    def getNextDirection(self, n):
        root = 0
        d = 360
        if len(self.outJunctions) == 1:
            root = (self.outJunctions[0] + 1080) % 360
            if n == 1:
                return [root + 120]
        if len(self.outJunctions) >= 2:
            a1 = (self.outJunctions[0] + 1080) % 360
            a2 = (self.outJunctions[1] + 1080) % 360

            if a2 < a1:
                tmp = a1
                a1 = a2
                a2 = tmp

            d = a2 - a1
            root = a1
            if d < 180:
                root = a2
                d = 360 - d
            
        directions = []
        for i in range(n):
            directions += [root + (i+1) * d / (n + 1)]
        
        return directions
    
    def draw(self, canvas, x, y):
        canvas.create_text(self.x + x, self.y + y, text=self.label)
    
class moleculeBond:
    def __init__(self, junction1, junction2, number):
        self.junction1 = junction1
        self.junction2 = junction2
        self.number = number
    
    def draw(self, canvas, x, y):
        x1 = self.junction1.x + x
        y1 = self.junction1.y + y
        x2 = self.junction2.x + x
        y2 = self.junction2.y + y

        d = hypot(x2-x1, y2-y1)
        dx = (y2-y1)/d * 3
        dy = (x1-x2)/d * 3

        canvas.create_line( x1, y1, x2, y2 )

        if self.number > 1:
            canvas.create_line( x1 + dx, y1 + dy, x2 + dx, y2 + dy)
        if self.number > 2:
            canvas.create_line( x1 - dx, y1 - dy, x2 - dx, y2 - dy)