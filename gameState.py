"""
Manages state and logic of the Wordle Game
"""
class gameState:

    def __init__(self) -> None:
        """
        Initializes the game state with default values.
        """
        self.guesses = []   # List to store guessed words and their feedback
        self.secretWord = ""    # secret word to be guessed
        self.wordFound = False  # true if secret word is found
        self.attempts = 1   # counter for number of guesses used
        self.userGuess = "" # current guess
        self.validGuesses = []  # List of valid guesses
        self.validSolutions = []  # List of valid solutions
        self.invalidChars = []  # invalid characters


    
    def updateGuesses(self, guess, numList):
        """
        Updates list of guesses with latest guess and feedback.

        Args:
            guess: guessed word
            numList: List with feedback from guessed word
        """
        self.guesses.append(list(zip(guess, numList)))

    def checkWord2(self,guess):
        """
        Checks to see if guessed word is secret word and generates feedback

        Args:
            guess: guessed word

        Returns:
            List with feedback for guessed word
        """
        numList = []  # feedback list
        
        for i in range(5):
            found = False;
            for j in range(5):
                if (self.secretWord[j] == guess[i]):
                    if (j == i):
                        numList.append(2)  # Correct letter, correct position - Green ('2')
                        found = True
                        break
                    else:
                        numList.append(1)  # Correct letter, wrong position - Yellow ('1')
                        found = True
                        break
            if (found == False):
                numList.append(0)  # Incorrect letter - Grey ('0')
        return numList
    

    def checkWord(self, secretWord, guess):
        numList = [0] * 5  # Initialize all to '0' (grey)
        used_indices = set()  # To track indices already matched exactly or as partial matches

        # First pass: check for exact matches
        for i in range(5):
            if guess[i] == secretWord[i]:
                numList[i] = 2
                used_indices.add(i)  # Mark this index as used

        # Second pass: check for partial matches
        for i in range(5):
            if numList[i] == 0:  # Only consider this if it's not an exact match
                for j in range(5):
                    if guess[i] == secretWord[j] and j not in used_indices:
                        numList[i] = 1  # Correct letter, wrong place
                        used_indices.add(j)  # Mark this index as used
                        break  # Break after the first unused match

        return numList

    
