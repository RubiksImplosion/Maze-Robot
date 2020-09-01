
class FloodFill:
    class Tile:
        def __init__(self,x,y):
            self.x = x
            self.y = y
            self.px = x
            self.py = y
            self.pdir = None
            self.dist = 0

        def update(self,px,py,dist):
            self.px = px
            self.py = py
            self.dist = dist
            if self.x > px:
                self.pdir = "w"
            elif self.x < px:
                self.pdir = "e"
            elif self.y > py:
                self.pdir = "n"
            else:
                self.pdir = "s"

        def __repr__(self):
            return "pd:{},d:{},{}".format(self.pdir,self.dist,[self.px,self.py])

    def __init__(self):
        self.seen = []
        
    def update(self,maze,bot,end):
        self.maze = maze
        self.bot = bot
        self.considering = [end]
        self.looking = True
        self.nopath = False
        del self.seen[:]
        self.seen = [[None for j in range(len(maze[0]))] for i in range(len(maze))]
        self.seen[end[1]][end[0]] = self.Tile(end[0],end[1])
        self.iterate()

    def iterate(self):
        while self.looking and not self.nopath:
            willconsider = []
            if len(self.considering) == 0:
                self.nopath = True
            else:
                for coord in self.considering:
                    x = coord[0]
                    y = coord[1]
                    if y > 0:
                        if self.check(x,y-1,x,y):
                            willconsider.append([x,y-1])
                    if y < len(self.maze)-1:
                        if self.check(x,y+1,x,y):
                            willconsider.append([x,y+1])
                    if x > 0:
                        if self.check(x-1,y,x,y):
                            willconsider.append([x-1,y])
                    if x < len(self.maze[0])-1:
                        if self.check(x+1,y,x,y):
                            willconsider.append([x+1,y])
            self.considering = willconsider
                        
    def check(self,cx,cy,px,py):
        if [cx,cy] == self.bot:
            self.looking = False
        elif self.maze[cy][cx] == 1:
            return False
        if self.seen[cy][cx] is None:
            self.seen[cy][cx] = self.Tile(cx,cy)
            self.seen[cy][cx].update(px,py,self.seen[py][px].dist+1)
            return True
        elif self.seen[cy][cx].dist > self.seen[py][px].dist+1:
            self.seen[cy][cx].update(px,py,self.seen[py][px].dist+1)
            return True
        else:
            return False
            
    def path(self):
        if self.nopath:
            return []
        else:
            path = []
            tile = self.seen[self.bot[1]][self.bot[0]]
            tracing = True
            while tracing:
                if tile.dist == 0:
                    tracing = False
                else:
                    path.append(tile.pdir)
                    tile = self.seen[tile.py][tile.px]
            return path
