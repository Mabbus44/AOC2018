from MabbusLib import getFileContent


class Observation:
    def __init__(self):
        self.start = [0, 0, 0, 0]
        self.command = [0, 0, 0, 0]
        self.end = [0, 0, 0, 0]


class OpDecoder:
    def __int__(self):
        self.notUsed = 0
        self.reg = [0, 0, 0, 0]

    def run(self, pCode, pA, pB, pC):
        if pCode == 0:
            #   addr
            self.reg[pC] = self.reg[pA] + self.reg[pB]
        elif pCode == 1:
            #   addi
            self.reg[pC] = self.reg[pA] + pB
        elif pCode == 2:
            #   mulr
            self.reg[pC] = self.reg[pA] * self.reg[pB]
        elif pCode == 3:
            #   muli
            self.reg[pC] = self.reg[pA] * pB
        elif pCode == 4:
            #   banr
            self.reg[pC] = self.reg[pA] & self.reg[pB]
        elif pCode == 5:
            #   bani
            self.reg[pC] = self.reg[pA] & pB
        elif pCode == 6:
            #   borr
            self.reg[pC] = self.reg[pA] | self.reg[pB]
        elif pCode == 7:
            #   bori
            self.reg[pC] = self.reg[pA] | pB
        elif pCode == 8:
            #   setr
            self.reg[pC] = self.reg[pA]
        elif pCode == 9:
            #   seti
            self.reg[pC] = pA
        elif pCode == 10:
            #   gtir
            if pA > self.reg[pB]:
                self.reg[pC] = 1
            else:
                self.reg[pC] = 0
        elif pCode == 11:
            #   gtri
            if self.reg[pA] > pB:
                self.reg[pC] = 1
            else:
                self.reg[pC] = 0
        elif pCode == 12:
            #   gtrr
            if self.reg[pA] > self.reg[pB]:
                self.reg[pC] = 1
            else:
                self.reg[pC] = 0
        elif pCode == 13:
            #   eqir
            if pA == self.reg[pB]:
                self.reg[pC] = 1
            else:
                self.reg[pC] = 0
        elif pCode == 14:
            #   eqri
            if self.reg[pA] == pB:
                self.reg[pC] = 1
            else:
                self.reg[pC] = 0
        elif pCode == 15:
            #   eqrr
            if self.reg[pA] == self.reg[pB]:
                self.reg[pC] = 1
            else:
                self.reg[pC] = 0


def part1():
    fileInput = getFileContent("Day 16 Input.txt", False, False, "\n")
    done = False
    i = 0
    observations = []
    while not done:
        if fileInput[i][0] == 'B':
            o = Observation()
            rString = fileInput[i].replace(',', ' ').replace('[', ' ').replace(']', ' ').replace("Before:", ' ')
            o.start = list(map(int, list(filter(None, rString.split(" ")))))
            o.command = list(map(int, list(filter(None, fileInput[i + 1].split(" ")))))
            rString = fileInput[i + 2].replace(',', ' ').replace('[', ' ').replace(']', ' ').replace("After:", ' ')
            o.end = list(map(int, list(filter(None, rString.split(" ")))))
            observations.append(o)
            i += 2
        elif fileInput[i] != "":
            done = True
        i += 1
    decoder = OpDecoder()
    ans = 0
    for o in observations:
        fitRules = 0
        frl = [0] * 16
        for r in range(16):
            frl[r] = 0
            decoder.reg = list(o.start)
            decoder.run(r, o.command[1], o.command[2], o.command[3])
            if (decoder.reg[0] == o.end[0] and decoder.reg[1] == o.end[1]
                    and decoder.reg[2] == o.end[2] and decoder.reg[3] == o.end[3]):
                fitRules += 1
                frl[r] = 1
        if fitRules >= 3:
            ans += 1
    print("Part 1: {} observations fit 3 or more rules".format(ans))


def part2():
    fileInput = getFileContent("Day 16 Input.txt", False, False, "\n")
    part1done = False
    i = 0
    observations = []
    codeLines = []
    while i < len(fileInput):
        if fileInput[i][0] == 'B':
            o = Observation()
            rString = fileInput[i].replace(',', ' ').replace('[', ' ').replace(']', ' ').replace("Before:", ' ')
            o.start = list(map(int, list(filter(None, rString.split(" ")))))
            o.command = list(map(int, list(filter(None, fileInput[i + 1].split(" ")))))
            rString = fileInput[i + 2].replace(',', ' ').replace('[', ' ').replace(']', ' ').replace("After:", ' ')
            o.end = list(map(int, list(filter(None, rString.split(" ")))))
            observations.append(o)
            i += 2
        elif fileInput[i] != "":
            part1done = True
        if part1done:
            codeLines.append(list(map(int, fileInput[i].split(" "))))
        i += 1
    iTable = []
    tList = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
    for i in range(16):
        iTable.append(list(tList))
    decoder = OpDecoder()
    for o in observations:
        for r in range(16):
            decoder.reg = list(o.start)
            decoder.run(r, o.command[1], o.command[2], o.command[3])
            if (not (decoder.reg[0] == o.end[0] and decoder.reg[1] == o.end[1]
                     and decoder.reg[2] == o.end[2] and decoder.reg[3] == o.end[3])):
                if r in iTable[o.command[0]]:
                    iTable[o.command[0]].remove(r)
    changed = True
    while changed:
        changed = False
        for i in range(16):
            if len(iTable[i]) == 1:
                for i2 in range(16):
                    if i != i2 and iTable[i][0] in iTable[i2]:
                        changed = True
                        iTable[i2].remove(iTable[i][0])
    decoder.reg = [0, 0, 0, 0]
    for line in codeLines:
        decoder.run(iTable[line[0]][0], line[1], line[2], line[3])
    print("Part 2: [0] of register after run is {}".format(decoder.reg[0]))


part2()
