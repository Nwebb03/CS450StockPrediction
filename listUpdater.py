class ListUpdater: # use the methods in this class to update the list of possible solutions ONLY, don't call on anything else
                   # gameState = 2d tuple containing word_list green_list, index_list, yellow_list, grey_list
    @staticmethod
    def updateValidWordsList():
        delete_grey_words()
        keep_yellow_words()
        keep_grey_words()
    
    @staticmethod
    def delete_grey_words(): # takes the list of currently valid words and removes all words with grey letters from it
        for word in gameState.word_list.copy():
            for letter in gameState.grey_list:
                if letter in word:
                    gameState.word_list.remove(word)
                    break

    @staticmethod
    def keep_yellow_words(): # take the list of currently valid words and removes all
        for word in gameState.word_list.copy():
            for letter in gameState.yellow_list:
                if letter not in word:
                    gameState.word_list.remove(word)
                    break

    @staticmethod
    def keep_green_words():
        for word in gameState.word_list.copy():
            for letter, index in zip(gameState.green_list, gameState.index_list):
                if index < len(word) and word[index] != letter:
                    gameState.word_list.remove(word)
                    break

    @staticmethod
    def is_char_in_string(char, string):
        return char in string

    @staticmethod
    def is_char_in_pos(char, i, string):
        return i < len(string) and string[i] == char
