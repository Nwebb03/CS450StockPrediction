class gameState:

    def __init__(self) -> None:
        self.guesses = []
        self.secretWord = ""
        self.wordFound = False
        self.attempts = 1
        self.userGuess = ""
        self.validGuesses = []
        self.validSolutions = []
        self.invalidChars = []


    
    def updateGuesses(self, guess, numList):
        self.guesses.append(list(zip(guess, numList)))

    def checkWord2(self,guess):
        numList = []
        
        for i in range(5):
            found = False;
            for j in range(5):
                if (self.secretWord[j] == guess[i]):
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

    