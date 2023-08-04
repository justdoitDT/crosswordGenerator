import copy
import itertools
import time
import numpy as np
import pandas as pd


wordsList = ['david', 'selma', 'alex', 'quique', 'mamita']

class Crossword(object):
    def __init__(self, parentCrossword=None, insertPosition=None, insertOrientation=None, wordsList=None):
        '''
        # If self is an updated version of a previous Crossword object, input the following 3 parameters:
            :param parentCrossword: Crossword object - the previous iteration of which self is an updated version
            :param insertPosition: tuple (row, col) - position where first letter of next word will be inserted
            :param insertOrientation: int - 0 for 'across', 1 for 'down'

        # if self is a seed crossword (i.e. starting from a blank crossword), input only the following parameter:
            :param wordsList: list - ordered list of words to be inserted into the crossword
        '''

        # flag defaults to True; if the next word could not be inserted into parent crossword because
        # it was blocked by an existing word, flag will become False
        self.validInitialization = True

        # if this crossword is an updated version of another crossword
        if parentCrossword:
            self.wordsToInsert = parentCrossword.getWordsToInsert()[1:]
            self.lettersDict = parentCrossword.getLettersDict()
            self.positionsDict = parentCrossword.getPositionsDict()
            self.minRow = parentCrossword.getMinRow()
            self.maxRow = parentCrossword.getMaxRow()
            self.minCol = parentCrossword.getMinCol()
            self.maxCol = parentCrossword.getMaxCol()
            # insert next word 'across'
            if insertOrientation == 0:
                for index, char in enumerate(parentCrossword.getWordsToInsert()[0]):
                    # if position is blank
                    if (insertPosition[0], insertPosition[1] + index) not in self.positionsDict:
                        # add letter in that position
                        self.positionsDict[(insertPosition[0], insertPosition[1] + index)] = char
                        self.lettersDict[char].append((insertPosition[0], insertPosition[1] + index))
                        # update minCol
                        if index == 0:
                            self.minCol = min(self.minCol, insertPosition[1])
                    # if position is already taken by another letter
                    elif self.positionsDict[(insertPosition[0], insertPosition[1] + index)] != char:
                        # self is an invalid crossword; flip flag to False
                        self.validInitialization = False
                        break
                # if word inserted successfully, update maxCol
                else:
                    self.maxCol = max(self.maxCol, insertPosition[1] + len(parentCrossword.getWordsToInsert()[0]) - 1)
            # insert next word 'down'
            elif insertOrientation == 1:
                for index, char in enumerate(parentCrossword.getWordsToInsert()[0]):
                    # if position is blank
                    if (insertPosition[0] + index, insertPosition[1]) not in self.positionsDict:
                        # add letter in that position
                        self.positionsDict[(insertPosition[0] + index, insertPosition[1])] = char
                        self.lettersDict[char].append((insertPosition[0] + index, insertPosition[1]))
                        # update minRow
                        if index == 0:
                            self.minRow = min(self.minRow, insertPosition[0])
                    # if position is already taken by another letter
                    elif self.positionsDict[(insertPosition[0] + index, insertPosition[1])] != char:
                        # self is an invalid crossword; flip flag to False
                        self.validInitialization = False
                        break
                # if word inserted successfully, update maxRow
                else:
                    self.maxRow = max(self.maxRow, insertPosition[0] + len(parentCrossword.getWordsToInsert()[0]) - 1)

        # if this is a seed crossword (i.e. starting from a blank crossword)
        else:
            self.wordsToInsert = wordsList[1:]
            self.lettersDict = {'A':[], 'B':[], 'C':[], 'D':[], 'E':[], 'F':[], 'G':[], 'H':[], 'I':[], 'J':[], 'K':[],
                            'L':[], 'M':[], 'N':[], 'O':[], 'P':[], 'Q':[], 'R':[], 'S':[], 'T':[], 'U':[], 'V':[],
                            'W':[], 'X':[], 'Y':[], 'Z':[]}
            self.positionsDict = {}
            # insert initial word 'across' starting from (0, 0)
            for index, char in enumerate(wordsList[0]):
                self.lettersDict[char].append((0, index))
                self.positionsDict[(0, index)] = char
            self.minRow = 0
            self.maxRow = 0
            self.minCol = 0
            self.maxCol = len(wordsList[0]) - 1

    def getValidInitialization(self):
        return self.validInitialization
    def getWordsToInsert(self):
        return self.wordsToInsert.copy()
    def getLettersDict(self):
        return copy.deepcopy(self.lettersDict)
    def getPositionsDict(self):
        return self.positionsDict.copy()
    def getMinRow(self):
        return self.minRow
    def getMaxRow(self):
        return self.maxRow
    def getMinCol(self):
        return self.minCol
    def getMaxCol(self):
        return self.maxCol
    def getSize(self):
        return max(self.maxRow - self.minRow + 1, self.maxCol - self.minCol + 1)
    def setReIndexedPositionsDict(self):
        '''
        Re-indexes "self.positionsDict" so that the minimum row and column values are 0. Stores re-indexed
        arrangement to a variable called "self.reIndexedPositionsDict"
        '''
        self.reIndexedPositionsDict = {}
        for row, col in self.positionsDict:
            self.reIndexedPositionsDict[(row - self.minRow, col - self.minCol)] = self.positionsDict[(row, col)]
    def getReIndexedPositionsDict(self):
        return self.reIndexedPositionsDict.copy()
    def getReflectedPositionsDict(self):
        reflectedPositionsDict = {}
        for row, col in self.reIndexedPositionsDict:
            reflectedPositionsDict[(col, row)] = self.reIndexedPositionsDict[(row, col)]
        return reflectedPositionsDict.copy()

    def isValid(self):
        '''
        Checks validity of crossword; it must contain only, and all of, the words that were meant to be inserted
        :return: bool - True if crossword is valid, False if crossword is invalid
        '''
        wordsInCrossword = []
        # read & record words across each row
        for row in range(self.minRow, self.maxRow + 1):
            rowChars = ''
            for col in range(self.minCol, self.maxCol + 1):
                try:
                    rowChars += self.positionsDict[(row, col)]
                except KeyError:
                    rowChars += '/'
            wordsInRow = rowChars.split('/')
            # check for words that were not meant to be inserted
            for word in wordsInRow:
                if len(word) < 2:
                    continue
                elif word in wordsSet:
                    wordsInCrossword.append(word)
                else:
                    return False
        # read & record words down each column
        for col in range(self.minCol, self.maxCol + 1):
            colChars = ''
            for row in range(self.minRow, self.maxRow + 1):
                try:
                    colChars += self.positionsDict[(row, col)]
                except KeyError:
                    colChars += '/'
            wordsInCol = colChars.split('/')
            # check for words that were not meant to be inserted
            for word in wordsInCol:
                if len(word) < 2:
                    continue
                elif word in wordsSet:
                    wordsInCrossword.append(word)
                else:
                    return False
        # check for missing words or unintended duplicates by comparing the sorted list of words in the
        # crossword with the sorted list of words that were meant to be inserted
        return sorted(wordsInCrossword) == wordsList

    def printCrossword(self):
        array = np.full((self.maxRow - self.minRow + 1, self.maxCol - self.minCol + 1), ' ')
        for row, col in self.getPositionsDict():
            array[row - self.minRow, col - self.minCol] = self.getPositionsDict()[(row, col)]
        print(pd.DataFrame(array).to_string(header=False, index=False))
        print('size: ' + str(self.getSize()) + '\n')


def dfs(crossword):
    '''
    Depth first search. At each level, a new Crossword object is created as an update to the parent crossword.
    The next word is inserted at every position (& orientation) where the word and the parent crossword share
    a letter. If the word could not be inserted because it was blocked by an existing word, we return up one
    level to the parent crossword. When a complete, valid, and unique crossword is discovered, it is stored in
    a dictionary called "validCrosswords", and a dictionary of the letters occupying each position (and the
    reflection of this arrangement) is stored in a hashable list called "alreadyDiscovered".
    :param crossword: Crossword object - the parent crossword
    :return: None
    '''

    # if parent crossword could not be updated correctly with current position/orientation of inserted word
    if not crossword.getValidInitialization():
        return

    # if crossword is complete
    if not crossword.getWordsToInsert():
        # if crossword is valid
        if crossword.isValid():
            # if crossword is unique
            crossword.setReIndexedPositionsDict()
            if crossword.getReIndexedPositionsDict() not in alreadyDiscovered \
                    and crossword.getReflectedPositionsDict() not in alreadyDiscovered:
                # add crossword to alreadyDiscovered
                alreadyDiscovered.append(crossword.getReIndexedPositionsDict())
                # add crossword to validCrosswords according to its size
                try:
                    validCrosswords[crossword.getSize()].append(crossword)
                except KeyError:
                    validCrosswords[crossword.getSize()] = [crossword]
                    # if new smallest crossword discovered, print it
                    if crossword.getSize() == min(validCrosswords):
                        print('Smallest crossword discovered so far:')
                        crossword.printCrossword()
        return

    # if crossword is not yet complete
    for index, char in enumerate(crossword.getWordsToInsert()[0]):
        for existingLetterPosition in crossword.getLettersDict()[char].copy():
            # insert 'across'
            dfs(Crossword(parentCrossword=crossword,
                          insertPosition=(existingLetterPosition[0], existingLetterPosition[1] - index),
                          insertOrientation=0))
            # insert 'down'
            dfs(Crossword(parentCrossword=crossword,
                          insertPosition=(existingLetterPosition[0] - index, existingLetterPosition[1]),
                          insertOrientation=1))
    return


# execute DFS function for each unique order of words to be inserted
startTime = time.time()
for i in range(len(wordsList)):
    wordsList[i] = wordsList[i].upper()
wordsList.sort()
wordsSet = set(wordsList)
validCrosswords = {}
alreadyDiscovered = []
for perm in itertools.permutations(wordsList):
    dfs(Crossword(wordsList=list(perm)))

# print results
sortedValidCrosswords = {i:validCrosswords[i] for i in sorted(list(validCrosswords.keys()))}
sizes = list(sortedValidCrosswords.keys())
arrangements = []
count = 0
print('\nProcess completed.\n')
for i in sortedValidCrosswords:
    arrangements.append(len(sortedValidCrosswords[i]))
    for j in sortedValidCrosswords[i]:
        j.printCrossword()
        count += 1
arrangementsPerSizeDict = {'Size':sizes, 'Arrangements':arrangements}
df = pd.DataFrame(data=arrangementsPerSizeDict).to_string(index=False)
print(df)
print('\nTotal arrangements:', count)
print('(' + str(round(time.time() - startTime, 2)) + ' seconds)')