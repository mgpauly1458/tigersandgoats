import functions as fn

boardGraph = {
    'a1': ['a2', 'b1'],
    'a2': ['a1', 'b2', 'a3'],
    'a3': ['a2', 'b3', 'b4'],
    'b0': ['b1', 'c1', 'd1', 'e1'],
    'b1': ['b0', 'a1', 'b2', 'c1'],
    'b2': ['b1', 'c2', 'b3', 'a2'],
    'b3': ['b2', 'c3', 'b4', 'a3'],
    'b4': ['b3', 'c4'],
    'c1': ['b0', 'd1', 'c2', 'b1'],
    'c2': ['c1', 'd2', 'c3', 'b2'],
    'c3': ['c2', 'd3', 'c4', 'b3'],
    'c4': ['c3', 'd4', 'b4'],
    'd1': ['b0', 'e1', 'd2', 'c1'],
    'd2': ['d1', 'e2', 'd3', 'c2'],
    'd3': ['d2', 'e3', 'd4', 'c3'],
    'd4': ['d3', 'e4', 'c4'],
    'e1': ['b0', 'f1', 'e2', 'd1'],
    'e2': ['e1', 'f2', 'e3', 'd2'],
    'e3': ['e2', 'f3', 'e4', 'd3'],
    'e4': ['e3', 'd4'],
    'f1': ['e1', 'f2'],
    'f2': ['f1', 'f3', 'e2'],
    'f3': ['f2', 'e4', 'e3'],
}

positionRestraints = {
    'always_safe':['b0', 'a1', 'f1', 'e4', 'b4'],
    'UpDownRight':['a2', 'a3'],
    'UpDownLeft':['f2', 'f3'],
    'UpLeftRight':['c4', 'd4'],
}

def checkCol(pos, tigerPos, goatPos):
    tigersAndGoats = tigerPos + goatPos
    row = int(pos[1])
    up = pos[0] + str(row - 1)
    down = pos[0] + str(row + 1)
    print("checkCol: pos=", pos, "up=", up, "down=", down)
    if up in tigerPos and down not in tigersAndGoats:
        return False
    
    if down in tigerPos and up not in tigersAndGoats:
        return False
    
    return True

def checkRow(pos, tigerPos, goatPos):
    tigersAndGoats = tigerPos + goatPos
    col = ord(pos[0])
    right = chr(col+1) + pos[1]
    left = chr(col-1) + pos[1]
    print("checkRow: pos=", pos, "left=", left, "right=", right)
    if right in tigerPos and left not in tigersAndGoats:
        return False

    if left in tigerPos and right not in tigersAndGoats:
        return False

    return True

def checkUDR(pos, tigerPos, goatPos):
    return checkCol(pos, tigerPos, goatPos)

def checkUDL(pos, tigerPos, goatPos):
    return checkCol(pos, tigerPos, goatPos)


def checkULR(pos, tigerPos, goatPos):
    return checkRow(pos, tigerPos, goatPos)

def checkUDLR(pos, tigerPos, goatPos):
    return ( checkRow(pos, tigerPos, goatPos) and checkCol(pos, tigerPos, goatPos))

def blockedByTiger(tigerPos, goatPos):

    blocked = set({})
    adjTigerPos = set({})
    for x in tigerPos:
        for y in boardGraph[x]:
            if y not in tigerPos:
                adjTigerPos.add(y)

    print("adjTigerPos: ", adjTigerPos)
    for x in adjTigerPos:
        if x in positionRestraints['UpDownRight']:
            if not checkUDR(x, tigerPos, goatPos):
                blocked.add(x)
        elif x in positionRestraints['UpDownLeft']:
            if not checkUDL(x, tigerPos, goatPos):
                blocked.add(x)
        elif x in positionRestraints['UpLeftRight']:
            if not checkULR(x, tigerPos, goatPos):
                blocked.add(x)
        elif x not in positionRestraints['always_safe'] and not checkUDLR(x, tigerPos, goatPos):
            blocked.add(x)

    return blocked

# returns list of all 'safe' goat positions
# a goat is not in danger of being killed in this position
# only shows where a goat can be placed, does not account for what phase of the game its in
# (can be used in conjunction with other functions to implement phase 2 movement)
def potentialGoatPositions(boardPositions):
    emptyPos = fn.emptyPositions(boardPositions)
    tigerPos = fn.tigerPositions(boardPositions)
    goatPos = fn.goatPositions(boardPositions)
    invalidFutureGoatPosition = set({})
    
    # add current goat positions
    for x in goatPos:
        invalidFutureGoatPosition.add(x)

    # add blocked by tiger
    for x in blockedByTiger(tigerPos, goatPos):
        invalidFutureGoatPosition.add(x)


    potentialPositions = [x for x in emptyPos if (x not in invalidFutureGoatPosition)]
    print("potential goat positions: ", potentialPositions)
    return potentialPositions


# call with Board.boardPositions
def allGoatPositionsPhase1(boardPositions):
    emptyPos = fn.emptyPositions(boardPositions)
    tigerPos = fn.tigerPositions(boardPositions)
    goatPos = fn.goatPositions(boardPositions)

    temp = [x for x in emptyPos if x not in tigerPos]
    temp = [x for x in temp if x not in goatPos]
    return temp

def allGoatPositionsPhase2(boardPositions):
    positions = set({})
    goatPos = fn.goatPositions(boardPositions)
    emptyPos = fn.emptyPositions(boardPositions)
    for goat in goatPos:
        adjPos = boardGraph[goat]
        for x in adjPos:
            if x in emptyPos:
                positions.add(x)
    return positions

def allGoatPositions(boardPositions, goatCount):
    if goatCount >= 15:
        return allGoatPositionsPhase2(boardPositions)
    return allGoatPositionsPhase1(boardPositions)