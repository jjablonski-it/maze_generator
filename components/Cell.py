import math
from components import Window

#Global variables
canvas = Window.canvas

class Cell:
    def __init__(self, x, y, maze):
        self.x = x              #Column
        self.y = y              #Row
        self.color = 'white'    #Wall color
        self.baseColor = None   #Square color
        self.visited = False    #Already visited boolean   
        self.maze = maze     

        #Real position
        self.rX = x*self.maze.cellSize+maze.cellSize
        self.rY = y*maze.cellSize+maze.cellSize

        #Path finding
        self.checked = False    #Already check in path finding boolean
        self.parent = None      #Node where it came from
        self.options = []       #Posible move options

        #Which walls exist
        self.walls = {
            'top': True,
            'right': True,
            'bottom': True,
            'left': True
        }

        #Grid is 1d array so calculate postion in array with x and y
    def index(self, x, y):
        if(x<0 or y<0 or x>self.maze.rWidth-1 or y>self.maze.rHeight-1):
            return None
        return x+y*self.maze.rHeight

    #Add to array all active neighbors of itself
    def activeNeighbourList(self):
        neighbours = []   
        i = self.index(self.x, self.y+1)
        if(i and not self.maze.grid[i].visited):      #top
            neighbours.append(self.maze.grid[i])
        i = self.index(self.x+1, self.y)    
        if(i and not self.maze.grid[i].visited):      #right
            neighbours.append(self.maze.grid[i])
        i = self.index(self.x, self.y-1)    
        if(i and not self.maze.grid[i].visited):      #bottom
            neighbours.append(self.maze.grid[i])      
        i = self.index(self.x-1, self.y)    
        if(i and not self.maze.grid[i].visited):      #left
            neighbours.append(self.maze.grid[i])
        return neighbours
    
    #Draw itself on a global canvas
    def show(self):
        #Drawing square
        if(self.baseColor):
            canvas.create_rectangle(self.rX, self.rY, self.rX+self.maze.cellSize, self.rY+self.maze.cellSize, fill=self.baseColor)

        #Drawing walls
        if(self.walls['top']):
            canvas.create_line(self.rX, self.rY, self.rX+self.maze.cellSize, self.rY, fill=self.color)                        #top
        if(self.walls['right']):
            canvas.create_line(self.rX+self.maze.cellSize, self.rY, self.rX+self.maze.cellSize, self.rY+self.maze.cellSize, fill=self.color)      #right
        if(self.walls['bottom']):
            canvas.create_line(self.rX, self.rY+self.maze.cellSize, self.rX+self.maze.cellSize, self.rY+self.maze.cellSize, fill=self.color)      #bottom
        if(self.walls['left']):
            canvas.create_line(self.rX, self.rY, self.rX, self.rY+self.maze.cellSize, fill=self.color)                        #left

    #Function calculating distance to a given cell
    def distance(self, cell):
        return math.floor(math.sqrt((self.x-cell.x)**2+(self.y-cell.y)**2)*10)

    #Draw line from itself to given cell with chosen color
    def lineTo(self, cell, color):
        canvas.create_line(self.rX + self.maze.cellSize/2, self.rY + self.maze.cellSize/2, cell.rX + self.maze.cellSize/2, cell.rY + self.maze.cellSize/2, fill=color)