import random
import sys
import csv

class Game:
    def __init__(self):
        self.wordList = []
        self.filePath = ""
        self.wordList = []
        self.gamestate = gamestate()
    
    def fillwordLists(self):
        with open('valid_guesses.txt', 'r') as validGuessesFile:
        # Read lines into a list and strip newline characters
            self.gamestate.validGuesses = [line.strip() for line in validGuessesFile.readlines()]
        
        with open('valid_solutions.txt', 'r') as validSolutionsFile:
            self.gamestate.validSolutions = [line.strip() for line in validSolutionsFile.readlines()]

    def setToList(wordSet):
        return list(wordSet)
    
    def setHiddenWord(self):
        random_index = random.randint(a=0, b=(len(self.gamestate.validSolutions) - 1))
        return self.gamestate.validSolutions[random_index]
    
    def checkWord(self,guess):
        numList = []
        
        for i in range(5):
            found = False;
            for j in range(5):
                if (self.gamestate.secretWord[j] == guess[i]):
                    if (j == i):
                        numList.append(2)
                        found = True
                        break
                    else:
                        numList.append(1)
                        found = True
                        break
            if (found == False):
                numList.append(0)
        self.gamestate.updateGuesses(guess, numList)
        return numList


    
    def playGame(self):
        ##self.filePath = input("enter the filePath of the list of all words: ")
        ##wordSet = Game.fillSet(self.filePath)
        ##self.wordList = Game.setToList(wordSet)
        ##self.secretWord = Game.setHiddenWord(self.wordList)
        valGuess = False
        self.fillwordLists()
        self.gamestate.secretWord = self.setHiddenWord()
        print(self.gamestate.secretWord)
        
        while (self.gamestate.wordFound == False) :
            valGuess = False
            if (self.gamestate.attempts > 5):
                print("you failed the word was: ")
                print(self.gamestate.secretWord)
                sys.exit()
            
            while (valGuess == False) :
                self.userGuess = input("make a guess: ") 
                if self.userGuess == "quit":
                    exit()
                print()
                if (len(self.userGuess) == 5 and (self.userGuess in self.gamestate.validGuesses) 
                    or (self.userGuess in self.gamestate.validSolutions)):
                    valGuess = True
                else :
                    print("word invalid, enter a 5 letter word in the valid guesses")
            
            tempList = self.checkWord(self.userGuess)
            print("Results for attempt #", self.gamestate.attempts, ", you have", 6 - self.gamestate.attempts, "attempts left")
            print()
            if (self.gamestate.attempts == 0):
                print("resulting colors: (0 is grey, 1 is yellow and 2 is green) : ")
                print()
            print(self.gamestate.guesses[self.gamestate.attempts])
            print()
            if all(color == 2 for color in tempList):
                self.gamestate.wordFound = True
                print("you guessed it the secret word was: ")
                print()
                print(self.gamestate.secretWord)

            else :
                self.gamestate.attempts += 1
        '''
        print("Secret word is: {}".format(self.gamestate.secretWord))

        guess = "dream"
        self.checkWord(guess)
        print(game1.gamestate.guesses)
        self.checkWord("chart")
        print(game1.gamestate.guesses)
        self.checkWord("ranch")
        print(game1.gamestate.guesses)
        '''




            
       

class gamestate:

    def __init__(self) -> None:
        self.guesses = []
        self.secretWord = ""
        self.wordFound = False
        self.attempts = 0
        self.userGuess = ""
        self.validGuesses = []
        self.validSolutions = []
        self.invalidChars = []

    
    def updateGuesses(self,guess, numList):
        self.guesses.append(list(zip(guess, numList)))
    

game1 = Game()
game1.playGame()
