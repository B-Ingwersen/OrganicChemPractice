from organicDefinitions import *

def numbersToString(nums):
    if len(nums) == 0:
        return ""
    if len(nums) == 1 and nums[0] == 1:
        return ""
    string = "-"
    for num in nums:
        string += str(num) + ","
    string = string[:-1] + "-"
    if len(nums) > 1:
        string += prefixes[len(nums)][0]
    return string

def numbersToString2(nums, noOne = True):
    if len(nums) == 0:
        return ""
    if len(nums) == 1 and nums[0] == 0 and noOne:
        return ""
    string = "-"
    for num in nums:
        string += str(num + 1) + ","
    string = string[:-1] + "-"
    if len(nums) > 1:
        string += prefixes[len(nums) - 2][0]
    return string


def getNumbers(name):
    numbers = []
    if name[-1] != "-":
        return name, [1]
    name = name[:-1]
    while True:
        numbers += [int(name[-1])]
        if (name[-2] == ","):
            name = name[:-2]
        else:
            name = name[:-1]
            break;
    if name[-1] == "-":
        name = name[:-1]
    return name, numbers

def getPrefixNumber(name):
    for prefix in prefixes:
        if name[-len(prefix[0]):] == prefix[0]:
            name = name[:-len(prefix[0])]
            return name, prefix[1]
    return name, 0

def getParentNumber(name):
    for n in parentNumbers:
        if name[-len(n[0]):] == n[0]:
            name = name[:-len(n[0])]
            return name, n[1]
    return name, 1

def getSubstituents(name):
    for sub in substituents:
        if name[-len(sub[1]):] == sub[1]:
            name = name[:-len(sub[1])]
            substituent = [0,[1],sub]

            name, number = getPrefixNumber(name)
            numbers = [1]*number
            name, numbers = getNumbers(name)

            return name, [number, numbers,sub]
        elif sub[1] == "":
            return name, [0, [1], sub]

def fixOrderRules(doubles, triples, parentLength, mainChain):
    directionKnown = False
    if len(doubles) != 0 and min(doubles) > parentLength - 1 - max(doubles):
        for i in range(len(doubles)):
            doubles[i] = parentLength - doubles[i] - 1
        for i in range(len(triples)):
            triples[i] = parentLength - triples[i] - 1
        mainChain.reverse();
        directionKnown = True
    elif len(doubles) == 0 or min(doubles) == parentLength - 1 - max(doubles):
        if len(triples) != 0 and min(triples) > parentLength - 1 - max(triples):
            for i in range(len(doubles)):
                doubles[i] = parentLength - doubles[i] - 1
            for i in range(len(triples)):
                triples[i] = parentLength - triples[i] - 1
            directionKnown = True
            mainChain.reverse();
    else:
        directionKnown = True
    doubles.sort()
    triples.sort()
    return doubles, triples, directionKnown, mainChain

def fixRotation(doubles, triples, parentLength):
    directionKnown = True
    rotate = 0
    if len(doubles) != 0:
        best = sum(doubles)
        for i in range(parentLength):
            for j in range(len(doubles)):
                doubles[j] = (doubles[j] + 1 + parentLength) % parentLength
            if min(doubles) == 0 and sum(doubles) < best:
                rotate = i
    elif len(triples) != 0:
        best = sum(triples)
        for i in range(parentLength):
            for j in range(len(triples)):
                triples[j] = (triples[j] + 1 + parentLength) % parentLength
            if min(triples) == 0 and sum(triples) < best:
                rotate = i
    else:
        directionKnown = False
    
    for i in range(rotate):
        for j in range(len(doubles)):
            doubles[j] = (doubles[j] + 1 + parentLength) % parentLength
        for j in range(len(triples)):
            triples[j] = (triples[j] + 1 + parentLength) % parentLength

    doubles.sort()
    triples.sort()
    return doubles, triples, directionKnown