class Cell:
    def __init__(self, r, p):
        self.rack = r
        self.power = p


def part1():
    serialNumber = 7347
    grid = []
    for y in range(300):
        grid.append([])
        for x in range(300):
            rack = x + 11
            power = ((y + 1) * rack + serialNumber) * rack
            power = int((power - int(power / 1000) * 1000) / 100) - 5
            grid[y].append(Cell(rack, power))
    bSum = 0
    bx = 0
    by = 0
    for y in range(298):
        for x in range(298):
            powerSum = 0
            for sy in range(3):
                for sx in range(3):
                    powerSum += grid[y + sy][x + sx].power
            if powerSum > bSum:
                bSum = powerSum
                bx = x + 1
                by = y + 1
    print("bSum: {} ({}, {})".format(bSum, bx, by))


def part2():
    #   Starting conditions
    serialNumber = 7347
    grid = Node(1, 1, 300, 300)
    #   Divide the grid into smaller pieces
    print("Dividing the grid")
    grid.populate()
    #   Insert all values into grid
    print("Inserting values into the grid")
    for y in range(300):
        for x in range(300):
            rack = x + 11
            power = ((y + 1) * rack + serialNumber) * rack
            power = int((power - int(power / 1000) * 1000) / 100) - 5
            grid.insertValue(power, x+1, y+1)
    #   Calculate values for all sub grids
    print("Calculate values for all sub grids")
    grid.setValues()
    #   Look for the square with the most power
    print("Looking for the square with the most power")
    bSum = 0
    bx = 0
    by = 0
    bSize = 0
    for y in range(300):
        for x in range(300):
            print("Progress ({}, {})".format(x, y))
            for size in range(300 - max(x, y)):
                powerSum = grid.getSum(x+1, y+1, size+1)
                if powerSum > bSum:
                    bSum = powerSum
                    bx = x + 1
                    by = y + 1
                    bSize = size + 1
    print("bSum: {} ({}, {}, {})".format(bSum, bx, by, bSize))


#   Node with size and position, contains smaller child nodes, smallest node is 1x1
class Node:
    def __init__(self, px=1, py=1, pSizeX=1, pSizeY=1):
        self.x = px
        self.y = py
        self.sizeX = pSizeX
        self.sizeY = pSizeY
        self.val = 0
        self.children = []

    #   Divides nodes area in four child nodes and calls "populate" for them
    def populate(self):
        if self.sizeY == 1 and self.sizeX == 1:
            return
        if self.sizeY == 1:
            self.children.append(Node(self.x, self.y, int(self.sizeX / 2), self.sizeY))
            self.children.append(Node(self.x + int(self.sizeX / 2), self.y,
                                      self.sizeX - int(self.sizeX / 2), self.sizeY))
        elif self.sizeX == 1:
            self.children.append(Node(self.x, self.y, self.sizeX, int(self.sizeY / 2)))
            self.children.append(Node(self.x, self.y + int(self.sizeY / 2),
                                      self.sizeX, self.sizeY - int(self.sizeY / 2)))
        else:
            self.children.append(Node(self.x, self.y, int(self.sizeX / 2), int(self.sizeY / 2)))
            self.children.append(Node(self.x + int(self.sizeX / 2), self.y,
                                      self.sizeX - int(self.sizeX / 2), int(self.sizeY / 2)))
            self.children.append(Node(self.x, self.y + int(self.sizeY / 2),
                                      int(self.sizeX / 2), self.sizeY - int(self.sizeY / 2)))
            self.children.append(Node(self.x + int(self.sizeX / 2), self.y + int(self.sizeY / 2),
                                      self.sizeX - int(self.sizeX / 2), self.sizeY - int(self.sizeY / 2)))
        for c in self.children:
            c.populate()

    #   Find where value belongs and puts it there
    def insertValue(self, pv, px, py):
        if self.sizeX == 1 and self.sizeY == 1:
            self.val = pv
            return
        for c in self.children:
            if c.x <= px < c.x + c.sizeX and c.y <= py < c.y + c.sizeY:
                c.insertValue(pv, px, py)

    #   Sets value of all nodes with children to the sum of the child values (and returns the value)
    def setValues(self):
        if len(self.children) > 0:
            self.val = 0
            for c in self.children:
                self.val += c.setValues()
        return self.val

    #   Gets sum of values inside square
    def getSum(self, px, py, pSize):
        if self.x >= px and self.y >= py and self.x + self.sizeX <= px + pSize and self.y + self.sizeY <= py + pSize:
            return self.val
        else:
            retVal = 0
            for c in self.children:
                if not(c.x >= px + pSize or c.x + c.sizeX <= px or c.y >= py + pSize or c.y + c.sizeY <= py):
                    retVal += c.getSum(px, py, pSize)
            return retVal

    #   Prints object content and children
    def print(self):
        print("({}, {})-({}, {}) {}".format(self.x, self.y, self.sizeX, self.sizeY, self.val))
        for c in self.children:
            c.print()


part2()
