import tkinter as tkr
import math, random, sys
from components import Settings

#Increse limit of recursion
sys.setrecursionlimit(10000)

#Import window file
from components import Window
Window.setupWindow()
Window.setupCanvas()

#Import maze file
from components import Maze

#Create maze object
maze = Maze.Maze(Settings.mazeRes)

#Set buttons
Window.setupInputs(maze)

#Generate starting maze
maze.generateMaze(False, Settings.mazeRes)

Window.root.mainloop()