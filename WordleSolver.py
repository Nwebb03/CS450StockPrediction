import math
import gameState
        
      
class patternMatrix: 
    def __init__(self) -> None:
        self.listOfCombos = []
        for i in range (0,3):
            for j in range (0,3):
                for k in range (0,3):
                    for l in range(0,3):
                        for m in range (0,3):
                            comboToAdd = [i,j,k,l,m]
                            self.listOfCombos.append(comboToAdd)
                            
                            
        self.pruneMatrix()
    
    def calculateHashVal(pattern):
        hashVal = 0
        increment = 0
        for val in pattern[::-1]:
            hashVal += (3**increment) * val
            increment+=1
        return hashVal


    def pruneMatrix(self) -> None:
        #If the sum is 9, that means the pattern is invalid. (i.e. g,g,g,g,y)
        SUM_TO_DELETE = 9
        self.listOfCombos = [combo for combo in self.listOfCombos if sum(combo[:5]) != SUM_TO_DELETE]

class wordleSolver:
    
    def __init__(self, gameState) -> None:
        self.calculatedEntropies = []
        self.patternMatrix = patternMatrix().listOfCombos
        self.gameState = gameState
        self.validWords = gameState.validSolutions + gameState.validGuesses
        self.greyLettersList = []
        self.yellowLettersAndIndexes = []
        self.greenLettersAndIndexes = []



    def calculateExpectedEntropy(self, wordToCalculate):
        patternsAndProbabilities = {}
        expectedEntropy = 0
        for pattern in self.patternMatrix:
            patternsAndProbabilities[patternMatrix.calculateHashVal(pattern = pattern)] = []
        for word in self.validWords:
                pattern = self.gameState.checkWord(secretWord= word, guess=wordToCalculate)
                patternsAndProbabilities[patternMatrix.calculateHashVal(pattern = pattern)].append(word)

        
        for pattern in self.patternMatrix:
           probabilityOfPattern = len(patternsAndProbabilities[patternMatrix.calculateHashVal(pattern = pattern)])/len(self.validWords)
           if probabilityOfPattern != 0:
                expectedEntropy += probabilityOfPattern * -1 * math.log2(probabilityOfPattern)
        
        return expectedEntropy


    def calculateTopNExpectedEntropies(self,n):
        calculatedEntropies = []
        i = 0
        for word in self.validWords:
            calculatedEntropies.append((word, self.calculateExpectedEntropy(word)))
            i+=1
            if i%50 == 0:
                print(i)
        calculatedEntropies.sort(key= lambda x: x[1], reverse=True)
        return calculatedEntropies[:n]

    def updateWordLists(self, guessedWordWithColors):
            print(guessedWordWithColors)
            index = 0
            for letter in guessedWordWithColors:
                if letter[1] == 0 and letter[0] not in self.greyLettersList:
                    self.greyLettersList.append(letter[0])
                elif letter[1] == 1 and (letter[0],index) not in self.yellowLettersAndIndexes: 
                    self.yellowLettersAndIndexes.append((letter[0],index))
                elif letter[1] == 0 and (letter[0],index) not in self.greenLettersAndIndexes:
                    self.greenLettersAndIndexes.append((letter[0], index))

                index += 1
            print(len(self.validWords))
            self.delete_grey_words()
            print(len(self.validWords))
            self.keep_yellow_words()
            print(len(self.validWords))
            self.keep_green_words()
            print(len(self.validWords))
    

    def delete_grey_words(self): # takes the list of currently valid words and removes all words with grey letters from it
        for word in self.validWords:
            for letter in self.greyLettersList:
                if letter in word:
                    self.validWords.remove(word)
                    break
                    



    def keep_yellow_words(self): # take the list of currently valid words and removes all
        for word in self.validWords:
            for letter in self.yellowLettersAndIndexes:
                if letter[0] not in word:
                    self.validWords.remove(word)
                    break
            



    def keep_green_words2(self):
        for word in self.validWords:
            for letter, index in self.greenLettersAndIndexes:
                if index < len(word) and word[index] != letter:
                    self.validWords.remove(word)
                    break
    
    def keep_green_words(self):
        new_valid_words = []
        for word in self.validWords:
            valid = True
            for letter, index in self.greenLettersAndIndexes:
                if index >= len(word) or word[index] != letter:
                    valid = False
                    break
            if valid:
                new_valid_words.append(word)
        self.validWords = new_valid_words
    
    def keepGreenWords(self):
        wordsToDelete = []
        for word in self.validWords:
            for letter, index in self.greenLettersAndIndexes:



