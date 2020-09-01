from turtle import *
from floodfillv2 import FloodFill
from processmaze import genBitmap
import os, math

class Maze:
    def __init__(self,screenx,screeny,mazename):
        hideturtle()
        tracer(0,0)
        speed(3)
        
        self.window = Screen()
        self.window.screensize(screenx,screeny)
        self.window.setup(width=1.0,height=1.0,startx=None,starty=None)

        self.maze = genBitmap(os.path.dirname(os.path.abspath(__file__))+ r"\mazes\{}.bmp".format(mazename))
        self.botx = None
        self.boty = None
        self.botdir = self.findStartDir()
        onscreenclick(self.updateMaze)
        self.currentGoal = [0,0]
        self.solver = FloodFill()
        self.moving = False

    def findStartDir(self):
        for i in self.maze:
            for j in i:
                if j >= 3:
                    return ["e","s","w","n"][j-3]

    def drawBox(self,x1,y1,x2,y2):
        penup()
        goto(x1,y1)
        pendown()
        goto(x1,y2)
        goto(x2,y2)
        goto(x2,y1)
        goto(x1,y1)

    def drawFilledBox(self,x1,y1,x2,y2,c):
        color(c)
        begin_fill()
        self.drawBox(x1,y1,x2,y2)
        end_fill()
        color("black")
        self.drawBox(x1,y1,x2,y2)
        self.drawBox(x1,y1,x2,y2)

    #x123/y123 are pixel offsets from bottom left corner
    def drawBot(self,x1,y1,x2,y2,x3,y3,c):
        color(c)
        penup()
        goto(self.botx+x1,self.boty+y1)
        pendown()
        begin_fill()
        goto(self.botx+x2,self.boty+y2)
        goto(self.botx+x3,self.boty+y3)
        goto(self.botx+x1,self.boty+y1)
        end_fill()
        color("black")
        
    def forward(self):
        if self.botdir == "n":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.boty += 50
            self.drawBot(12,5,38,5,25,45,"blue")
        elif self.botdir == "e":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.botx += 50
            self.drawBot(5,12,5,38,45,25,"blue")
        elif self.botdir == "s":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.boty -= 50
            self.drawBot(12,45,25,5,38,45,"blue")
        elif self.botdir == "w":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.botx -= 50
            self.drawBot(45,12,5,25,45,38,"blue")
            
    def right(self):
        if self.botdir == "n":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(5,12,5,38,45,25,"blue")
            self.botdir = "e"
        elif self.botdir == "e":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(12,45,25,5,38,45,"blue")
            self.botdir = "s"
        elif self.botdir == "s":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(45,12,5,25,45,38,"blue")
            self.botdir = "w"
        elif self.botdir == "w":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(12,5,38,5,25,45,"blue")
            self.botdir = "n"
        
    def left(self):
        if self.botdir == "n":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(45,12,5,25,45,38,"blue")
            self.botdir = "w"
        elif self.botdir == "e":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(12,5,38,5,25,45,"blue")
            self.botdir = "s"
        elif self.botdir == "s":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(5,12,5,38,45,25,"blue")
            self.botdir = "e"
        elif self.botdir == "w":
            self.drawFilledBox(self.botx,self.boty,self.botx+50,self.boty+50,"white")
            self.drawBot(12,45,25,5,38,45,"blue")
            self.botdir = "n"
        
    def drawMaze(self):
        width = len(self.maze[0])
        height = len(self.maze)
        startX = -int((width*50)/2)
        startY = int((height*50)/2)

        for i in range(height):
            for j in range(width):
                xOffset = startX+(50*j)
                if self.maze[i][j] == 0:
                    self.drawFilledBox(xOffset,startY,xOffset+50,startY-50,"white")
                elif self.maze[i][j] == 1:
                    self.drawFilledBox(xOffset,startY,xOffset+50,startY-50,"black")
                elif self.maze[i][j] == 2:
                    self.drawFilledBox(xOffset,startY,xOffset+50,startY-50,"white")
                    self.currentGoal = [j,i]
                else:
                    self.botx = xOffset
                    self.boty = startY-50
                    self.left()
                self.drawBox(xOffset,startY,xOffset+50,startY-50)
                self.drawBox(xOffset,startY,xOffset+50,startY-50)
            startY -= 50

    #click event handler
    def updateMaze(self,x,y):
        inside = self.isInsideMaze(x,y)
        if inside and not self.moving:
            self.moving = True
            coords = self.findTileCoord(x,y)
            if self.maze[coords[1]][coords[0]] != 1 and [coords[0],coords[1]] != self.currentGoal:
                tracer(0,0)
                width = len(self.maze[0])
                height = len(self.maze)
                startX = -int((width*50)/2)

                startY = int((height*50)/2) - 50*self.currentGoal[1]      
                xOffset = startX+50*self.currentGoal[0]
                self.drawFilledBox(xOffset,startY,xOffset+50,startY-50,"white")

                startY = int((height*50)/2) - 50*coords[1]
                xOffset = startX+50*coords[0]
                self.drawFilledBox(xOffset,startY,xOffset+50,startY-50,"gray")

                self.currentGoal = coords
                self.go()
            self.moving = False

    #detects if turtle coordinates are inside the tile grid
    def isInsideMaze(self,x,y):
        size = (((len(self.maze))%2))*25
        if x <= -len(self.maze[0]*25):
            return False
        if x >= len(self.maze[0]*25):
            return False
        if y >= len(self.maze*25):
            return False
        if y <= -len(self.maze*25):
            return False
        return True

    #converts board coordinates to tile grid coordinates
    def findTileCoord(self,x,y):
        size = (((len(self.maze))%2))*25        #deals with odd/even board size offset
        x = 50*math.floor((x+size)/50)          #floors turtle coordinates to multiple of 50
        y = 50*math.floor((y+size)/50)          #floors turtle coordinates to multiples of 50
        xCoord = int(x/50+len(self.maze)/2)     #converts turtle coordinates to tile grid coordinates
        yCoord = int(-(y/50-len(self.maze)/2))  #converts turtle coordinates to tile grid coordinates
        return [xCoord, yCoord]

    def go(self):
        botcoord = self.findTileCoord(self.botx,self.boty)
        self.solver.update(self.maze,[botcoord[0],botcoord[1]],self.currentGoal)
        for direction in self.solver.path():
            if direction != self.botdir:
                self.rotate(direction)
            self.forward()
            penup()
            goto(20000,20000)
            color("white")
            tracer(1,20)
            forward(50)
            tracer(0,0)
            pendown()
            color("black")

            
    def rotate(self,direction):
        possible = ["ne","es","sw","wn","nw","ws","se","en","ns","sn","we","ew"]
        if possible.index(self.botdir+direction) < 4:
            self.right()
        elif possible.index(self.botdir+direction) < 8:
            self.left()
        else:
            self.left()
            self.left()
        self.botdir = direction

        
            
