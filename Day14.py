def checkLastScores(scores, pInput):
    for i in range(6):
        if scores[len(scores)-6+i] != pInput[i]:
            return False
    return True


def part1():
    scoreList = [3, 7]
    elf = [0, 1]
    puzzleInput = 503761
    while len(scoreList) < puzzleInput + 10:
        if scoreList[elf[0]] + scoreList[elf[1]] > 9:
            scoreList.append(1)
            scoreList.append(scoreList[elf[0]] + scoreList[elf[1]] - 10)
        else:
            scoreList.append(scoreList[elf[0]] + scoreList[elf[1]])
        elf[0] += scoreList[elf[0]] + 1
        elf[1] += scoreList[elf[1]] + 1
        elf[0] = elf[0] % len(scoreList)
        elf[1] = elf[1] % len(scoreList)
    print("Part 1: ", end='')
    for n in range(puzzleInput, puzzleInput+10):
        print(scoreList[n], end='')
    print("")


def part2():
    scoreList = [3, 7]
    elf = [0, 1]
    puzzleInput = [5, 0, 3, 7, 6, 1]
    ans = 0
    while ans == 0:
        if scoreList[elf[0]] + scoreList[elf[1]] > 9:
            scoreList.append(1)
            if checkLastScores(scoreList, puzzleInput):
                ans = len(scoreList) - len(puzzleInput)
            scoreList.append(scoreList[elf[0]] + scoreList[elf[1]] - 10)
            if checkLastScores(scoreList, puzzleInput):
                ans = len(scoreList) - len(puzzleInput)
        else:
            scoreList.append(scoreList[elf[0]] + scoreList[elf[1]])
            if checkLastScores(scoreList, puzzleInput):
                ans = len(scoreList) - len(puzzleInput)
        elf[0] += scoreList[elf[0]] + 1
        elf[1] += scoreList[elf[1]] + 1
        elf[0] = elf[0] % len(scoreList)
        elf[1] = elf[1] % len(scoreList)
    print("Part 2: {} recipes".format(ans))


part2()
