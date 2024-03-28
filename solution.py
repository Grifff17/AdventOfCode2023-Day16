import sys
from functools import cache

directionsCoords = {
    "north": (-1,0),
    "south": (1,0),
    "west": (0,-1),
    "east": (0,1)
}
directionsAdjacent = {
    "north": ("east", "west"),
    "south": ("east", "west"),
    "west": ("north","south"),
    "east": ("north","south")
}
directionsSplitters = {
    "-": ("east", "west"),
    "|": ("north","south"),
}
directionsReflections = {
    ("/", "north"): "east",
    ("/", "east"): "north",
    ("/", "south"): "west",
    ("/", "west"): "south",
    ("\\", "north"): "west",
    ("\\", "west"): "north",
    ("\\", "south"): "east",
    ("\\", "east"): "south"
}


def solvepart1():
    data = fileRead("input.txt")
    data = [ row.strip() for row in data ]

    global grid
    grid = data.copy()
    global visitedSpaces
    visitedSpaces = []
    global energizedSpaces
    energizedSpaces = []

    sys.setrecursionlimit(100000)
    laserTraverse((0,0),"east")

    print(len(energizedSpaces))
    
#recursively travel a laser through the maze, ending when it reaches an edge or forms an infinite loop
def laserTraverse(pos, dir):
    if [pos, dir] in visitedSpaces or pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
        return 0

    visitedSpaces.append([pos, dir])
    if pos not in energizedSpaces:
        energizedSpaces.append(pos)

    spaceContents = grid[pos[0]][pos[1]]
    outDirections = ()
    if spaceContents == ".":
        outDirections = [dir]
    if spaceContents in ("|","-"):
        if dir in directionsSplitters[spaceContents]:
            outDirections = [dir]
        else:
            outDirections = list(directionsAdjacent[dir])
    if spaceContents in ("\\","/"):
        outDirections = [directionsReflections[(spaceContents,dir)]]

    for newDir in outDirections:
        newPos = tuple([ sum(coords) for coords in zip(pos, directionsCoords[newDir]) ])
        laserTraverse(newPos, newDir)

def solvepart2():
    data = fileRead("input.txt")
    data = [ row.strip() for row in data ]
    
    global grid
    grid = data.copy()
    global visitedSpaces
    visitedSpaces = []

    sys.setrecursionlimit(100000)
    greatestEnergized = 0

    for i in range(len(grid)):
        visitedSpaces = []
        val = len(laserTraverseCaching((i,0),"east"))
        print(i, "east", val)
        if val > greatestEnergized:
            greatestEnergized = val
        visitedSpaces = []
        val = len(laserTraverseCaching((i,len(grid[0])-1),"west"))
        print(i, "west", val)
        if val > greatestEnergized:
            greatestEnergized = val
    for i in range(len(grid[0])):
        visitedSpaces = []
        val = len(laserTraverseCaching((0,i),"south"))
        print(i, "south", val)
        if val > greatestEnergized:
            greatestEnergized = val
        visitedSpaces = []
        val = len(laserTraverseCaching((len(grid)-1,i),"north"))
        print(i, "north", val)
        if val > greatestEnergized:
            greatestEnergized = val

    print("")
    print(greatestEnergized)

#recursively travel a laser through the maze, ending when it reaches an edge or forms an infinite loop
#@cache
def laserTraverseCaching(pos, dir):
    global visitedSpaces
    if [pos, dir] in visitedSpaces or pos[0] < 0 or pos[0] >= len(grid) or pos[1] < 0 or pos[1] >= len(grid[0]):
        return ()

    visitedSpaces.append([pos, dir])

    spaceContents = grid[pos[0]][pos[1]]
    outDirections = ()
    if spaceContents == ".":
        outDirections = [dir]
    if spaceContents in ("|","-"):
        if dir in directionsSplitters[spaceContents]:
            outDirections = [dir]
        else:
            outDirections = list(directionsAdjacent[dir])
    if spaceContents in ("\\","/"):
        outDirections = [directionsReflections[(spaceContents,dir)]]

    energizedSpaces = ()
    for newDir in outDirections:
        newPos = tuple([ sum(coords) for coords in zip(pos, directionsCoords[newDir]) ])
        energizedSpaces = energizedSpaces + (pos,) + laserTraverseCaching(newPos, newDir)
    return tuple(set(energizedSpaces))

def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart2()
