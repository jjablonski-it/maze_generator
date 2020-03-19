import math, random, sys
from components import Settings
from components import Window
from components import Cell

#Global variables
height = Settings.height
width = Settings.width

class Maze:
    def __init__(self, mazeRes):
        self.mazeRes = mazeRes
        self.grid = []
        self.stack = []
        self.cellSize = width // (mazeRes + 2)
        self.start = None
        self.end = None

        #Real size
        self.rWidth = math.floor(width/self.cellSize)-2
        self.rHeight = math.floor(height/self.cellSize)-2

    #Drawing all the cells and marking current
    def draw(self, current):
        for g in self.grid:
            if not g.visited:
                g.color = 'gray'
            if g == current:
                g.baseColor = 'red'
            else: 
                g.baseColor = None
                g.color = 'white'
            if g == self.start:
                g.baseColor = 'green'
            elif g == self.end:
                g.baseColor = 'red'
            g.show()

    #Fill cells objects to grid array
    def fillGrid(self):
        for i in range(self.rHeight):
            for j in range(self.rWidth):
                self.grid.append(Cell.Cell(j, i, self))
        self.start = self.grid[0]
        self.end = self.grid[-1]
    
    #Checking if all cells have been visited already
    def allVisited(self):
        for i in self.grid:
            if(not i.visited):
                return False
        return True

    #Main function for generating maze (Recursive backtracker algorithm)
    def generateMaze(self, animate, mazeSize):
        self.__init__(mazeSize)
        self.fillGrid()

        current = self.start          #Selecting first cell

        #Maze generating loop
        while(not self.allVisited()):
            current.visited = True  #Mark current as visited
                
            #Get active neighbours list for current cell
            neighbours = current.activeNeighbourList()  
            if (neighbours):    #If list of neighbours is not empty
                next = random.choice(neighbours)    #Choosing next random neighbour cell
                self.stack.append(current)          #Add to stack
                self.removeWalls(current, next)          #Remove walls
                current.options.append(next)        #Add next to options array
            else:               #If there is no neighbour to visit pop (go back) 
                next = self.stack.pop()
            
            current = next          #Changing current cell
            Window.canvas.update()         #Updating canvas
            
            if animate:                 #Only if animating
                Window.canvas.delete('all')    #Clear canvas
                self.draw(current)           #Drawing canvas

        Window.canvas.delete('all')    #Clear canvas
        self.draw(None)              #Draw maze

    #Main function for fidning path (A* algorithm)
    def pathFinding(self, animate):  
        self.resetChecked()   
        current = self.start        #Starting cell
        current.checked = True      #Marking as checked
        allOpts = []                #Array of next move options
        while (current != self.end):     #Loop while cell isn't the ending cell
            options = current.options       #Get possible cells from current cell object
            fCostDict = {}                  #Dictionary with fCost as key and cell object as value (my weird sorting idea)
            if options:
                for option in options:         #option - CELL
                    if (not option.checked):            #Check if it is checked 
                        allOpts.append(option)                      #Add new possible cells to check from CELL option
                        option.gCost = option.distance(self.start)       #Setting gCost(distance from start)
                        option.hCost = option.distance(self.end)         #Setting hCost(distance to end)
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
                Window.canvas.delete('all')            #Clear canvas
                self.recursionDrawing(current)       #Draw line from current to start
                self.draw(None)                      #Redraw canvas
                Window.canvas.update()                 #Update changes
        
        #Display at the end
        Window.canvas.delete('all')            #Clear canvas
        self.recursionDrawing(current)       #Draw line from current to start
        self.draw(None)                      #Redraw canvas
        Window.canvas.update()

    #Reset checked
    def resetChecked(self):
        for cell in self.grid:
            cell.checked = False

    #Recursion line drawing function from each node parent unil not start cell
    def recursionDrawing(self, node):             
        parent = node.parent
        if parent:
            node.lineTo(parent, 'red')
            self.recursionDrawing(parent)

    #Function that removes the walls between the cells depending on the direction
    def removeWalls(self, cCell, nCell):
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

