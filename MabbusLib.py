def filterNumbers(strNum):
    #   Returns true if string contains number
    try:
        int(strNum)
        return True
    except ValueError:
        return False


def getFileContent(fileName, returnNumber, individualChars, firstSplit="", secondSplit=""):
    #   Converts file into lists of strings or integers
    #   IndividualChars can only be combined with returnNumber or firstSplit, not both and not secondSplit (lazy patch)
    #   Load file
    inputFile = open(fileName, "r")
    content = inputFile.read()
    inputFile.close()

    #   Replace characters if splits is list
    if not isinstance(firstSplit, str):
        for letter in firstSplit:
            content = content.replace(letter, firstSplit[0])
        firstSplit = firstSplit[0]
    if not isinstance(secondSplit, str):
        for letter in secondSplit:
            content = content.replace(letter, secondSplit[0])
        secondSplit = secondSplit[0]

    #   If "individualChars" split the string into chars
    if individualChars:
        ret = list(content)
        if firstSplit != "":
            content = list(filter(None, content.split(firstSplit)))
            ret = []
            for row in content:
                ret.append(list(row))
            return ret
        if returnNumber:
            ret = list(map(int, list(filter(filterNumbers, ret))))
        return ret

    #   Split the string by "firstSplit" if defined
    if firstSplit != "":
        if returnNumber and secondSplit == "":
            content = list(map(int, list(filter(filterNumbers, content.split(firstSplit)))))
        else:
            content = list(filter(None, content.split(firstSplit)))

    #   Split each string by "secondSplit" if defined
    if secondSplit != "":
        ret = []
        for row in content:
            if returnNumber:
                ret.append(list(map(int, list(filter(filterNumbers, row.split(secondSplit))))))
            else:
                ret.append(list(filter(None, row.split(secondSplit))))
    else:
        ret = content
    return ret


class RoundList:
    def __init__(self, newObj):
        self.obj = newObj
        self.prev = self
        self.nxt = self

    def delete(self):
        self.nxt.prev = self.prev
        self.prev.nxt = self.nxt

    def add(self, newObj):
        newListObj = RoundList(newObj)
        newListObj.prev = self
        newListObj.nxt = self.nxt
        self.nxt.prev = newListObj
        self.nxt = newListObj
