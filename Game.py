import random

class Game:
    wordSet = set()
    filePath = ""
    secretWord = ""

    def fillSet(filePath):

      
    def setHiddenWord(wordSet):
        return random.choice(tuple(wordSet))
    
    def playGame():
        filePath = input("enter the filePath of the list of all words: ")
        wordSet = Game.fillSet(filePath)
        
