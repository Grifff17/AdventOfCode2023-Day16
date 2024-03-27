import sys

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


def fileRead(name):
    data = []
    f = open(name, "r")
    for line in f:
        data.append(line);
    return data

solvepart1()