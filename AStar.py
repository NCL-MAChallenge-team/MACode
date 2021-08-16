#dimensions of lake
width = 16
height = 12
nm = 926 #how many miles per half nm

class NautMile: #class to make nautical miles
    def __init__(self, inx, iny):
        self.x = inx
        self.y = iny
        self.g = 0
        self.h = 0
        self.cost = 0
        self.open = False
        self.closed = False
        self.bestParent = 0

nautmiles = [0] * (width * height) #define nautmiles list with placeholders
for x in range(width): #make nautmiles objects
    for y in range (height):
        index = ((height - 1 - y) * width)+x #calculate index reference
        nautmiles[index] = NautMile(x,y) #place new nautical mile to be referenced at index

lines = []
with open('weights.txt') as f: #read in weights from text file
    lines = f.readlines()

y = height #markers for which y being looked at
for line in lines: #for every line from the txt file
    #adjust x and y
    y-=1
    x = 0
    line = line[:-1] #remove new line markers (side effect of reading file)
    for weight in line: #for every number in the line
        nautmiles[((height - 1 - y) * width)+x].cost = int(weight) #replace the weight of the naught mile
        x+=1 #increment x value

def getConnected(node): #method to get the vaild connecting nodes to a node
    neighbours = []
    #check x+1
    if (node.x < width - 1):
        index = ((height - 1 - node.y) * width) + node.x+1 #calc index
        if (node.g < 5): #if the mile is judged to be passable
            neighbours.append(nautmiles[index]) #add mile
    #check x-1
    if (node.x > 0):
        index = ((height - 1 - node.y) * width) + node.x-1 #calc index
        if (node.g < 5): #if the mile is judged to be passable
            neighbours.append(nautmiles[index]) #add mile
    #check y+1
    if (node.y < height - 1):
        index = ((height - 1 - node.y+1) * width) + node.x #calc index
        if (node.g < 5): #if the mile is judged to be passable
            neighbours.append(nautmiles[index]) #add mile
    #check y-1
    if (node.y > 0):
        index = ((height - 1 - node.y-1) * width) + node.x #calc index
        if (node.g < 5): #if the mile is judged to be passable
            neighbours.append(nautmiles[index]) #add mile
    return neighbours

def GetBest(openList): #iterate through the openList and find the node with the best f
    best = openList[0]
    bestF = best.g + best.h
    for node in openList:
        iF = node.g + node.h
        if (iF < bestF):
            best, bestF = node, iF
    return best

def Heuristic(node, goal): #method to calculate heuristic
    return abs(node.x - goal.x) + abs(node.y - goal.y)

def AStar():
    #set start and end nodes
    index = ((height - 1 - 1) * width) + 1
    start = nautmiles[index]
    index = ((height - 1 - 5) * width) + 8
    goal = nautmiles[index]
    
    start.h = Heuristic(start,goal) #calc h for start
    start.f = start.h #start has no cost so f is just h

    openList = []
    start.open = True #add to open list
    openList.append(start)
    closedList = [] #make list for closed nodes
    path = [] #make list for the final path

    while(len(openList) > 0): #loop until all nodes have been explored
        P = GetBest(openList) #find the node with the best f value
        if P == goal: #if the node is the goal quit
            print("found")
            break
        
        #close current node P
        openList.remove(P) 
        closedList.append(P)
        P.closed = True

        neighbours = getConnected(P) #get neighbours of P
        for n in neighbours: #fpr every neighbour
            if n.closed: #if its been closed no need to search it
                continue
            
            tempG = P.g + n.cost #calc cost of going to that node
            if n.open: #if the node is already listed to be searched
                if tempG > n.g: #and the new g is better
                    n.g = tempG #assign new g
                continue #skip the rest
            
            openList.append(n) #add neighbour to open list
            n.g = tempG #update g
            n.h = Heuristic(n, goal) #update h
            n.f = n.g + n.h #calc new cost
            n.bestParent = P #set parent node

    
    R = goal #start at the goal
    while (R.bestParent!=0): #unravel back through parents to find the path
        path.append(R)
        R = R.bestParent
    
    for i in path: #print path
        print(i.x, i.y)

AStar()