import tkinter as tkr
import math, random, sys
from settings import mazeRes

#Increse limit of recursion
sys.setrecursionlimit(10000)

#Import window file
import window
window.setupWindow()
window.setupCanvas()

#Import maze file
from maze import Maze

#Create maze object
maze = Maze(mazeRes)

#Set buttons
window.setupInputs(maze)

#Generate starting maze
maze.generateMaze(False, mazeRes)

window.root.mainloop()