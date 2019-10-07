import random
from math import *

from nameProcessing import *
from genericMolecule import *

class organicMolecule:

    def __init__(self, name):
        self.name = name
        self.name = self.generateRandom()
        self.getStructureFromName()
    
    def getStructureFromName(self):
        name = self.name

        n = "                     " + name

        for group in functionalGroups:
            ending = group[1]
            endLen = len(ending)
            if (n[-endLen:] == ending):
                break
            
        n = n[:-len(group[1])]
        n, nFuncGroups = getPrefixNumber(n)
        n, funcGroupNums = getNumbers(n)
        self.functionalGroup1 = [funcGroupNums, group]

        if (n[-1] == "-"):
            self.functionalGroup1[0] = int(n[-2])
            n = n[:-3]
        
        self.tripleBonds = []
        self.nTripleBonds = 0
        if (n[-2:] == "yn"):
            self.tripleBonds += [0]
            n = n[:-2]
            n, self.nTripleBonds = getPrefixNumber(n);
            n, self.tripleBonds = getNumbers(n)
        
        self.doubleBonds = []
        self.nDoubleBonds = 0
        if (n[-2:] == "en"):
            n = n[:-2]
            n, self.nDoubleBonds = getPrefixNumber(n);
            self.doubleBonds += [0]
            n, self.doubleBonds = getNumbers(n)

        
        if n[-2:] == "an":
            n = n[:-2]

        n,self.parentNumber = getParentNumber(n)

        self.substituents = []
        while True:
            n, substituent = getSubstituents(n)
            if substituent[2][0] == SUBSTITUENT_DNE:
                break;
            self.substituents += [substituent]

        self.mainChain = []
        for i in range(self.parentNumber):
            self.mainChain += [[2,1,1,[],[]]]

        for b in self.doubleBonds:
            self.mainChain[b - 1][2] = 2
            self.mainChain[b][1] = 2
        
        for b in self.tripleBonds:
            self.mainChain[b - 1][2] = 3
            self.mainChain[b][1] = 3
        
        if self.functionalGroup1[1][0] != "none":
            for i in self.functionalGroup1[0]:
                self.mainChain[i - 1][3] += [self.functionalGroup1[1]]
        
        for substituent in self.substituents:
            for number in substituent[1]:
                self.mainChain[number - 1][4] += [substituent[2]]

        self.rootJunction = moleculeJunction()
        self.mainChainJunctions = [self.rootJunction]
        self.junctions = [self.rootJunction]
        self.bonds = []

        direction = 0
        angle = -30
        self.rootJunction.chainExtention = (180 + (direction - angle)) % 360
        for i in range(1, self.parentNumber):
            totalD = direction + angle
            if self.mainChain[i][1] == 3 or self.mainChain[i-1][1] == 3:
                totalD = direction - angle
            else:
                angle = -angle
            previousJunction = self.mainChainJunctions[-1]
            newJunction = moleculeJunction(sourceJunction=self.mainChainJunctions[-1], direction=totalD, distance=50, atom = "C")
            self.mainChainJunctions += [newJunction]
            self.junctions += [newJunction]
            self.bonds += [ moleculeBond( previousJunction, newJunction, self.mainChain[i][1] ) ]
        self.mainChainJunctions[-1].chainExtention = (180 - (direction + angle)) % 360
        
        for i in range(len(self.mainChain)):
            atom = self.mainChain[i]
            root = self.mainChainJunctions[i]
            n = len(atom[3]) + len(atom[4])
            dirs = root.getNextDirection(n)
            j = 0
            for fGroup in atom[3]:
                self.addFunctionalGroup(group, i+1, dirs[j])
                j += 1
            for substituent in atom[4]:
                self.addSubstituent(substituent, i+1, dirs[j])
                j += 1
    
    def addFunctionalGroup(self, group, number, d):
        root = self.mainChainJunctions[number - 1]
        if group[0] == "Carboxylic acid":
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "OH", label = "OH")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 1) ]
            d = root.getNextDirection(1)[0]
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "O", label = "O")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 2) ]
        if group[0] == "Ketone":
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "O", label = "O")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 2) ]
        if group[0] == "Aldehyde":
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "H", label = "H")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 1) ]
            d = root.getNextDirection(1)[0]
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "O", label = "O")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 2) ]
        if group[0] == "Alcohol":
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "OH", label = "OH")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 1) ]
        if group[0] == "Amine":
            j = moleculeJunction(sourceJunction = root, direction = d, distance = 50, atom = "N", label = "N")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 1) ]
            dirs = j.getNextDirection(2)
            j1 = moleculeJunction(sourceJunction = j, direction = dirs[0], distance = 50, atom = "H", label = "H")
            j2 = moleculeJunction(sourceJunction = j, direction = dirs[1], distance = 50, atom = "H", label = "H")
            self.junctions += [j1,j2]
            self.bonds += [ moleculeBond(j, j1, 1) ]
            self.bonds += [ moleculeBond(j, j2, 1) ]

    def addSubstituent(self, substituent, number, d):
        root = self.mainChainJunctions[number - 1]

        if substituent[0] == SUBSTITUENT_HALOGEN:
            root = self.mainChainJunctions[number - 1]
            j = moleculeJunction(sourceJunction=root, direction=d, distance = 50, atom = substituent[2], label = substituent[2])
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 1) ]
        elif substituent[0] == SUBSTITUENT_CHAIN:
            self.addSubstituentChain(substituent[2], root, d)
        elif substituent[0] == SUBSTITUENT_MODIFIED_CHAIN:
            offsets = []
            if substituent[1] == "isopropyl":
                offsets = [-60, 60]
            if substituent[1] == "tert-butyl":
                offsets = [-60, 0, 60]
            
            root = self.mainChainJunctions[number - 1]
            j = moleculeJunction(sourceJunction=root, direction=d, distance = 50, atom = "C")
            self.junctions += [j]
            self.bonds += [ moleculeBond(root, j, 1) ]

            d_base = j.outJunctions[0]
            for offset in offsets:
                jn = moleculeJunction(sourceJunction=j, direction=d + offset, distance = 50, atom = "C")
                self.junctions += [jn]
                self.bonds += [ moleculeBond(j, jn, 1) ]            
                
    def addSubstituentChain(self, length, root, direction):
        direction = direction + 30
        angle = -30
        for i in range(length):
            j = moleculeJunction(sourceJunction=root, direction=(direction+angle), distance=50, atom="C")
            self.junctions += [j]
            self.bonds += [moleculeBond(root, j, 1)]
            root = j
            angle = -angle

    def draw(self, canvas, canvas_width, canvas_height):
        canvas.delete(ALL)
        X = canvas_width / 2
        Y = canvas_height / 2

        minX = 0
        minY = 0
        maxX = 0
        maxY = 0
        for junction in self.junctions:
            x = junction.x
            y = junction.y
            if x < minX:
                minX = x
            if x > maxX:
                maxX = x
            if y < minY:
                minY = y
            if y > maxY:
                maxY = y
        
        X -= (minX + maxX) / 2
        Y -= (minY + maxY) / 2

        for bond in self.bonds:
            bond.draw(canvas, X, Y)
        for junction in self.junctions:
            junction.draw(canvas, X, Y)
    
    def generateRandom(self):
        parentLength = random.randint(2,10)
        parentChainName = parentNumbers[parentLength-1][0]

        directionKnown = False

        mainChain = []
        for i in range(parentLength):
            mainChain += [[2,1,1,0]]
        
        ending = "e"
        fGroup = False
        
        mainChain[0][0] -= 1
        mainChain[0][1] = 0
        mainChain[-1][0] -= 1
        mainChain[-1][2] = 0

        if parentLength > 2:
            if random.randint(1,7) < 5:
                locs = []
                t = random.randint(0,2);

                for i in range(parentLength):
                    if t == 2 and (i == 0 or i == parentLength - 1):
                        continue
                    if random.randint(1,parentLength) == 1:
                        if t == 1:
                            f = [[i],[i,i]][random.randint(0,1)]
                            mainChain[i][3] += 2*functionalGroups[t+2][2]
                            locs += f
                        else:
                            mainChain[i][3] += functionalGroups[t+2][2]
                            locs += [i]
                if locs != []:
                    fGroup = True
                    uselessTriples = []
                    locs, uselessTriples, directionKnown, mainChain = fixOrderRules(locs, uselessTriples, parentLength, mainChain)
                    ending = numbersToString2(locs) + functionalGroups[t + 2][1]

        if fGroup == False and parentLength > 1:
            fg = random.randint(1,4)
            if fg <= 2:
                fGroup = True
                mainChain[0][3] += functionalGroups[fg - 1][2]
                ending = functionalGroups[fg - 1][1]
                directionKnown = True
    
        doubles = []
        triples = []

        if parentLength > 1:
            for i in range(parentLength-1):
                if mainChain[i][3] == 0 and mainChain[i+1][3] == 0 and mainChain[i][1] in [0,1]:
                    if random.randint(1,3) == 1:
                        doubles += [i]
                        mainChain[i][2] = 2
                        mainChain[i+1][1] = 2
                    elif random.randint(1,6) == 1:
                        triples += [i]
                        mainChain[i][2] = 3
                        mainChain[i+1][1] = 3
        
        if not directionKnown:
            doubles, triples, directionKnown, mainChain  = fixOrderRules(doubles, triples,parentLength, mainChain)
                

        Fs = []
        Cls = []
        Brs = []
        Is = []
        halogens = [Fs,Cls,Brs,Is]
        sideChains = [[],[],[],[],[]]
        isoProps = []
        tertBs = []

        maxLengthFirstPass = 0
        for i in range(parentLength-1):
            remainingGroups = 4 - mainChain[i][1] - mainChain[i][2] - mainChain[i][3]
            if remainingGroups == 0:
                pass
            else:
                t = random.randint(1,4)

                nums = [i]
                if remainingGroups == 2:
                    if random.randint(1,2) == 1:
                        nums = [i,i]

                maxLength = 5
                        
                maxLength = min(parentLength - i - 2, maxLengthFirstPass)
                maxLength = min(5, maxLength)

                if t == 1:
                    halogens[random.randint(0,3)] += nums
                elif t == 2 and maxLength > 0:
                    maxVal = parentLength - i
                    length = random.randint(1,maxLength)
                    sideChains[length - 1] += nums
                elif t == 3 and maxLength > 2:
                    st = random.randint(1,4)
                    if st == 1:
                        isoProps += nums
                    if st == 2:
                        tertBs += nums
            
            if remainingGroups < 2 or mainChain[i][3] != 0:
                maxLengthFirstPass = 10
            maxLengthFirstPass += 1

        unsat1 = ""
        unsat2 = ""
        unsat3 = "an"

        unsatNoOne = True;
        if (parentLength > 3):
            unsatNoOne = False;

        if len(doubles) != 0:
            unsat3 = ""
            unsat1 = numbersToString2(doubles, noOne = unsatNoOne) + "en"
        if len(triples) != 0:
            unsat3 = ""
            unsat2 = numbersToString2(triples, noOne = unsatNoOne) + "yn"
        unsaturation = unsat1 + unsat2 + unsat3

        substituents = ""
        if len(Brs) != 0:
            substituents += numbersToString2(Brs, noOne = False) + "bromo"
        if len(sideChains[3]) != 0:
            substituents += numbersToString2(sideChains[3], noOne = False) + "butyl"
        if len(Cls) != 0:
            substituents += numbersToString2(Cls, noOne = False) + "chloro"
        if len(sideChains[1]) != 0:
            substituents += numbersToString2(sideChains[1], noOne = False) + "ethyl"
        if len(Fs) != 0:
            substituents += numbersToString2(Fs, noOne = False) + "fluoro"
        if len(Is) != 0:
            substituents += numbersToString2(Is, noOne = False) + "iodo"
        if len(isoProps) != 0:
            substituents += numbersToString2(isoProps, noOne = False) + "isopropyl"
        if len(sideChains[0]) != 0:
            substituents += numbersToString2(sideChains[0], noOne = False) + "methyl"
        if len(sideChains[4]) != 0:
            substituents += numbersToString2(sideChains[4], noOne = False) + "pentyl"
        if len(sideChains[2]) != 0:
            substituents += numbersToString2(sideChains[2], noOne = False) + "propyl"
        if len(tertBs) != 0:
            substituents += numbersToString2(tertBs, noOne = False) + "tert-butyl"

        name = substituents + parentChainName + unsaturation + ending
        if name[0] == "-":
            name = name[1:]

        return name