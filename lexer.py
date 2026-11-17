from pointer import PointerClass
from enum import Enum, auto


class TokenType(Enum):
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


class Token:
    token_type: TokenType
    content: str

    def __init__(self, token_type: TokenType, content: str) -> None:
        self.token_type = token_type
        self.content = content

    def __repr__(self) -> str:
        return f"{self.token_type.name}<{self.content}>"


class Lexer(PointerClass[str]):
    def __init__(self, items: str) -> None:
        super().__init__(items)

    def tokenize(self) -> list[Token]:
        tokens: list[Token] = []
        while (c := self.consume()):
            if c == "=":
                tokens.append(Token(TokenType.EQUALS, c))
            elif c == "-":
                tokens.append(Token(TokenType.MINUS, c))
            elif c == " ":
                tokens.append(Token(TokenType.SPACE, c))
            elif c == "\n":
                tokens.append(Token(TokenType.NEWLINE, c))
            elif c.isalpha():
                buffer = c
                while (c := self.peek()) and c.isalpha():
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
                else:
                    tokens.append(Token(TokenType.TEXT, buffer))
            elif c.isdigit():
                buffer = c
                while (c := self.peek()) and c.isdigit():
                    buffer += c
                    self.consume()
                tokens.append(Token(TokenType.NUMBER, buffer))
            else:
                raise SyntaxError(f"Unexpected character '{c}'")
        return tokens
