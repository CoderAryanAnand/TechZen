class Position:
    def __init__(self, idx, ln, col, fn, ftxt):
        """
        This class gives the position of each token / character in the code.
        :param idx: The index of the character
        :param ln: The line of the character
        :param col: The column of the character
        :param fn: The file name of the character
        :param ftxt: The text of the file
        """
        self.idx = idx
        self.ln = ln
        self.col = col
        self.fn = fn
        self.ftxt = ftxt

    def advance(self, current_char=None):
        """
        Advance to the next character.
        :param current_char: Newline otherwise none
        :return: Position
        """
        self.idx += 1
        self.col += 1

        if current_char == "\n":
            self.ln += 1
            self.col = 0

        return self

    def copy(self):
        """
        Create a copy of the position.
        :return: Position copy
        """
        return Position(self.idx, self.ln, self.col, self.fn, self.ftxt)
