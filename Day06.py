from MabbusLib import getFileContent
import time


def mDist(p1, p2):
    #   Returns the manhattan distance between p1 an dp2
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])


def part1():
    #   Time with lists: 44,96 s
    start = time.time()
    points = getFileContent("Day 6 Input.txt", True, False, "\n", ",")
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    zoneSizes = []
    #   Go through all points
    for homeP in points:
        #   print("Testing point ({}, {})".format(homeP[0], homeP[1]))
        zone = [list(homeP)]
        i = 0
        dirNum = 0
        infiniteZone = False
        #   Expand area until all paths has ended
        while i < len(zone):
            #   Find new point
            newP = [zone[i][0]+directions[dirNum][0], zone[i][1]+directions[dirNum][1]]
            myMDist = mDist(newP, homeP)
            isMyP = True
            #   Check if point is already in zone
            for compP in zone:
                if newP[0] == compP[0] and newP[1] == compP[1]:
                    isMyP = False
                    break
            #   Compare coordinate with all other points to se who is closest, and check if outside field
            worst = [True, True, True, True]
            if isMyP:
                for compP in points:
                    if not(homeP[0] == compP[0] and homeP[1] == compP[1]):
                        if compP[0] > newP[0]:
                            worst[0] = False
                        if compP[0] < newP[0]:
                            worst[1] = False
                        if compP[1] > newP[1]:
                            worst[2] = False
                        if compP[1] < newP[1]:
                            worst[3] = False
                        if mDist(compP, newP) <= myMDist:
                            isMyP = False
                            break
            #   Add new point to zone
            if isMyP:
                zone.append(list(newP))
            #   Go to next new point
            dirNum += 1
            if dirNum > 3:
                i += 1
                dirNum = 0
            if isMyP and (worst[0] or worst[1] or worst[2] or worst[3]):
                infiniteZone = True
                break
        if infiniteZone:
            zoneSizes.append(0)
        else:
            zoneSizes.append(len(zone))
    print(zoneSizes)
    biggest = 0
    for z in zoneSizes:
        if z > biggest:
            biggest = z
    print("Biggest = {}".format(biggest))
    end = time.time()
    print(end-start)


def part2():
    #   Time with lists: 389,85 s
    start = time.time()
    points = getFileContent("Day 6 Input.txt", True, False, "\n", ",")
    bounds = [9999, 9999, 0, 0]
    directions = [[-1, 0], [0, -1], [1, 0], [0, 1]]
    myMDist = 10000
    #   Start at first point with total distance < myMDist
    for p in points:
        totalDist = 0
        for compP in points:
            totalDist += mDist(compP, p)
        if totalDist < myMDist:
            homeP = p
            break
    zone = [list(homeP)]
    i = 0
    dirNum = 0
    #   Expand area until to far away
    while i < len(zone):
        #   Find new point
        newP = [zone[i][0]+directions[dirNum][0], zone[i][1]+directions[dirNum][1]]
        isMyP = True
        #   Check if point is already in zone
        for compP in zone:
            if newP[0] == compP[0] and newP[1] == compP[1]:
                isMyP = False
                break
        #   Check distance to all other points
        worst = [True, True, True, True]
        totalDist = 0
        if isMyP:
            for compP in points:
                totalDist += mDist(compP, newP)
        #   Add new point to zone
        if isMyP and totalDist < myMDist:
            #if newP[0] < bounds[0]:
            #    bounds[0] = newP[0]
            #    print("Point x< ({}, {}) {}".format(newP[0], newP[1], totalDist))
            #if newP[0] > bounds[1]:
            #    bounds[1] = newP[0]
            #    print("Point x> ({}, {}) {}".format(newP[0], newP[1], totalDist))
            #if newP[1] < bounds[2]:
            #    bounds[2] = newP[1]
            #    print("Point y< ({}, {}) {}".format(newP[0], newP[1], totalDist))
            #if newP[1] > bounds[3]:
            #    bounds[3] = newP[1]
            #    print("Point y> ({}, {}) {}".format(newP[0], newP[1], totalDist))
            zone.append(list(newP))
        #   Go to next new point
        dirNum += 1
        if dirNum > 3:
            i += 1
            dirNum = 0
    print("Zone size = {}".format(len(zone)))
    end = time.time()
    print(end-start)


part1()