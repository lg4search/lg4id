import re
from bitarray import bitarray
from itertools import groupby

#import numpy as np

def getTestString(filename):
    #print(filename)
    lineList = []
    with open(filename, 'r') as file:
        for line in file:
            lineList.append(line.strip())
    #re.sub(r"\r?\n", "", outString)
    return "".join(lineList)

def fasta_iter(fasta_name):
    fh = open(fasta_name)
    faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
    for header in faiter:
        headerStr = header.__next__()[1:].strip()
        seq = "".join(s.strip() for s in faiter.__next__())
        yield headerStr,seq


def getMatches(inString):
    #import numpy as np
    
    #print("getting matches")
    stringLength = len(inString)
    patternLength = 3
    correctedLength = stringLength - patternLength + 1

    #boolArray = [[0,0] for _ in range(correctedLength)]#np.zeros((correctedLength,2))
    balry={}
    c_ray=correctedLength*bitarray('0')
    g_ray=correctedLength*bitarray('0')
    balry['0']=c_ray
    balry['1']=g_ray
    stringIterator = iter(range(correctedLength))
    for i in stringIterator:
        #print("beginning of iteration: " + str(i))
        #if((i % 1000000) == 0):
        #    print( str(i // 1000000) + " Million")
        tempString = inString[i:i + patternLength]
        if (tempString.upper() == "CCC"):
            balry['0'][i] = 1
            #print("*********skipping*********")
            for _ in range(patternLength - 1):
                try:
                    next(stringIterator)
                    #print(i)
                except StopIteration:
                    continue
        elif (tempString.upper() == "GGG"):
            balry['1'][i] = 1
            #print("*********skipping**********")
            for _ in range(patternLength - 1):
                try:
                    next(stringIterator)
                    #print(i)
                except StopIteration:
                    continue
    #print(boolArray)

    return balry

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
    #stringLength = len(inString)

    lG4List = []
    inLG4 = False
    currentStart = 0
    currentEnd = 0
    runningTotalGGG = 0
    runningTotalCCC = 0
    tfray={}
    tfray[True]=1
    tfray[False]=0

    matchArray = getMatches(inString)

    #print("calculating totals")
    #calculatate sums for first bin to initialize
    #for i in range(binSize):
        #tempCCC = matchArray[i][0]
        #tempGGG = matchArray[i][1]

    runningTotalCCC =matchArray['0'][0:binSize].count()
    runningTotalGGG =matchArray['1'][0:binSize].count()

    maxRunningTotal = max(runningTotalCCC, runningTotalGGG)
    if (maxRunningTotal > minHits):
        #this means the first bin was an LG4
        inLG4 = True
        currentStart = 0
        currentEnd = binSize


    #now go through next bin through end, adding next entry to running total and subtracting last entry of last bin to total
    for i in range(binSize, matchArray['0'].length()):
        #if((i % 1000000) == 0):
        #    print( str(i // 1000000) + " Million")
        lastBinStart = i - binSize

        tempCCC = tfray[matchArray['0'][i]]
        tempGGG = tfray[matchArray['1'][i]]

        tempCCClastBin = tfray[matchArray['0'][lastBinStart]]
        tempGGGlastBin = tfray[matchArray['1'][lastBinStart]]

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
    with open('input_filenames.txt') as inp:
        for line in inp:
            f_name=line.strip()
            print(f_name)
            with open(str(f_name.rsplit('.',1)[0].rsplit('/',1)[-1])+'.txt','w') as op_file:
                f_rdr=fasta_iter(f_name)
                for ij in f_rdr:
                    hdr,seq=ij
                    op_file.write(hdr+'\n')
                    lg4=driver(seq)
                    hits=0
                    for k in lg4:
                        hits+=1
                        binStart = k['binStart']
                        binEnd = k['binEnd']
                        sequence=k['sequence']
                        op_file.write('Hit::'+str(hits)+'\n')
                        op_file.write('Start-End Positions:: '+str(binStart)+'\t'+str(binEnd)+'\n')
                        op_file.write('Sequence:'+'\n')
                        op_file.write(str(sequence)+'\n')



