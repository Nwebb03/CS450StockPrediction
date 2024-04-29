import math
import gameState
        
"""
   Represents a matrix of all possible combinations of pattern indices.
"""   
class patternMatrix: 
    def __init__(self) -> None:
        """
        Initializes the pattern matrix and prunes it to remove invalid combos.
        """
        self.listOfCombos = []
        # Generate all possible combinations of pattern indices
        for i in range (0,3):
            for j in range (0,3):
                for k in range (0,3):
                    for l in range(0,3):
                        for m in range (0,3):
                            comboToAdd = [i,j,k,l,m]
                            self.listOfCombos.append(comboToAdd)
                                                  
        self.pruneMatrix()
    
    def calculateHashVal(pattern):
        """
        Calculates the hash value of a given pattern.

        Args:
            pattern: A list representing a pattern.

        Returns:
            Calculated hash value
        """
        hashVal = 0
        increment = 0
        for val in pattern[::-1]:
            hashVal += (3**increment) * val
            increment+=1

        return hashVal


    def pruneMatrix(self) -> None:
        #If the sum is 9, that means the pattern is invalid. (i.e. g,g,g,g,y)
        SUM_TO_DELETE = 9
        # Remove combinations where the sum of the first 5 elements is 9
        self.listOfCombos = [combo for combo in self.listOfCombos if sum(combo[:5]) != SUM_TO_DELETE]


"""
    Solves Wordle game by providing hints and narrowing down possible words.
"""
class wordleSolver:
    def __init__(self, gameState) -> None:
        """
        Initializes the Wordle solver.

        Args:
          gameState: instance of the gameState class
        """
        self.calculatedEntropies = []
        # Initialize pattern matrix and word lists
        self.patternMatrix = patternMatrix().listOfCombos
        self.gameState = gameState
        self.validWords = gameState.validSolutions  + gameState.validGuesses
        self.greyLettersList = []
        self.yellowLettersAndIndexes = []
        self.greenLettersAndIndexes = []

    def calculateExpectedEntropy(self, wordToCalculate):
        """
        Calculates the potential entropy of a given word.

        Args:
            wordToCalculate: word to calculate potential entropy for

        Returns:
            Calculated expected entropy value
        """
        patternsAndProbabilities = {}
        expectedEntropy = 0
        # Generate patterns and calculate probabilities
        for pattern in self.patternMatrix:
            patternsAndProbabilities[patternMatrix.calculateHashVal(pattern = pattern)] = []

        for word in self.validWords:
                pattern = self.gameState.checkWord(secretWord= word, guess=wordToCalculate)
                patternsAndProbabilities[patternMatrix.calculateHashVal(pattern = pattern)].append(word)
      
        for pattern in self.patternMatrix:
           # Calculate expected entropy based on probabilities
           probabilityOfPattern = len(patternsAndProbabilities[patternMatrix.calculateHashVal(pattern = pattern)])/len(self.validWords)
           if probabilityOfPattern != 0:
                expectedEntropy += probabilityOfPattern * -1 * math.log2(probabilityOfPattern)
        
        return expectedEntropy

    def countOccurances(self, letter):
        """
        Counts the occurrences of a letter in word lists.

        Args:
            letter: letter to count

        Returns:
            Count of occurances
        """
        count = 0
        for i in self.greyLettersList:
            if letter == i:
                count += 1
        for j, k in self.greenLettersAndIndexes:
            if letter == j:
                count += 1
        for l, m in self.yellowLettersAndIndexes:
            if letter == l:
                count += 1
        return count
    
    def calculateTopNExpectedEntropies(self,n):
        """
        Calculates the top N expected entropies of words.

        Args:
            n: Number top entropies to calculate

        Returns:
            List of tuples containing words and their corresponding entropies, sorted by entropy in descending order.
        """
        calculatedEntropies = []
        i = 0
        for word in self.validWords:
            calculatedEntropies.append((word, self.calculateExpectedEntropy(word)))
            i += 1
            # TESTING - to visualize calculation progress
            #if i % 50 == 0:
                #print(i)
        calculatedEntropies.sort(key= lambda x: x[1], reverse=True)
        return calculatedEntropies[:n]

    def updateWordLists(self, guessedWordWithColors):
            """
            Updates the Wordle solver's word lists based on the guessed word and its colors.

            Args:
               guessedWordWithColors: A list of tuples containing the guessed word and its colors.
            """
            print(guessedWordWithColors)
            index = 0
            for letter in guessedWordWithColors:
                if letter[1] == 2 and (letter[0],index) not in self.greenLettersAndIndexes:
                    self.greenLettersAndIndexes.append((letter[0], index))
                    # TESTING PURPOSES
                    #print("appended to greenList: ")
                    #print(letter[0])
                elif letter[1] == 1 and (letter[0],index):
                    self.yellowLettersAndIndexes.append((letter[0],index))
                    # TESTING PURPOSES
                    #print("appended to yellow List: ")
                    #print(letter[0])

                elif ((letter[1] == 0) and (letter[0] not in self.greyLettersList) and (letter[0] not in [t[0] for t in self.yellowLettersAndIndexes]) and (letter[0] not in [x[0] for x in self.greenLettersAndIndexes])):
                    
                    self.greyLettersList.append(letter[0])
                    # TESTING PURPOSES
                    #print("appended to grey List: ")
                    #print(letter[0])
                            
                elif ((letter[1] == 0) and (letter[0] in [x[0] for x in self.greenLettersAndIndexes] )):
                    
                    self.deleteGreyDupes(letter)

                index += 1
            # # TESTING PURPOSES - visualize if validWords is being updated
            #print(len(self.validWords))
            self.keepGreenWords()
            #print(len(self.validWords))
            self.keepYellowWords()
            #print(len(self.validWords))
            self.deleteGreyWords()
            #print(len(self.validWords))


    def deleteGreyWords(self): 
        """
        Removes any words containing grey letters
        """
        greyWordsToRemove = [] # List of grey words
        print("Grey letters and indices:")
        print(self.greyLettersList)
        for word in self.validWords:
            for letter in self.greyLettersList:
                if (letter in word) and (letter not in [x[0] for x in self.greenLettersAndIndexes]):
                    greyWordsToRemove.append(word)
                    break

        # prunes list of validWords to not include words with grey letters    
        for word in greyWordsToRemove:
            if (word in self.validWords):
                self.validWords.remove(word)

    def deleteGreyDupes(self,dupe):
        """
        Deletes words containing duplicate grey letters from the Wordle solver's word lists.

        Args:
            dupe: duplicate letter tuple
        """
        print("deleting a dupe: ")
        print(dupe[0])
        greyDupesToRemove =[]
        if self.countOccurances(dupe[0]) > 2:
            for word in self.validWords:
                if (word.count(dupe[0])) > 2:
                    if (dupe[0] not in [x[0] for x in self.greenLettersAndIndexes] and dupe[0] not in [y[0] for y in self.yellowLettersAndIndexes]):
                        print("made it into removing the dupe")
                        print(word)
                        greyDupesToRemove.append(word)
        else:
            for word in self.validWords:
                if (word.count(dupe[0])) > 1:
                    if (dupe[0] not in [x[0] for x in self.greenLettersAndIndexes] and dupe[0] not in [y[0] for y in self.yellowLettersAndIndexes]):
                        print("made it into removing the dupe")
                        print(word)
                        greyDupesToRemove.append(word)
                
        for i in greyDupesToRemove:
            self.validWords.remove(i)
                
             
    def keepYellowWords(self):
        """
        Removes all words with yellow letter in guessed position
        """
        yellowWordsToRemove = []
        print("Yellow letters and indices:")
        # Check for words not containing green letter
        print(self.yellowLettersAndIndexes)
        for word in self.validWords:
            containsYellow = False
            for letter,_ in self.yellowLettersAndIndexes:
                if letter not in word:
                    yellowWordsToRemove.append(word)
                    break
            
        # Check for words where green letters are not in the guessed positions
        for word in self.validWords:
            for letter, index in self.yellowLettersAndIndexes:
                indecesOfLetter = [i for i, j in enumerate(word) if j == letter]
                if ((letter in word) and (index in indecesOfLetter)):
                    yellowWordsToRemove.append(word)
                    break
        
        # Remove words without green letters
        for word in yellowWordsToRemove:
            if (word in self.validWords):
                self.validWords.remove(word)
    
    def keepGreenWords(self):
        """
        Removes words where green letters are not in guessed positions
        """  
        greenWordsToRemove = []
        print("Green letters and indices")
        print(self.greenLettersAndIndexes)

        # Check for words not containing green letters
        for word in self.validWords:
            for letter,_ in self.greenLettersAndIndexes:
                if letter not in word:
                    greenWordsToRemove.append(word)
                    break
        
        # Check for words where green letters are not in the guessed positions
        for word in self.validWords:
            for letter, index in self.greenLettersAndIndexes:
                indecesOfLetter = [i for i, j in enumerate(word) if j == letter]     
                if ((letter in word) and (index not in indecesOfLetter)):
                    greenWordsToRemove.append(word)
                    break

        # Remove words without green letters
        for word in greenWordsToRemove:
            if (word in self.validWords):
                self.validWords.remove(word)
