def crossword(words, findAll):
    '''
    input:
        words (list) - a list of strings to be inserted into the crossword
    output:
        crosswords (list of tuples) - a list of valid crossword arrangements. each entry is a tuple containing:
                                      (max dimension, min dimension, height, width, crossword grid)
    constraints:
        for a crossword arrangement to be valid, all adjacent characters must be part of a word in words
    '''

# helper functions
    import copy

    def DFS(allWords, orderedWords, grid, availableLetters):
        '''
        recursive depth-first search function
        inputs:
            allWords (list) - the list of all the words that will be added to the crossword
            orderedWords (list) - the list of words that still need to be added, in the order they will be added
            grid (list of lists) - the crossword grid
            availableLetters (dict) - keys are the letters of the alphabet, values are coordinates (tuples) describing
                                      where the letter is available on the grid: (row index, column index, 'across'/'down')
        output:
            output (list of tuples) - a list of valid crossword arrangements. each entry is a tuple containing:
                                      (max dimension, min dimension, height, width, crossword grid)
        '''
        output = []
        # if all the words have been inserted
        if not orderedWords:
            # if the grid is valid, trim it and return it up to the previous depth
            if isValidGrid(allWords, grid):
                return [trimGrid(grid)]
            # if the grid is invalid, return nothing back up to the previous depth
            else:
                return []
        # if there are more words to insert
        else:
            for index, char in enumerate(orderedWords[0]):
                for dictIndex, position in enumerate(availableLetters[char]):
                    newGrid, newAvailableLetters = insertWord(orderedWords[0], index, copy.deepcopy(grid), position, copy.deepcopy(availableLetters))
                    if newGrid:
                        newAvailableLetters[char].pop(dictIndex)
                        output += DFS(allWords, orderedWords[1:], newGrid, newAvailableLetters)
        return output


    def insertWord(word, crossLetterIndex, grid, position, availableLetters):
        '''
        inputs:
            word (string) - the word to be inserted into the grid
            crossLetterIndex (int) - the index of the letter in word that crosses with an existing word in the grid
            grid (list of lists) - the crossword grid
            position (tuple) - coordinate where the inserted word will cross with an existing word (row index, column index, 'across'/'down')
            availableLetters (dict) - keys are the letters of the alphabet, values are coordinates (tuples) describing
                                      where the letter is available on the grid: (row index, column index, 'across'/'down')
        outputs:
            returns the new crossword grid (if word is successfully inserted), returns [] otherwise
            returns the new availableLetters dictionary
        '''
        # if inserting across
        if position[2] == 'across':
            # insert the letters right of the crossLetter
            for lettersAfterCross in range(1, len(word) - crossLetterIndex):
                # if the position is blank, insert letter
                if grid[position[0]][position[1] + lettersAfterCross] == ' ':
                    grid[position[0]][position[1] + lettersAfterCross] = word[crossLetterIndex + lettersAfterCross]
                    availableLetters[word[crossLetterIndex + lettersAfterCross]] += [(position[0], position[1] + lettersAfterCross, 'down')]
                # if the position already contains this letter, do nothing
                elif grid[position[0]][position[1] + lettersAfterCross] == word[crossLetterIndex + lettersAfterCross]:
                    pass
                # if the position already contains another letter, the word cannot be inserted
                else:
                    return [], availableLetters
            # insert the letters left of the crossLetter
            for indexLetterBefore in range(crossLetterIndex):
                # if the position is blank, insert letter
                if grid[position[0]][position[1] - crossLetterIndex + indexLetterBefore] == ' ':
                    grid[position[0]][position[1] - crossLetterIndex + indexLetterBefore] = word[indexLetterBefore]
                    availableLetters[word[indexLetterBefore]] += [(position[0], position[1] - crossLetterIndex + indexLetterBefore, 'down')]
                # if the position already contains this letter, do nothing
                elif grid[position[0]][position[1] - crossLetterIndex + indexLetterBefore] == word[indexLetterBefore]:
                    pass
                # if the position already contains another letter, the word cannot be inserted
                else:
                    return [], availableLetters
        # if inserting down
        else:
            # insert the letters below the crossLetter
            for lettersBelowCross in range(1, len(word) - crossLetterIndex):
                # if the position is blank, insert letter
                if grid[position[0] + lettersBelowCross][position[1]] == ' ':
                    grid[position[0] + lettersBelowCross][position[1]] = word[crossLetterIndex + lettersBelowCross]
                    availableLetters[word[crossLetterIndex + lettersBelowCross]] += [(position[0] + lettersBelowCross, position[1], 'across')]
                # if the position already contains this letter, do nothing
                elif grid[position[0] + lettersBelowCross][position[1]] == word[crossLetterIndex + lettersBelowCross]:
                    pass
                # if the position already contains another letter, the word cannot be inserted
                else:
                    return [], availableLetters
            # insert the letters above the crossLetter
            for indexLetterAbove in range(crossLetterIndex):
                # if the position is blank, insert letter
                if grid[position[0] - crossLetterIndex + indexLetterAbove][position[1]] == ' ':
                    grid[position[0] - crossLetterIndex + indexLetterAbove][position[1]] = word[indexLetterAbove]
                    availableLetters[word[indexLetterAbove]] += [(position[0] - crossLetterIndex + indexLetterAbove, position[1], 'across')]
                # if the position already contains this letter, do nothing
                elif grid[position[0] - crossLetterIndex + indexLetterAbove][position[1]] == word[indexLetterAbove]:
                    pass
                # if the position already contains another letter, the word cannot be inserted
                else:
                    return [], availableLetters
        return grid, availableLetters


    def isValidGrid(words, grid):
        '''
        inputs:
            words (list) - list of all words to be inserted into the crossword
            grid (list of lists) - the crossword grid
        output:
            returns True, if the grid contains all words and no extraneous words
            returns False, otherwise
        '''
        wordsSet = set(words)
        gridWords = []
        # iterate through rows
        for row in grid:
            gridWords += ''.join(row).split()
        # iterate through columns
        verticalWords = ''
        for columnIndex in range(len(grid[0])):
            for row in grid:
                verticalWords += row[columnIndex]
        gridWords += verticalWords.split()
        # check against wordsSet
        for word in gridWords:
            if len(word) > 1 and word not in wordsSet:
                return False
        return True


    def trimGrid(grid):
        '''
        Removes the excess whitespace around the borders, and measures the dimensions of the resulting grid.
        input:
            grid (list of lists) - the crossword grid
        output:
            a tuple containing: (max dimension, min dimension, height, width, crossword grid)
        '''
        width = len(grid[0])
        height = len(grid)
        # remove top whitespace
        blankRow = [' '] * width
        for rowIndex in range(height):
            if grid[rowIndex] != blankRow:
                grid = grid[rowIndex:]
                height -= rowIndex
                break
        # remove bottom whitespace
        for rowIndex in range(height):
            if grid[rowIndex] == blankRow:
                grid = grid[:rowIndex]
                height = rowIndex
                break
        # remove left whitespace
        minLeftSpace = width
        for row in grid:
            leftSpace = 0
            for columnIndex in range(width):
                if row[columnIndex] == ' ':
                    leftSpace += 1
                else:
                    if leftSpace < minLeftSpace:
                        minLeftSpace = leftSpace
                        break
        for rowIndex in range(height):
            grid[rowIndex] = grid[rowIndex][minLeftSpace:]
        width -= minLeftSpace
        # remove right whitespace
        minRightSpace = width
        for row in grid:
            rightSpace = 0
            for columnIndex in range(width)[::-1]:
                if row[columnIndex] == ' ':
                    rightSpace += 1
                else:
                    if rightSpace < minRightSpace:
                        minRightSpace = rightSpace
                        break
        for rowIndex in range(height):
            grid[rowIndex] = grid[rowIndex][:-minRightSpace]
        width -= minRightSpace
        # return output
        #return (max(width, height), min(width, height), grid)
        return (max(width, height), min(width, height), height, width, grid)

    def initializeGrid(orderedWords, maxSize):
        '''
        inputs:
            orderedWords (list) - ordered list of words to be inserted in the crossword
            maxSize (int) - the dimensions of the crossword, equal to total length of words + 2
        output:
            grid (list of lists) - mostly empty crossword grid with the first word in orderedWords inserted dead center
            availableLetters (dict) - keys are the letters of the alphabet, values are coordinates (tuples) describing
                                      where the letter is available on the grid: (row index, column index, 'across'/'down')
        '''
        # generate blank grid of dimensions maxSize x maxSize
        grid = []
        for i in range(maxSize):
            grid.append([])
            for j in range(maxSize):
                grid[-1].append(' ')
        # initialize availableLetters
        availableLetters = {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [], 'H': [], 'I': [], 'J': [],
                            'K': [], 'L': [], 'M': [], 'N': [], 'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [],
                            'U': [], 'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
        # insert the first word in orderedWords right in the center, and populate availableLetters
        for index, char in enumerate(orderedWords[0]):
            grid[(len(grid) - 1) // 2][((maxSize - len(orderedWords[0])) // 2) + index] = char
            availableLetters[char].append(((len(grid) - 1) // 2, ((maxSize - len(orderedWords[0])) // 2) + index, 'down'))
        # return outputs
        return grid, availableLetters


#execute function

    # determine grid size and capitalize the words
    maxSize = 2
    for index, word in enumerate(words):
        maxSize += len(word)
        words[index] = word.upper()

    # initialize output list of valid crossword arrangements
    crosswords = []

    # execute a DFS for every permutation of words, append all valid arrangements to crosswords list
    import itertools
    permutations = list(itertools.permutations(words))
    for index, orderedWords in enumerate(permutations):
        print('Progress: ', round(index / len(permutations) * 100, 3), '%')
        grid, availableLetters = initializeGrid(orderedWords, maxSize)
        crosswords += DFS(words, orderedWords[1:], grid, availableLetters)
        # if FAST option was selected, stop iterating
        if findAll == 'FAST' and crosswords:
            break
    print('Progress: 100 %\n')

    # return all solutions
    return crosswords



# obtain user inputs
while True:
    findAll = str(input('To find all arrangements, enter ALL.\nTo find the ideal arrangement, enter IDEAL.\nTo find the fastest arrangement, enter FAST.\n\n'))
    if findAll.upper() == 'ALL':
        findAll = 'ALL'
        break
    elif findAll.upper() == 'FAST':
        findAll = 'FAST'
        break
    elif findAll.upper() == 'IDEAL':
        findAll = 'IDEAL'
        break
    else:
        print('Invalid input.\n')
print('\n')
validCrosswords = crossword(str(input('Enter list of words: ')).replace(',',' ').split(), findAll)

# assemble list of unique valid crossword arrangements
uniqueCrosswords = []
for crossword in validCrosswords:
    if crossword not in uniqueCrosswords:
        uniqueCrosswords.append(crossword)
uniqueCrosswords.sort()

# print the crossword(s)
if uniqueCrosswords:
    if findAll == 'ALL':
        for crossword in uniqueCrosswords[::-1]:
            # print dimensions of crossword
            print('\nSize:', crossword[2], 'x', crossword[3])
            # print each row of the crossword
            for row in crossword[4]:
                print(row)
        print('\n' + str(len(uniqueCrosswords)) + ' unique crossword arrangements.')
    else:
        # print each row of the first/only crossword
        for row in uniqueCrosswords[0][4]:
            print(row)
else:
    print('No possible crossword arrangements.')