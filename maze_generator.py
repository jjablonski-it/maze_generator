import tkinter as tkr
import math, random, time, sys

#Increse limit of recursion
sys.setrecursionlimit(10000)

#Size and resolution of canvas
navHeight=50
cellSize=20
height=width=600

#Real size
rWidth = math.floor(width/cellSize)-2
rHeight = math.floor(height/cellSize)-2

#Set up window
window = tkr.Tk()
window.geometry('{}x{}'.format(width,height+navHeight))
window.resizable(False, False)

topPanel = tkr.Frame(window)
topPanel.pack()

#Set up navigation
topFrame = tkr.Frame(window, bg='#000', height=50)
topFrame.pack(expand = False, fill=tkr.X)

#Set up buttons
generateButton = tkr.Button(topFrame, text="Generatre maze", command=lambda : generateMaze(False, 50))
generateButton.pack(side=tkr.LEFT, pady=navHeight/4, padx=25)
findpathButton = tkr.Button(topFrame, text="Find path", command=lambda : pathFinding(False, 0))
findpathButton.pack(side=tkr.RIGHT, pady=navHeight/4, padx=25)

#Set up canvas
canvas = tkr.Canvas(window, bg='#000')
canvas.pack(side=tkr.BOTTOM, expand=True, fill=tkr.BOTH)

class Maze:
    def __init__(self):
        self.grid = []
        self.stack = []
        self.start = None
        self.end = None
    
    def fillGrid(self):
        for i in range(rHeight):
            for j in range(rWidth):
                self.grid.append(Cell(j, i))
        self.start = self.grid[0]
        self.end = self.grid[-1]

    #Checking if all cells have been visited already
    def allVisited(self):
        for i in self.grid:
            if(not i.visited):
                return False
        return True


class Cell:
    def __init__(self, x, y):
        self.x = x              #Column
        self.y = y              #Row
        self.color = 'white'    #Wall color
        self.baseColor = None   #Square color
        self.visited = False    #Already visited boolean        

        #Real position
        self.rX = x*cellSize+cellSize
        self.rY = y*cellSize+cellSize

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

    #Add to array all active neighbors of itself
    def activeNeighbourList(self):
        neighbours = []   
        i = index(self.x, self.y+1)
        if(i and not maze.grid[i].visited):      #top
            neighbours.append(maze.grid[i])
        i = index(self.x+1, self.y)    
        if(i and not maze.grid[i].visited):      #right
            neighbours.append(maze.grid[i])
        i = index(self.x, self.y-1)    
        if(i and not maze.grid[i].visited):      #bottom
            neighbours.append(maze.grid[i])      
        i = index(self.x-1, self.y)    
        if(i and not maze.grid[i].visited):      #left
            neighbours.append(maze.grid[i])
        return neighbours
    
    #Draw itself on a global canvas
    def show(self):
        #Drawing square
        if(self.baseColor):
            canvas.create_rectangle(self.rX, self.rY, self.rX+cellSize, self.rY+cellSize, fill=self.baseColor)

        #Drawing walls
        if(self.walls['top']):
            canvas.create_line(self.rX, self.rY, self.rX+cellSize, self.rY, fill=self.color)                        #top
        if(self.walls['right']):
            canvas.create_line(self.rX+cellSize, self.rY, self.rX+cellSize, self.rY+cellSize, fill=self.color)      #right
        if(self.walls['bottom']):
            canvas.create_line(self.rX, self.rY+cellSize, self.rX+cellSize, self.rY+cellSize, fill=self.color)      #bottom
        if(self.walls['left']):
            canvas.create_line(self.rX, self.rY, self.rX, self.rY+cellSize, fill=self.color)                        #left

    #Function calculating distance to a given cell
    def distance(self, cell):
        return math.floor(math.sqrt((self.x-cell.x)**2+(self.y-cell.y)**2)*10)

    #Draw line from itself to given cell with chosen color
    def lineTo(self, cell, color):
        canvas.create_line(self.rX + cellSize/2, self.rY + cellSize/2, cell.rX + cellSize/2, cell.rY + cellSize/2, fill=color)

#Grid is 1d array so calculate postion in array with x and y
def index(x, y):
    if(x<0 or y<0 or x>rWidth-1 or y>rHeight-1):
        return None
    return x+y*rHeight

#Drawing all the cells and marking current
def draw(current):
    for g in maze.grid:
        if not g.visited:
            g.color = 'gray'
        if g == current:
            g.baseColor = 'red'
        else: 
            g.baseColor = None
            g.color = 'white'
        if g == maze.start:
            g.baseColor = 'green'
        elif g == maze.end:
            g.baseColor = 'red'
        g.show()

#Function that removes the walls between the cells depending on the direction
def removeWalls(cCell, nCell):
    if(cCell.x - nCell.x < 0):
        cWall, nWall = 'right', 'left'
    elif(cCell.x - nCell.x > 0):
        cWall, nWall = 'left', 'right'
    elif(cCell.y - nCell.y < 0):
        cWall, nWall = 'bottom', 'top'
    elif(cCell.y - nCell.y > 0):
        cWall, nWall = 'top', 'bottom'
    if(cWall and nWall):
        cCell.walls[cWall] = False
        nCell.walls[nWall] = False

#Main function for generating maze (Recursive backtracker algorithm)
def generateMaze(animate, delay_ms):
    global maze
    maze = Maze()
    maze.fillGrid()

    current = maze.start          #Selecting first cell
    speed = 1/1000 * delay_ms   #Delay between frames in ms

    #Maze generating loop
    while(not maze.allVisited()):
        current.visited = True  #Mark current as visited
            
        #Get active neighbours list for current cell
        neighbours = current.activeNeighbourList()  
        if (neighbours):    #If list of neighbours is not empty
            next = random.choice(neighbours)    #Choosing next random neighbour cell
            maze.stack.append(current)          #Add to stack
            removeWalls(current, next)          #Remove walls
            current.options.append(next)        #Add next to options array
        else:               #If there is no neighbour to visit pop (go back) 
            next = maze.stack.pop()
        
        current = next          #Changing current cell
        canvas.update()         #Updating canvas
        
        if animate:                 #Only if animating
            canvas.delete('all')    #Clear canvas
            draw(current)           #Drawing canvas
            time.sleep(speed)       #Delay for each frame

    canvas.delete('all')    #Clear canvas
    draw(None)              #Draw maze

#Main function for fidning path (A* algorithm)
def pathFinding(animate, delay_ms):         
    current = maze.start             #Starting cell
    current.checked = True      #Marking as checked
    allOpts = []                #Array of next move options
    while (current != maze.end):     #Loop while cell isn't the ending cell
        options = current.options       #Get possible cells from current cell object
        fCostDict = {}                  #Dictionary with fCost as key and cell object as value (my weird sorting idea)
        if options:
            for option in options:         #option - CELL
                if (not option.checked):            #Check if it is checked 
                    allOpts.append(option)                      #Add new possible cells to check from CELL option
                    option.gCost = option.distance(maze.start)       #Setting gCost(distance from start)
                    option.hCost = option.distance(maze.end)         #Setting hCost(distance to end)
                    option.fCost = option.gCost + option.hCost  #Setting fCost(sum of gCost and hCost)
                    option.checked = True           #Mark as checked
                option.parent = current             #Set cell's parent
        for option in allOpts:                      #Check all options for the lowest fCost possible
            fCostDict[option.fCost] = option        #Adding all options to dictionary (fCost - key, cell object - value)
        next = fCostDict[sorted(fCostDict)[0]]      #Chosing next from sorting fCostDict keys and picking the lowest one (0)
        allOpts.remove(next)                        #Remove used cell from options
        current = next                              #Set next current cell

        #Drawing part
        if(animate):
            canvas.delete('all')            #Clear canvas
            recursionDrawing(current)       #Draw line from current to start
            draw(None)                      #Redraw canvas
            canvas.update()                 #Update changes
            time.sleep(delay_ms)
    
    #Display at the end
    canvas.delete('all')            #Clear canvas
    recursionDrawing(current)       #Draw line from current to start
    draw(None)                      #Redraw canvas
    canvas.update()

#Recursion line drawing function from each node parent unil not start cell
def recursionDrawing(node):             
    parent = node.parent
    if parent:
        node.lineTo(parent, 'red')
        recursionDrawing(parent)

#'Main'
maze = Maze()
maze.fillGrid()

#Update canvas
canvas.update()

window.mainloop()