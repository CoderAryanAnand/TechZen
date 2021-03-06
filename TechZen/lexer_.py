from TechZen.token_ import (
    Token,
    TokenType,
    KEYWORDS,
    DIGITS,
    LETTERS,
    SKIP_LETTERS,
    COMMENT_SYMBOL,
    SYMBOL_TO_TOKENS,
)
from TechZen.position_ import Position
from TechZen.errors_ import IllegalCharError, ExpectedCharError


LETTERS_DIGITS = LETTERS + DIGITS


class Lexer:
    def __init__(self, fn, text):
        """
        This is the lexer of the language. It takes in an input and figures out what each character/word stands for
        (Token).
        :param fn: File name of input
        :param text: Input to make tokens out of
        """
        self.fn = fn
        self.text = text
        self.pos = Position(-1, 0, -1, fn, text)
        self.current_char = None
        self.advance()

    def advance(self):
        """
        Advance to the next character
        :return: nothing
        """
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    def make_tokens(self):  # sourcery no-metrics
        """
        Makes tokens from the input.
        :return: The input in token format, if there is an error, then the error
        """
        tokens = []

        while self.current_char is not None:
            if self.current_char in SKIP_LETTERS:
                self.advance()
            elif self.current_char == COMMENT_SYMBOL:
                self.skip_comment()
            elif self.current_char in DIGITS:
                tokens.append(self.make_number())
            elif self.current_char in LETTERS:
                tokens.append(self.make_identifier())
            elif self.current_char in SYMBOL_TO_TOKENS:
                tokens.append(
                    Token(SYMBOL_TO_TOKENS[self.current_char], pos_start=self.pos)
                )
                self.advance()
            elif self.current_char in ('"', "'"):
                tokens.append(self.make_string(self.current_char))
            elif self.current_char == "-":
                tokens.append(self.make_minus_or_arrow())
                self.advance()
            elif self.current_char == "/":
                tokens.append(self.make_division())
            elif self.current_char == "!":
                token, error = self.make_not_equals()
                if error:
                    return [], error
                tokens.append(token)
            elif self.current_char == "=":
                tokens.append(self.make_equals())
            elif self.current_char == "<":
                tokens.append(self.make_less_than())
            elif self.current_char == ">":
                tokens.append(self.make_greater_than())
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, "'" + char + "'")

        tokens.append(Token(TokenType.TT_EOF, pos_start=self.pos))
        return tokens, None

    def make_number(self):
        """
        Decides whether number is an integer or a floating point.
        :return: Integer or floating point
        """
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char is not None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                if dot_count == 1:
                    break
                dot_count += 1
                num_str += "."
            else:
                num_str += self.current_char
            self.advance()

        if dot_count == 0:
            return Token(TokenType.TT_INT, int(num_str), pos_start, self.pos)
        else:
            return Token(TokenType.TT_FLOAT, float(num_str), pos_start, self.pos)

    def make_string(self, qt):
        """
        Adds escape characters and characters until it finds a quote.
        :param qt: Quote type " or '
        :return:
        """
        string = ""
        pos_start = self.pos.copy()
        escape_character = False
        self.advance()

        escape_characters = {"n": "\n", "t": "\t", "r": "\r", "v": "\v", "0": "\0"}

        while self.current_char is not None and (
            self.current_char != qt or escape_character
        ):
            if escape_character:
                string += escape_characters.get(self.current_char, self.current_char)
                escape_character = False
            elif self.current_char == "\\":
                escape_character = True
            else:
                string += self.current_char
            self.advance()

        self.advance()
        return Token(TokenType.TT_STRING, string, pos_start, self.pos)

    def make_identifier(self):
        """
        Finds out if a token is an identifier or a keyword.
        :return: Token - KEYWORD or IDENTIFIER
        """
        id_str = ""
        pos_start = self.pos.copy()

        while (
            self.current_char is not None and self.current_char in LETTERS_DIGITS + "_"
        ):
            id_str += self.current_char
            self.advance()

        token_type = (
            TokenType.TT_KEYWORD
            if id_str.upper() in KEYWORDS
            else TokenType.TT_IDENTIFIER
        )
        return Token(token_type, id_str, pos_start, self.pos)

    def make_minus_or_arrow(self):
        """
        Decides if the minus is a minus or an arrow.
        :return: Token - MINUS or ARROW
        """
        token_type = TokenType.TT_MINUS
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == ">":
            self.advance()
            token_type = TokenType.TT_ARROW

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_not_equals(self):
        """
        Makes the not equals token.
        :return: Token or error
        """
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            return Token(TokenType.TT_NE, pos_start=pos_start, pos_end=self.pos), None

        self.advance()
        return None, ExpectedCharError(pos_start, self.pos, "'=' (after '!')")

    def make_division(self):
        """
        Decides if "/" is a division or a floor.
        :return: Token - DIV or DFL
        """
        token_type = TokenType.TT_DIV
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "/":
            self.advance()
            token_type = TokenType.TT_DFL

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_equals(self):
        """
        Decides if "=" is an equal sign or an is equal sign.
        :return: Token - EQUALS or IS_EQUAL
        """
        token_type = TokenType.TT_EQ
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TokenType.TT_EE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_less_than(self):
        """
        Decides if "<" is less than or less than or equal to.
        :return: Token - LESS_THAN or LESS_THAN_OR_EQUAL
        """
        token_type = TokenType.TT_LT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TokenType.TT_LTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def make_greater_than(self):
        """
        Decides if ">" is greater than or greater than or equal to.
        :return: Token - GREATER_THAN or GREATER_THAN_OR_EQUAL
        """
        token_type = TokenType.TT_GT
        pos_start = self.pos.copy()
        self.advance()

        if self.current_char == "=":
            self.advance()
            token_type = TokenType.TT_GTE

        return Token(token_type, pos_start=pos_start, pos_end=self.pos)

    def skip_comment(self):
        """
        Skips all comments, even multiline comments.
        :return: nothing
        """
        pos_start = self.pos.copy()
        self.advance()
        if self.current_char == "[":
            self.advance()
            while self.current_char != "]":
                self.advance()
            self.advance()
            if self.current_char != "#":
                return (
                    None,
                    ExpectedCharError(
                        pos_start,
                        self.pos,
                        "While making multiline comment, a '#' (Hash sign) is expected after a ']' (Square bracket)",
                    ),
                )
            while self.current_char != "\n":
                self.advance()
        self.advance()
