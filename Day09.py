from MabbusLib import getFileContent
from MabbusLib import RoundList


def part1():
    #   Read file
    fileNumbers = getFileContent("Day 9 Input.txt", True, False, " ")
    playGame(1, fileNumbers[0], fileNumbers[1])


def playGame(part, playerCount, maxPoints):
    #   Set starting conditions
    points = 0
    currentMarble = RoundList(0)
    scores = []
    currentPlayer = 0
    for i in range(playerCount):
        scores.append(0)
    #   Loop until all marbles is placed
    while points < maxPoints:
        #   Next marble and player
        if points % 10000 == 0:
            print("{}/{}".format(int(points/10000), int(maxPoints/10000)))
        points += 1
        currentPlayer += 1
        #   Loop to player 0 if needed
        while currentPlayer >= playerCount:
            currentPlayer -= playerCount
        #   Every 23d marble is special
        if points % 23 == 0:
            #   Add points and remove marble
            scores[currentPlayer] += points
            for i in range(7):
                currentMarble = currentMarble.prev
            scores[currentPlayer] += currentMarble.obj
            currentMarble.delete()
            currentMarble = currentMarble.nxt
        else:
            #   Go two steps right and insert marble
            currentMarble = currentMarble.nxt
            currentMarble.add(points)
            currentMarble = currentMarble.nxt
    winningScore = 0
    for s in scores:
        if s > winningScore:
            winningScore = s
    print("Part {}: {}".format(part, winningScore))


def part2():
    #   Read file
    fileNumbers = getFileContent("Day 9 Input.txt", True, False, " ")
    playGame(2, fileNumbers[0], fileNumbers[1]*100)


part2()
