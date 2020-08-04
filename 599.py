import math
import numpy as np

#projeuler 599: The well-known Rubik's Cube puzzle has many fascinating mathematical properties.
#The 2×2×2 variant has 8 cubelets with a total of 24 visible faces, each with a coloured sticker.
# Successively turning faces will rearrange the cubelets, although not all arrangements of cubelets are reachable
# without dismantling the puzzle.

#Suppose that we wish to apply new stickers to a 2×2×2 Rubik's cube in a non-standard colouring. Specifically, we have n

#different colours available (with an unlimited supply of stickers of each colour),
# and we place one sticker on each of the 24 faces in any arrangement that we please.
# We are not required to use all the colours, and if desired the same colour may appear in more than one face of a single cubelet.

#We say that two such colourings c1,c2
# are essentially distinct if a cube coloured according to c1
# cannot be made to match a cube coloured according to c2
# by performing mechanically possible Rubik's Cube moves.

# For example, with two colours available, there are 183 essentially distinct colourings.

# How many essentially distinct colourings are there with 10 different colours available?
#

#------------LIST OF FACES, LIST OF FUNCTIONS

pm = [-1,1]
dir = ["x","y","z"]

S = [] #list of faces: Ppp, pmP, pMp, etc. cardinality 24

for x in pm:
    for y in pm:
        for z in pm:
            #translate = {"x":x, "y":y, "z":z}
            for d in dir:
                S.append({"x":x, "y":y, "z":z, "d":d})

funclabels = [] #list of function labels: +x, -x, +y, -y, etc.
for sgn in pm:
    for d in dir:
        funclabels.append({"s":sgn, "d":d})

def labeltofunc(label):
    #returns a dictionary S -> S

    swaps = {"x":{"x":"x", "y":"z", "z":"y"}, "y":{"x":"z", "y":"y", "z":"x"}, "z":{"x":"y", "y":"x", "z":"z"}}
    forward = {"x":"y", "y":"z", "z":"x"}
    reverse = {"x":"z", "y":"x", "z":"y"}

    lsgn = label["s"]
    ld = label["d"]
    result = {}
    for x in pm:
        for y in pm:
            for z in pm:
                for d in dir:
                    face = {"x":x, "y":y, "z":z, "d":d}
                    if (face[ld] != lsgn):
                        result[face] = face
                    else: #face[ld] == lsgn
                        image = {}
                        if (face["d"] == ld):
                            image["d"] = ld
                        else:
                            image["d"] = swaps[ld][face["d"]]
                        image[ld] = face[ld] #= lsgn
                        image[reverse[ld]] = lsgn * face[forward[ld]]
                        image[forward[ld]] = -lsgn * face[reverse[ld]]
                        result[face] = image
    return result

def applyfunc(func, state):
    #state is a dictionary S->S
    #returns statenew: another dictionary S->S
    #func[state]
    statenew = {}
    funcdict = labeltofunc(func)

    for s in S:
        statenew[s] = funcdict[state[s]]
    return statenew

id = {}
for s in S:
    id[s] = s

#----------BFS to find all functions reachable by applying things in funclabels

queue = [id]
visited = [] #queue, visited must always be disjoint

while(queue):
    state = queue.pop(0)


    visited.append(state)

    for func in funclabels:
        statenew = applyfunc(func,state)
        if (statenew not in visited) and (statenew not in queue):
            queue.append(statenew)

print(visited) #sanity check

#-----------FINAL COMPUTATION: SUM OVER ALL STATES IN VISITED, INVOKE BURNSIDES LEMMA

size = len(visited)
NUMCOLORS = 10
fixptcount = 0 #counts total number of pairs (colorings, permutations) such that coloring is fixed by the permutation
for state in visited:
    componentcount = 0
    statevisited = []
    statequeue = []
    while(True):
        if not statequeue:
            allvisited = True
            unvisitedex = None
            for s in S:
                if s not in statevisited:
                    allvisited = False
                    unvisitedex = s
            if allvisited:
                break
            else:
                componentcount = componentcount + 1
                statequeue.append(unvisitedex)
        else:
            face = statequeue.pop(0)
            statevisited.append(face)
            facenew = state[face]
            if (facenew not in statevisited) and (facenew not in statequeue):
                queue.append(facenew)
    fixptcount = fixptcount + (NUMCOLORS ** componentcount)
distinctcolorings = fixptcount / size #ans: total number of equivalence classes of colorings





