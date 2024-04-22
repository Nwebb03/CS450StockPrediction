import random
import sys
import gameState
import wordleSolver
import matplotlib.pyplot as plt

class game:
    def __init__(self):
        self.gameState = gameState.gameState()
    
    def fillWordLists(self):
        with open('valid_guesses.txt', 'r') as validGuessesFile:
        # Read lines into a list and strip newline characters
            self.gameState.validGuesses = [line.strip() for line in validGuessesFile.readlines()]
        
        with open('valid_solutions.txt', 'r') as validSolutionsFile:
            self.gameState.validSolutions = [line.strip() for line in validSolutionsFile.readlines()]

    def setToList(wordSet):
        return list(wordSet)
    
    def setHiddenWord(self):
        random_index = random.randint(a=0, b=(len(self.gameState.validSolutions) - 1))
        return self.gameState.validSolutions[random_index]


    
    def playGame(self, autoEnable):
        valGuess = False
        self.fillWordLists()
        self.gameState.secretWord = self.setHiddenWord()
        print(self.gameState.secretWord)
        
        print("Welcome to wordle, would you like to use the AI?")
        if autoEnable:
            wordleSolverEnableInput = 'y'
        else:
            wordleSolverEnableInput = input("Y for yes, N for no: ").lower()
        
        while wordleSolverEnableInput not in ["y","n"]:
            wordleSolverEnableInput = input("Invalid input input Y for yes or N for no").lower()
        
        if wordleSolverEnableInput == "y":
            wordleBot = wordleSolver.wordleSolver(gameState= self.gameState)
            wordleSolverEnable = True
        else:
            wordleSolverEnable = False

            
        while (self.gameState.wordFound == False) :
            valGuess = False
            if (self.gameState.attempts >= 6):
                print("you failed the word was: ")
                print(self.gameState.secretWord)
                return (self.gameState.attempts, self.gameState.guesses)
            
            while (valGuess == False):
                if self.gameState.attempts == 1:
                    if wordleSolverEnable:
                        print("Here are the top 10 best guesses")
                        with open('wordsAndEntropies.txt', 'r') as topEntropies:
                           topEntropies = [line.strip() for line in topEntropies.readlines()]
                        for entropyWord in topEntropies:
                            print(entropyWord)
                        if autoEnable:
                            print("hello")
                            self.userGuess = topEntropies[0][2:7:1]
                            print(self.userGuess)
                        else:
                            self.userGuess = input("Make a guess: ").lower()
                        
                else:
                    if wordleSolverEnable:
                        print("Here are the top 10 best guesses")
                        topEntropies = wordleBot.calculateTopNExpectedEntropies(10)
                        for entropyWord in topEntropies:
                            print(entropyWord)
                        if autoEnable:
                            print("hello")
                            self.userGuess = topEntropies[0][0]
                            print(self.userGuess)
                        else:
                            self.userGuess = input("Make another guess: ").lower()
                if self.userGuess == "quit":
                    exit()
                print()


                if ((len(self.userGuess) == 5 and (self.userGuess in self.gameState.validGuesses))
                    or (self.userGuess in self.gameState.validSolutions)):
                    valGuess = True
                else :
                    print("Word invalid, enter a 5 letter word in the valid guesses")
            


            tempList = self.gameState.checkWord(self.gameState.secretWord,self.userGuess)
            print(tempList)
            self.gameState.updateGuesses( guess=self.userGuess, numList=tempList)




            if wordleSolverEnable:
                print(list(zip(self.userGuess, tempList)))
                wordleBot.updateWordLists(list(zip(self.userGuess, tempList)))
            print("Results for attempt #", self.gameState.attempts, ", you have", 6 - self.gameState.attempts, "attempts left")
            print()
            if (self.gameState.attempts == 0):
                print("Resulting colors: (0 is grey, 1 is yellow and 2 is green) : ")
                print()
            for guess in self.gameState.guesses:
                print(guess)
                print()
            print()
            if all(color == 2 for color in tempList):
                self.gameState.wordFound = True
                print("You guessed it the secret word was: ")
                print()
                print(self.gameState.secretWord)

            else :
                self.gameState.attempts += 1
        return (self.gameState.attempts, self.gameState.guesses, self.gameState.secretWord)
        '''
        print("Secret word is: {}".format(self.gameState.secretWord))

        guess = "dream"
        self.checkWord(guess)\
        print(game1.gameState.guesses)
        self.checkWord("chart")
        print(game1.gameState.guesses)
        self.checkWord("ranch")\
        print(game1.gameState.guesses)
        '''




            
       


    

resultsSum = 0
gameResultsList = []
letter_freq = {}

# Play the game 10 times and collect results
for i in range(1000):
    game1 = game()
    gameResults = game1.playGame(autoEnable=True)
    gameResultsList.append(gameResults)

    # Calculate letter frequencies for each game
    for guess in gameResults[1]:  # gameResults[1] contains guesses
        for letter in guess[0]:  # guess[0] contains the guessed word
            letter_freq[letter] = letter_freq.get(letter, 0) + 1

    # Add the number of attempts for this game to resultsSum
    resultsSum += gameResults[0]

for i, gameResults in enumerate(gameResultsList):
    print(f"Game {i + 1}: guessed ", end="")
    for guess in gameResults[1][-1]:
        print(guess[0], end="")
    print(" in", gameResults[0], "attempts")

# Print average number of attempts
print("Average number of attempts:", resultsSum / 1000)

import string

# Filter letter frequency to include only alphabetic characters
filtered_letter_freq = {str(key): value for key, value in letter_freq.items() if isinstance(key, str) and key.isalpha()}

# Sort letter frequencies alphabetically
sorted_filtered_letter_freq = sorted(filtered_letter_freq.items())

# Convert keys and values to lists of strings
keys = [char for char, _ in sorted_filtered_letter_freq]
vals = [freq for _, freq in sorted_filtered_letter_freq]

plt.bar(keys, vals)
plt.xlabel('Letters')
plt.ylabel('Frequency')
plt.title('Letter Frequency in Guesses')
plt.show()

num_guesses = [gameResults[0] for gameResults in gameResultsList]

# Plot histogram
plt.hist(num_guesses, bins=range(min(num_guesses), max(num_guesses) + 1), edgecolor='black')
plt.xlabel('Number of Guesses')
plt.ylabel('Frequency')
plt.title('Histogram of Number of Guesses')
plt.show()
