from MabbusLib import getFileContent

#   Constants
LEFT = 1
UP = 2
RIGHT = 3
DOWN = 4
FORWARD = 5


def sortCarts(carts):
    #   Sort cars from top to bottom, left to right
    changed = True
    while changed:
        changed = False
        for n1 in range(len(carts)-1):
            for n2 in range(n1+1, len(carts)):
                if carts[n2].y < carts[n1].y or (carts[n2].y == carts[n1].y and carts[n2].x < carts[n1].x):
                    tCart = carts[n2]
                    carts[n2] = carts[n1]
                    carts[n1] = tCart
                    changed = True


class Cart:
    #   Cart class
    def __init__(self, px=0, py=0, pDir=0):
        self.x = px
        self.y = py
        self.dir = pDir
        self.lastTurn = RIGHT
        self.dead = False


def printRail(pRail, carts, compress=False):
    #   Output the rail for debug purposes
    rail = []
    lineIndex = 0
    for line in pRail:
        if not compress:
            rail.append(list(line))
        if compress and lineIndex % 4 == 0:
            rail.append([' ']*len(line))
        lineIndex += 1
    for c in carts:
        if compress:
            if c.dir == LEFT:
                rail[int(c.y/4)][c.x] = '<'
            if c.dir == UP:
                rail[int(c.y/4)][c.x] = '^'
            if c.dir == RIGHT:
                rail[int(c.y/4)][c.x] = '>'
            if c.dir == DOWN:
                rail[int(c.y/4)][c.x] = 'v'
        else:
            if c.dir == LEFT:
                rail[c.y][c.x] = '<'
            if c.dir == UP:
                rail[c.y][c.x] = '^'
            if c.dir == RIGHT:
                rail[c.y][c.x] = '>'
            if c.dir == DOWN:
                rail[c.y][c.x] = 'v'
    for y in range(len(rail)):
        for x in range(len(rail[y])):
            print(rail[y][x], end='')
        print("")
    for x in range(len(rail[0])):
        print('-', end='')
    print("")


def part1():
    #   Get file input
    fileInput = getFileContent("Day 13 Input.txt", False, True, "\n")
    rails = fileInput
    #   Create carts
    carts = []
    for y in range(len(rails)):
        for x in range(len(rails[y])):
            if rails[y][x] == '<':
                carts.append(Cart(x, y, LEFT))
                rails[y][x] = '-'
            if rails[y][x] == '>':
                carts.append(Cart(x, y, RIGHT))
                rails[y][x] = '-'
            if rails[y][x] == '^':
                carts.append(Cart(x, y, UP))
                rails[y][x] = '|'
            if rails[y][x] == 'v':
                carts.append(Cart(x, y, DOWN))
                rails[y][x] = '|'
    #   Move carts
    crash = False
    crashX = 0
    crashY = 0
    cycles = 0
    while not crash:
        sortCarts(carts)
        for c in carts:
            if rails[c.y][c.x] == '/':
                if c.dir == LEFT:
                    c.dir = DOWN
                elif c.dir == RIGHT:
                    c.dir = UP
                elif c.dir == UP:
                    c.dir = RIGHT
                elif c.dir == DOWN:
                    c.dir = LEFT
            if rails[c.y][c.x] == '\\':
                if c.dir == LEFT:
                    c.dir = UP
                elif c.dir == RIGHT:
                    c.dir = DOWN
                elif c.dir == UP:
                    c.dir = LEFT
                elif c.dir == DOWN:
                    c.dir = RIGHT
            if rails[c.y][c.x] == '+':
                if c.lastTurn == LEFT:
                    c.lastTurn = FORWARD
                elif c.lastTurn == FORWARD:
                    c.lastTurn = RIGHT
                    c.dir += 1
                    if c.dir == 5:
                        c.dir = 1
                elif c.lastTurn == RIGHT:
                    c.lastTurn = LEFT
                    c.dir -= 1
                    if c.dir == 0:
                        c.dir = 4
            if c.dir == LEFT:
                c.x -= 1
            if c.dir == RIGHT:
                c.x += 1
            if c.dir == UP:
                c.y -= 1
            if c.dir == DOWN:
                c.y += 1
            #   Test for collision
            cIndex = 0
            for c1 in range(len(carts)-1):
                cIndex2 = c1+1
                for c2 in range(c1+1, len(carts)):
                    if carts[c1].x == carts[c2].x and carts[c1].y == carts[c2].y:
                        crash = True
                        crashX = carts[c1].x
                        crashY = carts[c1].y
                    cIndex2 += 1
                cIndex += 1
        cycles += 1
    print("Part 1: Crash at ({}, {}) after {} cycles".format(crashX, crashY, cycles))


def part2():
    #   Get file input
    fileInput = getFileContent("Day 13 Input.txt", False, True, "\n")
    rails = fileInput
    #   Create carts
    carts = []
    for y in range(len(rails)):
        for x in range(len(rails[y])):
            if rails[y][x] == '<':
                carts.append(Cart(x, y, LEFT))
                rails[y][x] = '-'
            if rails[y][x] == '>':
                carts.append(Cart(x, y, RIGHT))
                rails[y][x] = '-'
            if rails[y][x] == '^':
                carts.append(Cart(x, y, UP))
                rails[y][x] = '|'
            if rails[y][x] == 'v':
                carts.append(Cart(x, y, DOWN))
                rails[y][x] = '|'
    #   Move carts
    cycles = 0
    while len(carts) > 1:
        sortCarts(carts)
        for c in carts:
            if rails[c.y][c.x] == '/':
                if c.dir == LEFT:
                    c.dir = DOWN
                elif c.dir == RIGHT:
                    c.dir = UP
                elif c.dir == UP:
                    c.dir = RIGHT
                elif c.dir == DOWN:
                    c.dir = LEFT
            if rails[c.y][c.x] == '\\':
                if c.dir == LEFT:
                    c.dir = UP
                elif c.dir == RIGHT:
                    c.dir = DOWN
                elif c.dir == UP:
                    c.dir = LEFT
                elif c.dir == DOWN:
                    c.dir = RIGHT
            if rails[c.y][c.x] == '+':
                if c.lastTurn == LEFT:
                    c.lastTurn = FORWARD
                elif c.lastTurn == FORWARD:
                    c.lastTurn = RIGHT
                    c.dir += 1
                    if c.dir == 5:
                        c.dir = 1
                elif c.lastTurn == RIGHT:
                    c.lastTurn = LEFT
                    c.dir -= 1
                    if c.dir == 0:
                        c.dir = 4
            if not c.dead and c.dir == LEFT:
                c.x -= 1
            if not c.dead and  c.dir == RIGHT:
                c.x += 1
            if not c.dead and  c.dir == UP:
                c.y -= 1
            if not c.dead and  c.dir == DOWN:
                c.y += 1
            #   Test for collision
            cIndex = 0
            for c1 in range(len(carts)-1):
                cIndex2 = c1+1
                for c2 in range(c1+1, len(carts)):
                    if carts[c1].x == carts[c2].x and carts[c1].y == carts[c2].y:
                        carts[c1].dead = True
                        carts[c2].dead = True
                    cIndex2 += 1
                cIndex += 1
        for c in range(len(carts)-1, -1, -1):
            if carts[c].dead:
                print("Cart died at step {} ".format(cycles))
                del(carts[c])
        cycles += 1
    print("Part 2: Last cart at ({}, {}) after {} cycles".format(carts[0].x, carts[0].y, cycles))


part2()
