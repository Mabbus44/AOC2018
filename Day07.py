from MabbusLib import getFileContent


class Letter:
    def __init__(self, name):
        self.name = name
        self.active = False
        self.counted = False
        self.processing = False
        self.parents = []
        self.children = []


class Worker:
    def __init__(self):
        self.letter = Letter("|")
        self.time = 0


def part1():
    #   Read file
    letterInput = getFileContent("Day 7 Input.txt", False, False, "\n", " must be finished before step ")
    #   Get important letters
    for l in letterInput:
        l[0] = l[0][-1]
        l[1] = l[1][0:1]
    #   Create list of class objects
    letters = []
    for l1 in letterInput:
        isNew0 = True
        isNew1 = True
        for l2 in letters:
            if l1[0] == l2.name:
                isNew0 = False
            if l1[1] == l2.name:
                isNew1 = False
        if isNew0:
            letters.append(Letter(l1[0]))
        if isNew1:
            letters.append(Letter(l1[1]))
    #   Set parents and children
    for lInput in letterInput:
        for lObject in letters:
            if lInput[0] == lObject.name:
                for lObject2 in letters:
                    if lObject2.name == lInput[1]:
                        lObject.children.append(lObject2)
            if lInput[1] == lObject.name:
                for lObject2 in letters:
                    if lObject2.name == lInput[0]:
                        lObject.parents.append(lObject2)
    #   Find grand parents
    for lObject in letters:
        if len(lObject.parents) == 0:
            lObject.active = True
    #   Find order
    done = False
    ans = ""
    while not done:
        lowestLetter = Letter("|")  # Higher ASCII code then Z
        #   Find lowest active letter that is not counted
        for lObject in letters:
            if lObject.active and not lObject.counted and lObject.name < lowestLetter.name:
                lowestLetter = lObject
        if lowestLetter.name == "|":
            done = True
        else:
            #   Add letter
            ans = ans + lowestLetter.name
            lowestLetter.counted = True
            #   Activate all children that have all parents active
            for lObject in lowestLetter.children:
                active = True
                for lObject2 in lObject.parents:
                    if not lObject2.counted:
                        active = False
                if active:
                    lObject.active = True
    #   Print
    print("Part 1: {}".format(ans))


def part2():
    #   Read file
    letterInput = getFileContent("Day 7 Input.txt", False, False, "\n", " must be finished before step ")
    #   Get important letters
    for l in letterInput:
        l[0] = l[0][-1]
        l[1] = l[1][0:1]
    #   Create list of class objects
    letters = []
    for l1 in letterInput:
        isNew0 = True
        isNew1 = True
        for l2 in letters:
            if l1[0] == l2.name:
                isNew0 = False
            if l1[1] == l2.name:
                isNew1 = False
        if isNew0:
            letters.append(Letter(l1[0]))
        if isNew1:
            letters.append(Letter(l1[1]))
    #   Set parents and children
    for lInput in letterInput:
        for lObject in letters:
            if lInput[0] == lObject.name:
                for lObject2 in letters:
                    if lObject2.name == lInput[1]:
                        lObject.children.append(lObject2)
            if lInput[1] == lObject.name:
                for lObject2 in letters:
                    if lObject2.name == lInput[0]:
                        lObject.parents.append(lObject2)
    #   Find grand parents
    for lObject in letters:
        if len(lObject.parents) == 0:
            lObject.active = True
    #   Find order
    done = False
    ans = ""
    totalTime = 0
    workers = [Worker(), Worker(), Worker(), Worker(), Worker()]
    while not done:
        #   Check for new letters for the workers
        for w in workers:
            if w.time == 0:
                lowestLetter = Letter("|")  # Higher ASCII code then Z
                #   Find lowest active letter that is not counted and is not being processed
                for lObject in letters:
                    if (lObject.active and not lObject.counted and not lObject.processing
                            and lObject.name < lowestLetter.name):
                        lowestLetter = lObject
                if not lowestLetter.name == "|":
                    w.letter = lowestLetter
                    lowestLetter.processing = True
                    w.time = ord(w.letter.name) - 64 + 60
        for w in workers:
            #   Decrease time and save letters
            if w.time == 1:
                #   Add letter
                ans = ans + w.letter.name
                w.letter.processing = False
                w.letter.counted = True
                #   Activate all children that have all parents active
                for lObject in w.letter.children:
                    active = True
                    for lObject2 in lObject.parents:
                        if not lObject2.counted:
                            active = False
                    if active:
                        lObject.active = True
            if w.time > 0:
                w.time = w.time - 1
        done = True
        for lObject in letters:
            if not lObject.counted:
                done = False
                break
        totalTime = totalTime + 1
    #   Print
    print("Part 2: {} {}".format(ans, totalTime))


part2()