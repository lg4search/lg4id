import re
#import numpy as np

def getTestString(filename):
    #print(filename)
    lineList = []
    with open(filename, 'r') as file:
        for line in file:
            lineList.append(line.strip())
    #re.sub(r"\r?\n", "", outString)
    return "".join(lineList)


def getMatches(inString):
    #import numpy as np
    #print('vachindi')
    #print("getting matches")
    stringLength = len(inString)
    patternLength = 3
    correctedLength = stringLength - patternLength + 1

    boolArray = [[0,0] for _ in range(correctedLength)]#np.zeros((correctedLength,2))
    #balry={}
    #balry['0']=cray
    #balry['1']=gray
    stringIterator = iter(range(correctedLength))
    for i in stringIterator:
        #print("beginning of iteration: " + str(i))
        #if((i % 1000000) == 0):
        #    print( str(i // 1000000) + " Million")
        tempString = inString[i:i + patternLength]
        if (tempString.upper() == "CCC"):
            boolArray[i][0] = 1
            #print("*********skipping*********")
            for _ in range(patternLength - 1):
                try:
                    next(stringIterator)
                    #print(i)
                except StopIteration:
                    continue
        elif (tempString.upper() == "GGG"):
            boolArray[i][1] = 1
            #print("*********skipping**********")
            for _ in range(patternLength - 1):
                try:
                    next(stringIterator)
                    #print(i)
                except StopIteration:
                    continue
    #print(boolArray)

    return boolArray

#def getCounts(regexResults):
#    count = 0

#    for entry in regexResults:
#        count += 1
#    return count

def processDictEntry(lG4List, currentStart, currentEnd, inString):
    if(len(lG4List) > 0):
        #get previous entry
        lastEntry = lG4List[-1]
        #go back to zero index
        lastStart = lastEntry['binStart'] - 1
        lastEnd = lastEntry['binEnd']

        #need to merge
        if(currentStart <= lastEnd):
            #remove the last entry
            lG4List.pop()
            currentStart = lastStart
            #current End stays the same

    sequenceString = inString[currentStart:currentEnd ]
    tempDict = {'binStart': currentStart + 1, 'binEnd': currentEnd, 'sequence' : sequenceString }
    lG4List.append(tempDict)

def driver(inString, binSize=1500, minHits=120):
    stringLength = len(inString)

    lG4List = []
    inLG4 = False
    currentStart = 0
    currentEnd = 0
    runningTotalGGG = 0
    runningTotalCCC = 0

    matchArray = getMatches(inString)

    #print("calculating totals")
    #calculatate sums for first bin to initialize
    for i in range(binSize):
        tempCCC = matchArray[i][0]
        tempGGG = matchArray[i][1]

        runningTotalCCC += tempCCC
        runningTotalGGG += tempGGG

    maxRunningTotal = max(runningTotalCCC, runningTotalGGG)
    if (maxRunningTotal > minHits):
        #this means the first bin was an LG4
        inLG4 = True
        currentStart = 0
        currentEnd = binSize


    #now go through next bin through end, adding next entry to running total and subtracting last entry of last bin to total
    for i in range(binSize, len(matchArray)):
        #if((i % 1000000) == 0):
        #    print( str(i // 1000000) + " Million")
        lastBinStart = i - binSize

        tempCCC = matchArray[i][0]
        tempGGG = matchArray[i][1]

        tempCCClastBin = matchArray[lastBinStart][0]
        tempGGGlastBin = matchArray[lastBinStart][1]

        runningTotalCCC += tempCCC
        runningTotalGGG += tempGGG

        runningTotalCCC -= tempCCClastBin
        runningTotalGGG -= tempGGGlastBin

        maxRunningTotal = max(runningTotalCCC, runningTotalGGG)
        #print(maxCount)
        if (maxRunningTotal > minHits):
            if ( inLG4 == False ):
                currentStart = i - binSize + 1
                currentEnd = i + 1
                inLG4 = True
            else:
                currentEnd = i + 1
        else:
            if ( inLG4 == True ):
                inLG4 = False
                #print(str(currentStart) + " - " + str(currentEnd))
                #sequence string applies to previous bin (because current failed), so - 1

                #check that not overlapping with previous entry
                #can modify lG4List as side effect, adding or removing entries
                processDictEntry(lG4List, currentStart, currentEnd, inString)
                #sequenceString = inString[currentStart:currentEnd ]
                #tempDict = {'binStart': currentStart + 1, 'binEnd': currentEnd, 'sequence' : sequenceString }
                #lG4List.append(tempDict)
    #on last iteration, check if in LG4 to write outString
    if ( inLG4 == True ):
        inLG4 = False
        #print(str(currentStart) + " - " + str(currentEnd))
        #sequence string applies to previous bin (because current failed), so - 1
        #sequenceString = inString[currentStart:currentEnd ]
        #tempDict = {'binStart': currentStart + 1, 'binEnd': currentEnd, 'sequence' : sequenceString }
        #lG4List.append(tempDict)
        processDictEntry(lG4List, currentStart, currentEnd, inString)
    return lG4List
if __name__ == '__main__':
    #testString = getTestString("C:/SALTS/lncrna/grant/Grant-file_upload/Grant-file_upload-new/testG4sequencesnew.txt")
    #testString = getTestString()
    #print("Got String")
    #tempMatches = getMatches(testString)
    #print(tempMatches)
    #print(getCounts(tempMatches))
    for i in driver(testString):
        print(i)
