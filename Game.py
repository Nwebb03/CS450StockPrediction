import random

class Game:
    wordSet = set()
    filePath = ""
    secretWord = ""

    def fillSet(filePath):

        with open(filePath, 'r') as file:
            mySet = set()
            for line in file:
                words = line.split()  # Split the line into words
                mySet.update(words)  # Add the words to the set
        return mySet
    
    def setHiddenWord(wordSet):
        return random.choice(tuple(wordSet))
    
    def playGame():
        filePath = input("enter the filePath of the list of all words: ")
        wordSet = Game.fillSet(filePath)
        
