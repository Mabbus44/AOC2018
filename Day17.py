from MabbusLib import getFileContent

SAND = 1
CLAY = 2
FLOWING_WATER = 3
STILL_WATER = 4


class Board:
    def __init__(self):
        self.grid = []
        self.xMin = 99999999
        self.xMax = 0
        self.yMin = 99999999
        self.yMax = 0
        self.width = 0
        self.height = 0
        self.newWater = []

    def flow(self):
        #   Let water flow one tick
        addedWater = []
        for w in self.newWater:
            if w[1] == len(self.grid[0]) - 1:
                #   Water reached bottom of grid
                None
            elif self.grid[w[0]][w[1]+1] == SAND:
                #   Flow downwards
                addedWater.append([w[0], w[1]+1])
                self.grid[w[0]][w[1]+1] = FLOWING_WATER
            elif self.grid[w[0]][w[1]+1] == CLAY or self.grid[w[0]][w[1]+1] == STILL_WATER:
                #   If still surface below
                if self.grid[w[0]-1][w[1]] != SAND and self.grid[w[0]-1][w[1]] != SAND:
                    #   If walled in with floor, transform FLOWING_WATER to STILL_WATER
                    transform = True
                    xMin = w[0]
                    xMax = w[0]
                    while transform and self.grid[xMin][w[1]] != CLAY:
                        xMin -= 1
                        if self.grid[xMin][w[1]+1] != CLAY and self.grid[xMin][w[1]+1] != STILL_WATER:
                            transform = False
                    while transform and self.grid[xMax][w[1]] != CLAY:
                        xMax += 1
                        if self.grid[xMax][w[1]+1] != CLAY and self.grid[xMax][w[1]+1] != STILL_WATER:
                            transform = False
                    if transform:
                        for x in range(xMin+1, xMax):
                            self.grid[x][w[1]] = STILL_WATER
                            if self.grid[x][w[1]-1] == FLOWING_WATER:
                                #   If one layer became STILL_WATER, start to spread layer above
                                addedWater.append([x, w[1]-1])
                #   Flow sideways
                if self.grid[w[0]-1][w[1]] == SAND:
                    addedWater.append([w[0]-1, w[1]])
                    self.grid[w[0]-1][w[1]] = FLOWING_WATER
                if self.grid[w[0]+1][w[1]] == SAND:
                    addedWater.append([w[0]+1, w[1]])
                    self.grid[w[0]+1][w[1]] = FLOWING_WATER
        self.newWater = addedWater

    def setGrid(self, fileInput):
        #   Set min/max
        for row in fileInput:
            if row[0] == 'x':
                if int(row[1]) < self.xMin:
                    self.xMin = int(row[1])
                if int(row[1]) > self.xMax:
                    self.xMax = int(row[1])
                if int(row[3]) < self.yMin:
                    self.yMin = int(row[3])
                if int(row[4]) > self.yMax:
                    self.yMax = int(row[4])
            if row[0] == 'y':
                if int(row[1]) < self.yMin:
                    self.yMin = int(row[1])
                if int(row[1]) > self.yMax:
                    self.yMax = int(row[1])
                if int(row[3]) < self.xMin:
                    self.xMin = int(row[3])
                if int(row[4]) > self.xMax:
                    self.xMax = int(row[4])
        self.xMin -= 1
        self.xMax += 1
        #   Set sand
        self.width = self.xMax - self.xMin + 1
        self.height = self.yMax - self.yMin + 1
        self.grid = [[SAND] * self.height for n in range(self.width)]
        #   Set clay
        for row in fileInput:
            if row[0] == 'x':
                x = int(row[1])
                for y in range(int(row[3]), int(row[4]) + 1):
                    self.grid[x - self.xMin][y - self.yMin] = CLAY
            if row[0] == 'y':
                y = int(row[1])
                for x in range(int(row[3]), int(row[4]) + 1):
                    self.grid[x - self.xMin][y - self.yMin] = CLAY
        #   Set water
        self.grid[500-self.xMin][0] = FLOWING_WATER
        self.newWater.append([500-self.xMin, 0])

    def print(self):
        #   Print board
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[x][y] == SAND:
                    print(".", end='')
                if self.grid[x][y] == CLAY:
                    print("#", end='')
                if self.grid[x][y] == FLOWING_WATER:
                    print("|", end='')
                if self.grid[x][y] == STILL_WATER:
                    print("~", end='')
            print("")

    def waterCount(self, onlyStill=False):
        #   Counts water in grid
        c = 0
        for col in self.grid:
            for symbol in col:
                if symbol == STILL_WATER:
                    c += 1
                if not onlyStill and symbol == FLOWING_WATER:
                    c += 1
        return c


def part1():
    #   Read file
    fileInput = getFileContent("Day 17 Input.txt", False, False, "\n", ["=", ",", "..", " "])
    board = Board()
    board.setGrid(fileInput)
    while len(board.newWater) > 0:
        board.flow()
    print("Part 1: Water count is {}".format(board.waterCount()))


def part2():
    #   Read file
    fileInput = getFileContent("Day 17 Input.txt", False, False, "\n", ["=", ",", "..", " "])
    board = Board()
    board.setGrid(fileInput)
    while len(board.newWater) > 0:
        board.flow()
    print("Part 2: Water count is {}".format(board.waterCount(True)))


part2()
