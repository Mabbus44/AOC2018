from MabbusLib import getFileContent


def trim(state):
    #   pad to minimum four '0' in the begining
    prefix = 4
    for i in range(4):
        if state[i]:
            break
        prefix -= 1
    postfix = 4
    #   pad to minimum four '0' in the end
    for i in range(4):
        if state[len(state)-1-i]:
            break
        postfix -= 1
    #   do the actual padding
    for i in range(prefix):
        state.insert(0, 0)
    for i in range(postfix):
        state.append(0)
    #   remove until fifth state is a '1'
    while not state[4]:
        del state[4]
        prefix -= 1
    #   remove until fifth last state is a '1'
    while not state[len(state) - 5]:
        del state[len(state) - 5]
    #   return the number of '0' added in the begining of state
    return prefix


def part1():
    #   Read file
    fileInput = getFileContent("Day 12 Input.txt", False, False, "\n", [" ", "=", ">"])
    #   Translate state
    state = []
    zeroIndex = 0
    for i in range(len(fileInput[0][2])):
        if fileInput[0][2][i] == "#":
            state.append(1)
        else:
            state.append(0)
    #   Translate rules
    rules = []
    for i0 in range(2):
        rules.append([])
        for i1 in range(2):
            rules[i0].append([])
            for i2 in range(2):
                rules[i0][i1].append([])
                for i3 in range(2):
                    rules[i0][i1][i2].append([])
                    for i4 in range(2):
                        rules[i0][i1][i2][i3].append(0)
    del fileInput[0]
    for l in fileInput:
        cond = [0, 0, 0, 0, 0]
        for i in range(5):
            if l[0][i] == "#":
                cond[i] = 1
        if l[1] == "#":
            res = 1
        else:
            res = 0
        rules[cond[0]][cond[1]][cond[2]][cond[3]][cond[4]] = res
    #   Apply rules
    for i in range(20):
        zeroIndex += trim(state)
        newState = [False] * len(state)
        for i in range(len(newState)-4):
            newState[i+2] = rules[state[i]][state[i+1]][state[i+2]][state[i+3]][state[i+4]]
        state = newState
    #   Count points
    points = 0
    potIndex = 0 - zeroIndex
    for s in state:
        if s:
            points += potIndex
        potIndex += 1
    print("Part 1: {}".format(points))


def part2():
    #   Read file
    fileInput = getFileContent("Day 12 Input.txt", False, False, "\n", [" ", "=", ">"])
    #   Translate state
    state = []
    zeroIndex = 0
    for i in range(len(fileInput[0][2])):
        if fileInput[0][2][i] == "#":
            state.append(1)
        else:
            state.append(0)
    #   Translate rules
    rules = []
    for i0 in range(2):
        rules.append([])
        for i1 in range(2):
            rules[i0].append([])
            for i2 in range(2):
                rules[i0][i1].append([])
                for i3 in range(2):
                    rules[i0][i1][i2].append([])
                    for i4 in range(2):
                        rules[i0][i1][i2][i3].append(0)
    del fileInput[0]
    for l in fileInput:
        cond = [0, 0, 0, 0, 0]
        for i in range(5):
            if l[0][i] == "#":
                cond[i] = 1
        if l[1] == "#":
            res = 1
        else:
            res = 0
        rules[cond[0]][cond[1]][cond[2]][cond[3]][cond[4]] = res
    #   Apply rules (it seems that after a while the state is unchanged and only the zeroIndex changes)
    for roundNum in range(5000):
        zeroIndex += trim(state)
        newState = [0] * len(state)
        for i in range(len(newState)-4):
            newState[i+2] = rules[state[i]][state[i+1]][state[i+2]][state[i+3]][state[i+4]]
        state = newState
    #   Count points
    points = 0
    zeroIndex = zeroIndex - (50000000000-5000)  # Simulates the last 49 999 995 000 rounds
    potIndex = 0 - zeroIndex
    for s in state:
        if s:
            points += potIndex
        potIndex += 1
    print("Part 2: {}".format(points))


part2()
