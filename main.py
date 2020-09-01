from gridv2 import Maze

class Main:
    def __init__(self):
        self.maze = Maze(1920,1080,"maze5")
        self.maze.drawMaze()

main = Main()

