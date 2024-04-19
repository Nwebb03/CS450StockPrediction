class entropy
  def getPossibleWords(wordList, char, i):
    possibleWords = []
    for string in wordList:
        if entropy.isCharInString(char,string): # idk if this line is neccesary
          if entropy.isCharInPos(char, i, string)
            possibleWords.append(string)
    return possibleWords
    
  def isCharInString(char,string):
    return char in string

  def isCharInPos(char, i, string):
    return string[i] == char and i < len(String)
