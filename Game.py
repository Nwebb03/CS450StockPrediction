import random

class Game:
    wordList = []
    filePath = ""
    secretWord = ""
    wordFound = False
    
    def fillSet(filePath):
        wordSet = set()
        return wordSet
    
    def setToList(wordSet):
        return list(wordSet)
    
    def setHiddenWord(wordList):
        random_index = random.randint(0, (wordList.length()) - 1)
        return wordList[random_index]
    
    def playGame():
        filePath = input("enter the filePath of the list of all words: ")
        wordSet = Game.fillSet(filePath)
        wordList = Game.setToList(wordSet)
        secretWord = Game.setHiddenWord(wordList)

        while (wordFound == False) {
            
        }

class gamestate:
    
