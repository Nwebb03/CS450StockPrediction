import random

class Game:
    def __init__(self):
        self.wordList = []
        self.filePath = ""
        self.secretWord = ""
        self.wordFound = False
        self.attempts = 0
        self.userGuess = ""
    
    
    def fillSet(filePath):
        wordSet = set()
        return wordSet
    
    def setToList(wordSet):
        return list(wordSet)
    
    def setHiddenWord(wordList):
        random_index = random.randint(0, (wordList.length()) - 1)
        return wordList[random_index]
    
    def checkWord(guess):
        numList = []
        for i in guess:
            for 
    
    def playGame(self):
        self.filePath = input("enter the filePath of the list of all words: ")
        wordSet = Game.fillSet(self.filePath)
        self.wordList = Game.setToList(wordSet)
        self.secretWord = Game.setHiddenWord(self.wordList)
        valGuess = False

        while (self.wordFound == False & self.attempts < 6) :
            while (valGuess == False) :
                self.userGuess = input("make a guess: ") 
                if (len(self.userGuess) == 5):
                    valGuess = True
            
            



            
        

class gamestate:
    
