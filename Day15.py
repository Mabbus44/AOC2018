from MabbusLib import getFileContent


#   Global constants
ELF = 1
GOBLIN = 2
LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4


#   Class path contains a path and tools for extending the path
class Path:
    def __init__(self, x, y):
        self.path = [[x, y]]

    def unique(self, x, y, pathLen=-1):
        #   Checks if x,y is not in the path
        if pathLen == -1:
            pathLen = len(self.path)
        for p in range(pathLen):
            if self.path[p][0] == x and self.path[p][1] == y:
                return False
        return True

    def copy(self):
        ret = Path(0, 0)
        ret.path = []
        for p in self.path:
            ret.path.append([p[0], p[1]])
        return ret

    def nextSteps(self, pMap, pPaths):
        #   Returns a list of all the possible paths one step forward from current path
        ret = []
        x = 0
        y = 0
        for i in range(4):
            if i == 0:
                x = self.path[len(self.path)-1][0] - 1
                y = self.path[len(self.path)-1][1]
            if i == 1:
                x = self.path[len(self.path)-1][0] + 1
                y = self.path[len(self.path)-1][1]
            if i == 2:
                x = self.path[len(self.path)-1][0]
                y = self.path[len(self.path)-1][1] - 1
            if i == 3:
                x = self.path[len(self.path)-1][0]
                y = self.path[len(self.path)-1][1] + 1
            if self.unique(x, y) and not pMap.outOfBounds(x, y) and pMap.map[x][y].icon == ".":
                unique = True
                #   Check if any other path arrived faster
                for p in pPaths:
                    if p != self and not p.unique(x, y, len(self.path)):
                        unique = False
                        break
                if unique:
                    newPath = self.copy()
                    newPath.path.append([x, y])
                    ret.append(newPath)
        return ret


#   Class map contains one empty map, one populated map and a list of units
class Map:
    def __init__(self, pElfDamage=3, pGoblinDamage=3):
        self.map = []
        self.units = []
        self.wallInst = Wall()
        self.floorInst = Floor()
        self.finished = False
        self.rounds = 0
        self.elfDamage = pElfDamage
        self.goblinDamage = pGoblinDamage

    def loadMap(self, fileInput):
        #   Loads map from file input (only supports maps where all columns are the same with)
        self.map = []
        self.units = []
        self.rounds = 0
        self.finished = False
        for x in range(len(fileInput[0])):
            self.map.append([])
            for y in range(len(fileInput)):
                if fileInput[y][x] == "#":
                    self.map[x].append(self.wallInst)
                else:
                    self.map[x].append(self.floorInst)
                if fileInput[y][x] == "G":
                    self.units.append(Unit(x, y, GOBLIN, self, self.goblinDamage))
                    self.map[x][y] = self.units[len(self.units)-1]
                if fileInput[y][x] == "E":
                    self.units.append(Unit(x, y, ELF, self, self.elfDamage))
                    self.map[x][y] = self.units[len(self.units)-1]

    def print(self):
        #   Outputs the map in the terminal
        for y in range(len(self.map[0])):
            for x in range(len(self.map)):
                print(self.map[x][y].icon, end='')
            for u in self.units:
                if u.y == y:
                    print(" {}/200 hp".format(u.hp), end='')
            print("")

    def outOfBounds(self, x, y):
        #   Checks if coordinates is inside map
        if x < 0 or y < 0 or x >= len(self.map) or y >= len(self.map[0]):
            return True
        return False

    def action(self, debug=False):
        #   Sort and copy unit list
        changed = True
        while changed:
            changed = False
            for i1 in range(len(self.units)-1):
                for i2 in range(i1+1, len(self.units)):
                    if (self.units[i2].y < self.units[i1].y or
                            (self.units[i2].y == self.units[i1].y and self.units[i2].x < self.units[i1].x)):
                        swapUnits = self.units[i2]
                        self.units[i2] = self.units[i1]
                        self.units[i1] = swapUnits
                        changed = True
        tUnits = list(self.units)
        #   Each unit makes it action
        i = 0
        for u in tUnits:
            #   if i == 25:
            #   print("Arrived")
            i += 1
            if u.hp > 0:
                u.action()
            if debug:
                self.print()
                print(u.icon + " at ({}, {}) took action".format(u.x, u.y))
        #   Count rounds
        if not self.finished:
            self.rounds += 1


#   A unit that can move and attack
class Unit:
    def __init__(self, px, py, pType, pParent, pDamage=3, pHp=200):
        self.x = px
        self.y = py
        self.type = pType
        self.hp = pHp
        self.damage = pDamage
        self.icon = "."
        self.parent = pParent
        if self.type == ELF:
            self.icon = "E"
        elif self.type == GOBLIN:
            self.icon = "G"

    def moveToPoint(self, point):
        #   Moves towards point
        if point[0] < self.x:
            self.move(LEFT)
        elif point[0] > self.x:
            self.move(RIGHT)
        elif point[1] < self.y:
            self.move(UP)
        elif point[1] > self.y:
            self.move(DOWN)

    def move(self, direction):
        #   Moves the unit in the direction "direction"
        self.parent.map[self.x][self.y] = self.parent.floorInst
        newX = self.x
        newY = self.y
        if direction == LEFT:
            newX -= 1
        if direction == UP:
            newY -= 1
        if direction == RIGHT:
            newX += 1
        if direction == DOWN:
            newY += 1
        if self.parent.outOfBounds(newX, newY) or self.parent.map[newX][newY].icon == "#":
            self.parent.map[self.x][self.y] = self
            print("Error, cannot move there")
            return False
        self.x = newX
        self.y = newY
        self.parent.map[self.x][self.y] = self
        return True

    def findDestinations(self):
        #   Return a list of possible destinations
        destinations = []
        for u in self.parent.units:
            if u.type != self.type:
                if not self.parent.outOfBounds(u.x-1, u.y) and self.parent.map[u.x-1][u.y].icon == ".":
                    destinations.append([u.x-1, u.y])
                if not self.parent.outOfBounds(u.x+1, u.y) and self.parent.map[u.x+1][u.y].icon == ".":
                    destinations.append([u.x+1, u.y])
                if not self.parent.outOfBounds(u.x, u.y-1) and self.parent.map[u.x][u.y-1].icon == ".":
                    destinations.append([u.x, u.y-1])
                if not self.parent.outOfBounds(u.x, u.y+1) and self.parent.map[u.x][u.y+1].icon == ".":
                    destinations.append([u.x, u.y+1])
        return destinations

    def evaluateAndMove(self):
        #   Finds possible paths
        destinations = self.findDestinations()
        paths = []
        pathAndDests = []
        if len(destinations) == 0:
            return
        if not self.parent.outOfBounds(self.x + 1, self.y) and self.parent.map[self.x + 1][self.y].icon == ".":
            paths.append(Path(self.x + 1, self.y))
        if not self.parent.outOfBounds(self.x - 1, self.y) and self.parent.map[self.x - 1][self.y].icon == ".":
            paths.append(Path(self.x - 1, self.y))
        if not self.parent.outOfBounds(self.x, self.y + 1) and self.parent.map[self.x][self.y + 1].icon == ".":
            paths.append(Path(self.x, self.y + 1))
        if not self.parent.outOfBounds(self.x, self.y - 1) and self.parent.map[self.x][self.y - 1].icon == ".":
            paths.append(Path(self.x, self.y - 1))
        newPathsFound = False
        if len(paths) > 0:
            newPathsFound = True
        for p in paths:
            for d in destinations:
                lastP = p.path[len(p.path) - 1]
                if lastP[0] == d[0] and lastP[1] == d[1]:
                    pathAndDests.append([p, d])
        while newPathsFound and len(pathAndDests) == 0:
            newPathsFound = False
            newPaths = []
            for p in paths:
                tNewPaths = p.nextSteps(self.parent, paths)
                #   Check if another path with the same starting point arrived at the same time
                lastIndex = len(p.path)
                for i1 in range(len(tNewPaths) - 1, -1, -1):
                    for i2 in range(len(newPaths)):
                        if (newPaths[i2].path[lastIndex][0] == tNewPaths[i1].path[lastIndex][0]
                                and newPaths[i2].path[lastIndex][1] == tNewPaths[i1].path[lastIndex][1]
                                and newPaths[i2].path[0][0] == tNewPaths[i1].path[0][0]
                                and newPaths[i2].path[0][0] == tNewPaths[i1].path[0][0]):
                            del tNewPaths[i1]
                            break
                for t in tNewPaths:
                    newPaths.append(t)
                    newPathsFound = True
            paths = newPaths
            pathAndDests = []
            for p in paths:
                for d in destinations:
                    lastP = p.path[len(p.path) - 1]
                    if lastP[0] == d[0] and lastP[1] == d[1]:
                        pathAndDests.append([p, d])
        #   Find first dest in reading order
        if len(pathAndDests) > 0:
            pathAndDestsNew = [pathAndDests[0]]
        else:
            pathAndDestsNew = []
        for i in range(1, len(pathAndDests)):
            if pathAndDests[i][1][1] < pathAndDestsNew[0][1][1]:
                pathAndDestsNew = [pathAndDests[i]]
            elif (pathAndDests[i][1][1] == pathAndDestsNew[0][1][1] and
                  pathAndDests[i][1][0] < pathAndDestsNew[0][1][0]):
                pathAndDestsNew = [pathAndDests[i]]
            elif (pathAndDests[i][1][1] == pathAndDestsNew[0][1][1] and
                  pathAndDests[i][1][0] == pathAndDestsNew[0][1][0]):
                pathAndDestsNew.append(pathAndDests[i])
        pathAndDests = pathAndDestsNew
        #   Find first source in reading order
        if len(pathAndDests) > 0:
            pathAndDestsNew = pathAndDests[0]
        else:
            pathAndDestsNew = []
        for i in range(1, len(pathAndDests)):
            if pathAndDests[i][0].path[0][1] < pathAndDestsNew[0].path[0][1]:
                pathAndDestsNew = pathAndDests[i]
            elif (pathAndDests[i][0].path[0][1] == pathAndDestsNew[0].path[0][1] and
                  pathAndDests[i][0].path[0][0] < pathAndDestsNew[0].path[0][0]):
                pathAndDestsNew = pathAndDests[i]
        pathAndDests = pathAndDestsNew
        #   Move
        if len(pathAndDests) > 0:
            self.moveToPoint(pathAndDests[0].path[0])

    def action(self):
        #   Executes units next action
        #   Check if next to enemy
        enemy = "G"
        if self.icon == "G":
            enemy = "E"
        if (not((not self.parent.outOfBounds(self.x+1, self.y) and self.parent.map[self.x+1][self.y].icon == enemy)
                or (not self.parent.outOfBounds(self.x-1, self.y) and self.parent.map[self.x-1][self.y].icon == enemy)
                or (not self.parent.outOfBounds(self.x, self.y+1) and self.parent.map[self.x][self.y+1].icon == enemy)
                or (not self.parent.outOfBounds(self.x, self.y-1) and self.parent.map[self.x][self.y-1].icon == enemy))):
            self.evaluateAndMove()
        #   Check if opponents remain
        targets = []
        enemiesExist = False
        enemy = "G"
        if self.icon == "G":
            enemy = "E"
        for u in self.parent.units:
            if u.icon == enemy:
                enemiesExist = True
                break
        if not enemiesExist:
            self.parent.finished = True
        #   Attack
        if not self.parent.outOfBounds(self.x+1, self.y) and self.parent.map[self.x+1][self.y].icon == enemy:
            targets.append(self.parent.map[self.x+1][self.y])
        if not self.parent.outOfBounds(self.x-1, self.y) and self.parent.map[self.x-1][self.y].icon == enemy:
            targets.append(self.parent.map[self.x-1][self.y])
        if not self.parent.outOfBounds(self.x, self.y+1) and self.parent.map[self.x][self.y+1].icon == enemy:
            targets.append(self.parent.map[self.x][self.y+1])
        if not self.parent.outOfBounds(self.x, self.y-1) and self.parent.map[self.x][self.y-1].icon == enemy:
            targets.append(self.parent.map[self.x][self.y-1])
        #   Find enemy with lowest HP or first in reading order
        if len(targets) > 0:
            finalTarget = targets[0]
        else:
            finalTarget = 0
        for i in range(1, len(targets)):
            if targets[i].hp < finalTarget.hp:
                finalTarget = targets[i]
            elif targets[i].hp == finalTarget.hp and targets[i].y < finalTarget.y:
                finalTarget = targets[i]
            elif targets[i].hp == finalTarget.hp and targets[i].y == finalTarget.y and targets[i].x < finalTarget.x:
                finalTarget = targets[i]
        #   Attack
        if len(targets) > 0:
            finalTarget.hp -= self.damage
            if finalTarget.hp < 1:
                self.parent.units.remove(finalTarget)
                self.parent.map[finalTarget.x][finalTarget.y] = self.parent.floorInst


#   Represent an wall in the map
class Wall:
    icon = "#"


#   Represents an empty square in the map
class Floor:
    icon = "."


def part1():
    #   Get file input
    fileInput = getFileContent("Day 15 Input.txt", False, True, "\n")
    mapInst = Map()
    mapInst.loadMap(fileInput)
    mapInst.print()
    while not mapInst.finished:
        eSum = 0
        gSum = 0
        for u in mapInst.units:
            if u.icon == "E":
                eSum += u.hp
            if u.icon == "G":
                gSum += u.hp
        print("Turn: {}, Elves HP: {}, Goblins HP: {}".format(mapInst.rounds, eSum, gSum))
        mapInst.action(False)
    hpSum = 0
    for u in mapInst.units:
        hpSum += u.hp
    mapInst.print()
    print("Part 1: {} turns * {} hp = {}".format(mapInst.rounds, hpSum, mapInst.rounds*hpSum))


def part2():
    #   Get file input
    fileInput = getFileContent("Day 15 Input.txt", False, True, "\n")
    mapInst = Map()
    damage = 3
    maxDamage = 0
    minDamage = damage
    while minDamage+1 != maxDamage:
        #   Restart map
        print("Starting map damage min, now, max {} {} {}".format(minDamage, damage, maxDamage))
        mapInst.elfDamage = damage
        mapInst.loadMap(fileInput)
        eCountStart = 0
        for u in mapInst.units:
            if u.icon == "E":
                eCountStart += 1
        eCount = eCountStart
        while not mapInst.finished and eCountStart == eCount:
            #   Run map
            mapInst.action(False)
            eCount = 0
            eSum = 0
            gSum = 0
            for u in mapInst.units:
                if u.icon == "E":
                    eSum += u.hp
                    eCount += 1
                if u.icon == "G":
                    gSum += u.hp
            print("Turn: {}, Elves HP: {}({}), Goblins HP: {}".format(mapInst.rounds, eSum, eCount, gSum))
        if eCountStart != eCount:
            #   If elf died, damage was to low
            minDamage = damage
            if maxDamage == 0:
                damage *= 2
            else:
                damage = int((maxDamage + minDamage)/2)
        else:
            #   If no elf died, damage might be to high
            maxDamage = damage
            damage = int((maxDamage + minDamage) / 2)
    print("Minimum required damage for no elf to die is {}".format(maxDamage))
    hpSum = 0
    for u in mapInst.units:
        hpSum += u.hp
    print("Part 2: {} turns * {} hp = {}".format(mapInst.rounds, hpSum, mapInst.rounds*hpSum))


part2()
