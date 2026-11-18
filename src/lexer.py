"""Lexer module to turn source code to tokens.

Lexer class does the conversion with the tokenize method. Token class represents
tokens.

Typical usage:
    tokens = Lexer(source_code).tokenize()
"""

from src.pointer import PointerClass
from enum import Enum, auto


class TokenType(Enum):
    """Type of the token.

    Values are automatically generated integers.
    """
    LET = auto()
    PRINT = auto()
    EQUALS = auto()
    TEXT = auto()
    NUMBER = auto()
    MINUS = auto()
    SPACE = auto()
    NEWLINE = auto()
    INC = auto()
    DEC = auto()
    LABEL = auto()
    GOTO = auto()
    JUMP = auto()
    IF = auto()


class Token:
    """Token representation.

    Attributes:
        token_type(TokenType): Type of the token.
        content(str): The string in the source code that this token represents.
    """
    token_type: TokenType
    content: str

    def __init__(self, token_type: TokenType, content: str) -> None:
        """Initializes a token.

        Args:
            token_type(TokenType): Type of the token.
            content(str): The string in the source code that this token 
              represents.
        """
        self.token_type = token_type
        self.content = content

    def __repr__(self) -> str:
        """Returns the string representation of the token.
        """
        return f"{self.token_type.name}<{self.content}>"


class Lexer(PointerClass[str]):
    """Lexer turns source code to tokens.

    Attributes:
        items(str): The source code as a string.
    """

    def __init__(self, items: str) -> None:
        """Initializes the Lexer object.

        Parameters:
            items(str): The source code as a string.
        """
        super().__init__(items)

    def tokenize(self) -> list[Token]:
        """Turn the source code to tokens.

        Returns:
            tokens(list[Token]): A list of tokens representing the source code.
        """
        tokens: list[Token] = []
        while (c := self.consume()):
            # Single character tokens
            if c == "=":
                tokens.append(Token(TokenType.EQUALS, c))
            elif c == "-":
                tokens.append(Token(TokenType.MINUS, c))
            elif c == " ":
                tokens.append(Token(TokenType.SPACE, c))
            elif c == "\n":
                tokens.append(Token(TokenType.NEWLINE, c))
            # Text and keyword tokens
            elif c.isalpha():
                buffer = c
                while (c := self.peek()) and c.isalnum():
                    buffer += c
                    self.consume()
                if buffer == "LET":
                    tokens.append(Token(TokenType.LET, buffer))
                elif buffer == "PRINT":
                    tokens.append(Token(TokenType.PRINT, buffer))
                elif buffer == "INC":
                    tokens.append(Token(TokenType.INC, buffer))
                elif buffer == "DEC":
                    tokens.append(Token(TokenType.DEC, buffer))
                elif buffer == "LABEL":
                    tokens.append(Token(TokenType.LABEL, buffer))
                elif buffer == "GOTO":
                    tokens.append(Token(TokenType.GOTO, buffer))
                elif buffer == "JUMP":
                    tokens.append(Token(TokenType.JUMP, buffer))
                elif buffer == "IF":
                    tokens.append(Token(TokenType.IF, buffer))
                else:
                    tokens.append(Token(TokenType.TEXT, buffer))
            # Number token
            elif c.isdigit():
                buffer = c
                while (c := self.peek()) and c.isdigit():
                    buffer += c
                    self.consume()
                tokens.append(Token(TokenType.NUMBER, buffer))
            else:
                raise SyntaxError(f"Unexpected character '{c}'")
        return tokens
