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
        self.validWords = gameState.validSolutions  ##+ gameState.validGuesses
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
                elif letter[1] == 2 and (letter[0],index) not in self.greenLettersAndIndexes:
                    self.greenLettersAndIndexes.append((letter[0], index))

                index += 1
            print(len(self.validWords))
            self.deleteGreyWords()
            print(len(self.validWords))
            self.keepYellowWords()
            print(len(self.validWords))
            self.keepGreenWords()
            print(len(self.validWords))
    

    def deleteGreyWords(self): # takes the list of currently valid words and removes all words with grey letters from it
        greyWordsToRemove = []
        for word in self.validWords:
            for letter in self.greyLettersList:
                if letter in word:
                    greyWordsToRemove.append(word)
                    break
                    

        for word in greyWordsToRemove:
            self.validWords.remove(word)

    def keepYellowWords(self): # take the list of currently valid words and removes all
        yellowWordsToRemove = []
        for word in self.validWords:
            containsYellow = False
            for letter,_ in self.yellowLettersAndIndexes:
                if letter in word:
                    containsYellow = True
                    break
            if containsYellow == False:
                yellowWordsToRemove.append(word)
            
        for word in self.validWords:
            for letter, index in self.yellowLettersAndIndexes:
                if (letter in word) and (word.find(letter) == index):
                    yellowWordsToRemove.append(word)
                    break
        

        for word in yellowWordsToRemove:
            self.validWords.remove(word)
        
      



    
    def keepGreenWords1(self):
        for word in self.validWords:
            for letter, index in self.greenLettersAndIndexes:
                if index < len(word) and word[index] != letter:
                    self.validWords.remove(word)
                    break
    
    def keepGreenWords(self):
    
        
        greenWordsToRemove = []
        for word in self.validWords:
            for letter,_ in self.greenLettersAndIndexes:
                if letter not in word:
                    greenWordsToRemove.append(word)
                    break
                    

        for word in greenWordsToRemove:
            self.validWords.remove(word)
    
    '''
    def keepGreenWords2(self):
        wordsToDelete = []
        for word in self.validWords:
            for letter, index in self.greenLettersAndIndexes:
    '''


