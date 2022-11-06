#######################################
# TOKENS
#######################################
from enum import Enum
import string

DIGITS = "0123456789"
LETTERS = string.ascii_letters
SKIP_LETTERS = " \t"
NEW_LINES = ";\n"
COMMENT_SYMBOL = "#"


class TokenType(Enum):
    TT_INT = "INT"
    TT_FLOAT = "FLOAT"
    TT_STRING = "STRING"
    TT_IDENTIFIER = "IDENTIFIER"
    TT_KEYWORD = "KEYWORD"
    TT_PLUS = "PLUS"
    TT_MINUS = "MINUS"
    TT_MUL = "MUL"
    TT_DIV = "DIV"
    TT_DFL = "DFL"
    TT_POW = "POW"
    TT_MOD = "MOD"
    TT_EQ = "EQ"
    TT_LPAREN = "LPAREN"
    TT_RPAREN = "RPAREN"
    TT_LSQUARE = "LSQUARE"
    TT_RSQUARE = "RSQUARE"
    TT_LCURLY = "LCURLY"
    TT_RCURLY = "RCURLY"
    TT_COLON = "COLON"
    TT_EE = "EE"
    TT_NE = "NE"
    TT_LT = "LT"
    TT_GT = "GT"
    TT_LTE = "LTE"
    TT_GTE = "GTE"
    TT_COMMA = "COMMA"
    TT_ARROW = "ARROW"
    TT_NEWLINE = "NEWLINE"
    TT_DOT = "DOT"
    TT_EOF = "EOF"

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self)


SYMBOL_TO_TOKENS = {
    "+": TokenType.TT_PLUS,
    "*": TokenType.TT_MUL,
    "^": TokenType.TT_POW,
    "%": TokenType.TT_MOD,
    "(": TokenType.TT_LPAREN,
    ")": TokenType.TT_RPAREN,
    "[": TokenType.TT_LSQUARE,
    "]": TokenType.TT_RSQUARE,
    "{": TokenType.TT_LCURLY,
    "}": TokenType.TT_RCURLY,
    ",": TokenType.TT_COMMA,
    ";": TokenType.TT_NEWLINE,
    ":": TokenType.TT_COLON,
    ".": TokenType.TT_DOT,
    "\n": TokenType.TT_NEWLINE,
}


class Keywords(Enum):
    KW_VAR = "VAR"
    KW_AND = "AND"
    KW_OR = "OR"
    KW_NOT = "NOT"
    KW_IF = "IF"
    KW_ELIF = "ELIF"
    KW_ELSE = "ELSE"
    KW_FOR = "FOR"
    KW_TO = "TO"
    KW_STEP = "STEP"
    KW_WHILE = "WHILE"
    KW_FUN = "FUN"
    KW_THEN = "THEN"
    KW_END = "END"
    KW_ENDF = "ENDF"
    KW_ENDC = "ENDC"
    KW_RETURN = "RETURN"
    KW_CONTINUE = "CONTINUE"
    KW_BREAK = "BREAK"
    KW_CLASS = "CLASS"
    KW_TRY = "TRY"
    KW_EXCEPT = "EXCEPT"
    KW_INCLUDE = "INCLUDE"

    def __str__(self):
        return str(self.value)


KEYWORDS = {
    Keywords.KW_VAR.value: Keywords.KW_VAR,
    Keywords.KW_AND.value: Keywords.KW_AND,
    Keywords.KW_OR.value: Keywords.KW_OR,
    Keywords.KW_NOT.value: Keywords.KW_NOT,
    Keywords.KW_IF.value: Keywords.KW_IF,
    Keywords.KW_ELIF.value: Keywords.KW_ELIF,
    Keywords.KW_ELSE.value: Keywords.KW_ELSE,
    Keywords.KW_FOR.value: Keywords.KW_FOR,
    Keywords.KW_TO.value: Keywords.KW_TO,
    Keywords.KW_STEP.value: Keywords.KW_STEP,
    Keywords.KW_WHILE.value: Keywords.KW_WHILE,
    Keywords.KW_FUN.value: Keywords.KW_FUN,
    Keywords.KW_THEN.value: Keywords.KW_THEN,
    Keywords.KW_END.value: Keywords.KW_END,
    Keywords.KW_ENDF.value: Keywords.KW_ENDF,
    Keywords.KW_ENDC.value: Keywords.KW_ENDC,
    Keywords.KW_RETURN.value: Keywords.KW_RETURN,
    Keywords.KW_CONTINUE.value: Keywords.KW_CONTINUE,
    Keywords.KW_BREAK.value: Keywords.KW_BREAK,
    Keywords.KW_CLASS.value: Keywords.KW_CLASS,
    Keywords.KW_TRY.value: Keywords.KW_TRY,
    Keywords.KW_EXCEPT.value: Keywords.KW_EXCEPT,
    Keywords.KW_INCLUDE.value: Keywords.KW_INCLUDE,
}


class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        """
        This is the token class. It defines the token and its values.
        :param type_: The TokenType
        :param value: Value of the token
        :param pos_start: Start position of the token
        :param pos_end: End position of the token
        """
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end.copy()

    def matches(self, type_, value):
        """
        Find if token type matches the value
        :param type_: TokenType
        :param value: value
        :return: TokenType == value
        """
        return self.type == type_ and self.value.upper() == value

    def __repr__(self):
        if self.value:
            return f"{self.type}:{self.value}"
        return f"{self.type}"
