from MabbusLib import getFileContent


def findGeneralArea():
    #   Read file
    posNVel = getFileContent("Day 10 Input.txt", True, False, "\n", [" ", "<", ">", ","])
    minDX = 99999999
    minX = 0
    maxX = 0
    minDY = 99999999
    minY = 0
    maxY = 0
    minArea = 99999999
    minDXI = 0
    minDYI = 0
    minAreaI = 0
    for i in range(20000):
        minXT = 9999
        maxXT = -9999
        minYT = 9999
        maxYT = -9999
        for pv in posNVel:
            pv[0] += pv[2]
            pv[1] += pv[3]
            if pv[0] < minXT:
                minXT = pv[0]
            if pv[0] > maxXT:
                maxXT = pv[0]
            if pv[1] < minYT:
                minYT = pv[1]
            if pv[1] > maxYT:
                maxYT = pv[1]
        areaT = (maxXT-minXT)*(maxYT-minYT)
        if areaT < minArea:
            minArea = areaT
            minAreaI = i
            print("minDX {}: {} ({}-{})".format(minDXI, minDX, minX, maxX))
            print("minDY {}: {} ({}-{})".format(minDYI, minDY, minY, maxY))
            print("minArea {}: {}".format(minAreaI, minArea))
        if (maxXT-minXT) < minDX:
            minDX = (maxXT-minXT)
            minX = minXT
            maxX = maxXT
            minDXI = i
            print("minDX {}: {} ({}-{})".format(minDXI, minDX, minX, maxX))
            print("minDY {}: {} ({}-{})".format(minDYI, minDY, minY, maxY))
            print("minArea {}: {}".format(minAreaI, minArea))
        if (maxYT-minYT) < minDY:
            minDY = (maxYT-minYT)
            minY = minYT
            maxY = maxYT
            minDYI = i
            print("minDX {}: {} ({}-{})".format(minDXI, minDX, minX, maxX))
            print("minDY {}: {} ({}-{})".format(minDYI, minDY, minY, maxY))
            print("minArea {}: {}".format(minAreaI, minArea))


def printHMI(data, xMin, xMax, yMin, yMax):
    oneRow = ["."]
    for i in range(xMax-xMin):
        oneRow.append(".")
    rows = [list(oneRow)]
    for i in range(yMax-yMin):
        rows.append(list(oneRow))
    outSide = 0
    for d in data:
        x = d[0] - xMin
        y = d[1] - yMin
        if y < len(rows):
            if x < len(rows[y]):
                rows[y][x] = "#"
            else:
                outSide += 1
        else:
            outSide += 1
    for i in range(yMax - yMin):
        print("".join(rows[i]))
    print("Outside: {}".format(outSide))


def part1():
    #   Read file
    posNVel = getFileContent("Day 10 Input.txt", True, False, "\n", [" ", "<", ">", ","])
    for i in range(10121):
        for pv in posNVel:
            pv[0] += pv[2]
            pv[1] += pv[3]
    for i in range(5):
        for pv in posNVel:
            pv[0] += pv[2]
            pv[1] += pv[3]
        printHMI(posNVel, 100, 250, 100, 170)


part1()
