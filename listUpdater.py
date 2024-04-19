class listUpdater:
  def deleteGreyWords(wordList, greyList):
    for word in worldList:
      for letter in greyList:
        if isCharInString(letter,word):
          wordList.remove(word)
  def keepYellowWords(wordList, yellowList):
    for word in worldList:
      for letter in greyList:
        if not isCharInString(letter,word):
          wordList.remove(word)
  def keepGreenWords(wordList, greenList, indexList):
    for word in WordList:
        for letter, index in zip(greenList, indexList):
          if not isCharInPos(letter, index, word):
            wordList.remove(word)
  def isCharInString(char,string):
    return char in string

  def isCharInPos(char, i, string):
    return string[i] == char and i < len(String)
