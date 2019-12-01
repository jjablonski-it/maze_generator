import tkinter as tkr
from settings import width, height, navHeight, mazeRes

#Canvas global variable
canvas = None

#Set up tkinter window
def setupWindow():
    global topFrame, root
    root = tkr.Tk()
    root.geometry('{}x{}'.format(width,height+navHeight+2))
    root.resizable(False, False)

    #Navigation panel
    topPanel = tkr.Frame(root)
    topPanel.pack()

    #Set up navigation
    topFrame = tkr.Frame(root, bg='#000', height=50)
    topFrame.pack(expand=False, fill=tkr.X)

def setupInputs(maze):
    #Buttons for generating
    generateButton = tkr.Button(topFrame, text="Generatre maze", command=lambda : maze.generateMaze(False, sizeSlider.get()))
    generateButton.pack(side=tkr.LEFT, pady=navHeight/4, padx=50)

    #Buttons for path finding
    findpathButton = tkr.Button(topFrame, text="Find path", command=lambda : maze.pathFinding(False))
    findpathButton.pack(side=tkr.RIGHT, pady=navHeight/4, padx=50)

    #Slider
    sizeSlider = tkr.Scale(topFrame, orient=tkr.HORIZONTAL, length=200, from_=2, to=99)
    sizeSlider.pack(pady=5)
    sizeSlider.set(mazeRes)

#Function creating canvas
def setupCanvas():
    global canvas
    canvas = tkr.Canvas(root, bg='#000')
    canvas.pack(side=tkr.BOTTOM, expand=True, fill=tkr.BOTH)

#Debbuging animate options
    #Set up buttons
    #Generating
    # animGenerate = tkr.BooleanVar()
    # animGenerateB = tkr.Checkbutton(topFrame, text='Animate', variable=animGenerate)
    # animGenerateB.pack(side=tkr.LEFT)
    #Pathfinding
    # animPath = tkr.BooleanVar()
    # animPathB = tkr.Checkbutton(topFrame, text='Animate', variable=animPath)
    # animPathB.pack(side=tkr.RIGHT)