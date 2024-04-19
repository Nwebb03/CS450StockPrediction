class ListUpdater:
    @staticmethod
    def delete_grey_words(word_list, grey_list):
        for word in word_list.copy():
            for letter in grey_list:
                if letter in word:
                    word_list.remove(word)
                    break

    @staticmethod
    def keep_yellow_words(word_list, yellow_list):
        for word in word_list.copy():
            for letter in yellow_list:
                if letter not in word:
                    word_list.remove(word)
                    break

    @staticmethod
    def keep_green_words(word_list, green_list, index_list):
        for word in word_list.copy():
            for letter, index in zip(green_list, index_list):
                if index < len(word) and word[index] != letter:
                    word_list.remove(word)
                    break

    @staticmethod
    def is_char_in_string(char, string):
        return char in string

    @staticmethod
    def is_char_in_pos(char, i, string):
        return i < len(string) and string[i] == char
