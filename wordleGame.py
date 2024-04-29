import random
import sys
import gameState
import wordleSolver
import string
import matplotlib.pyplot as plt

"""
Manages the Wordle game, allowing the player to interact with the game, make guesses, and optionally use the AI for assistance.
"""
class game:
    def __init__(self):
        """
        Initializes a game instance with a gameState object.
        """
        self.gameState = gameState.gameState()
    
    def fillWordLists(self):
        """
        Fill the validGuesses and validSolutions lists from external files.
        """
        with open('valid_guesses.txt', 'r') as validGuessesFile:
        # Read lines into a list and strip newline characters
            self.gameState.validGuesses = [line.strip() for line in validGuessesFile.readlines()]
        
        with open('valid_solutions.txt', 'r') as validSolutionsFile:
            self.gameState.validSolutions = [line.strip() for line in validSolutionsFile.readlines()]

    def setToList(wordSet):
        """
        Convert a word set to a list.

        Args:
            wordSet: Set of words

        Returns:
            List containing the words from the set
        """
        return list(wordSet)
    
    def setHiddenWord(self):
        """
        Randomly select secret word from validSolutions list

        Returns:
            Secret word
        """
        random_index = random.randint(a=0, b=(len(self.gameState.validSolutions) - 1))
        return self.gameState.validSolutions[random_index]


    
    def playGame(self, autoEnable):
        """
        Play the Wordle game.

        Args:
            autoEnable: Boolean indicating whether AI mode is enabled.

        Returns:
            Tuple containing the number of attempts, guesses, and the secret word.
        """
        valGuess = False
        self.fillWordLists()  # Fill word lists
        self.gameState.secretWord = self.setHiddenWord()  # set secret word
        #print(self.gameState.secretWord) - TESTING PURPOSES
        
        print("Welcome to wordle, would you like to use the AI Wordle Solver?")
        if autoEnable:
            wordleSolverEnableInput = 'y'  # Auto enable AI
        else:
            wordleSolverEnableInput = input("Y for yes, N for no: ").lower()
        
        # Validate user input for starting game
        while wordleSolverEnableInput not in ["y","n"]:
            wordleSolverEnableInput = input("Invalid input, type 'Y' for yes or 'N' for no: ").lower()
        
        if wordleSolverEnableInput == "y":
            wordleBot = wordleSolver.wordleSolver(gameState= self.gameState)    # Create a wordleSolver instance
            wordleSolverEnable = True
        else:
            wordleSolverEnable = False

        # Play while secret word has not been found
        while (self.gameState.wordFound == False) :
            valGuess = False
            if (self.gameState.attempts >= 6):  # If 6 attempts used, end game and reveal word
                print("You ran out of turns! The word was: ")
                print(self.gameState.secretWord)
                return (self.gameState.attempts, self.gameState.guesses)
            
            while (valGuess == False):
                if self.gameState.attempts == 1:
                    if wordleSolverEnable:
                        print("Here are the best guesses: ")   # Recommend best guesses based on potential entropy
                        with open('wordsAndEntropies.txt', 'r') as topEntropies:
                           topEntropies = [line.strip() for line in topEntropies.readlines()]
                        for entropyWord in topEntropies:
                            print(entropyWord)
                        if autoEnable:
                            self.userGuess = topEntropies[0][2:7:1]
                            print(self.userGuess)
                        else:
                            self.userGuess = input("Make a guess: ").lower()
                        
                else:
                    if wordleSolverEnable:
                        print("Here are the best next guesses: ")   # Recommend best guesses based on potential entropy
                        topEntropies = wordleBot.calculateTopNExpectedEntropies(10)
                        for entropyWord in topEntropies:
                            print(entropyWord)
                        if autoEnable:
                            self.userGuess = topEntropies[0][0]
                            print(self.userGuess)
                        else:
                            self.userGuess = input("Make another guess: ").lower()
                if self.userGuess == "quit":
                    exit()
                print()

                # Validate user guess to have 5 letters
                if ((len(self.userGuess) == 5 and (self.userGuess in self.gameState.validGuesses))
                    or (self.userGuess in self.gameState.validSolutions)):
                    valGuess = True
                else :
                    print("Invalid word, please enter a valid 5 letter word:")
            

            tempList = self.gameState.checkWord(self.gameState.secretWord,self.userGuess)
            #print(tempList) - TESTING PURPOSES
            self.gameState.updateGuesses( guess=self.userGuess, numList=tempList)

            # Update word lists if AI is enabled
            if wordleSolverEnable:
                #print(list(zip(self.userGuess, tempList))) - TESTING PURPOSES
                wordleBot.updateWordLists(list(zip(self.userGuess, tempList)))
            print("Results for attempt #", self.gameState.attempts, ", you have", 6 - self.gameState.attempts, "attempts left")
            print()

            if (self.gameState.attempts == 1):
                print("Resulting colors: (0 is grey, 1 is yellow and 2 is green) : ")   # explain rules after 1st guess so user can read feedback
                print()
            for guess in self.gameState.guesses:
                print(guess)
                print()
            print()

            if all(color == 2 for color in tempList):
                self.gameState.wordFound = True
                print("You guessed it the secret word was: ")   # Win statement
                print()
                print(self.gameState.secretWord)


            else :
                self.gameState.attempts += 1
        return (self.gameState.attempts, self.gameState.guesses, self.gameState.secretWord)
    
"""
Plots a graph of Letter frequencies in guesses and a graph of average number of guesses
"""
def displayGraphs():
    #Filter letter frequency to include only alphabetic characters
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


"""
Play the Wordle Game
"""
resultsSum = 0
gameResultsList = []
letter_freq = {}
autoEnable = False  # change to true if want to run games automatically

# Play the game x times and collect results
for i in range(1):
    game1 = game()
    gameResults = game1.playGame(autoEnable)
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

#Prompt user if they want to see graphical data; display graphs if auto
if (autoEnable):
    displayGraphs()
else:
    decision = input("Do you want to see the graphs of the letter frequency in guesses and the number of guesses? (Y/N): ").lower()
    if decision == 'y':
        displayGraphs()
