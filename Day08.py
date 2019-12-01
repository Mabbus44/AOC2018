from MabbusLib import getFileContent


class Node:
    def __init__(self):
        self.childCount = 0
        self.metadataCount = 0
        self.children = []
        self.metadata = []

    def setValues(self, data):
        self.childCount = data[0][data[1]]
        self.metadataCount = data[0][data[1]+1]
        data[1] += 2
        for i in range(self.childCount):
            self.children.append(Node())
            self.children[i].setValues(data)
        for i in range(self.metadataCount):
            self.metadata.append(data[0][data[1]])
            data[1] += 1

    def sumOfMetadata(self):
        dataSum = 0
        for m in self.metadata:
            dataSum += m
        for c in self.children:
            dataSum += c.sumOfMetadata()
        return dataSum

    def part2Sum(self):
        dataSum = 0
        if self.childCount == 0:
            for m in self.metadata:
                dataSum += m
        else:
            for m in self.metadata:
                if m-1 < self.childCount:
                    dataSum += self.children[m-1].part2Sum()
        return dataSum

    def print(self, family):
        print("Name: {}".format(family))
        print("Data: {} (".format(self.metadataCount), end='')
        first = True
        for d in self.metadata:
            if first:
                print("{}".format(d), end='')
                first = False
            else:
                print(", {}".format(d), end='')
        print(")")
        print("Children: {} (".format(self.childCount))
        i = 0
        for d in self.children:
            d.print(family + "-{}".format(i))
            i += 1
        print(")", end='')


def part1():
    #   Read file
    dataInput = getFileContent("Day 8 Input.txt", True, False, " ")
    data = [dataInput, 0]
    n = Node()
    n.setValues(data)
    print("Part 1: {}".format(n.sumOfMetadata()))


def part2():
    #   Read file
    dataInput = getFileContent("Day 8 Input.txt", True, False, " ")
    data = [dataInput, 0]
    n = Node()
    n.setValues(data)
    print("Part 2: {}".format(n.part2Sum()))


part2()
