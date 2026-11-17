from typing import Sequence
from pointer import PointerClass
from lexer import Token, TokenType


class Expression:
    pass


class IntLiteral(Expression):
    num: int

    def __init__(self, num: int) -> None:
        super().__init__()
        self.num = num


class VariableRef(Expression):
    var_name: str

    def __init__(self, var_name: str) -> None:
        super().__init__()
        self.var_name = var_name


class Instruction:
    pass


class PrintInst(Instruction):
    value: Expression

    def __init__(self, value: Expression) -> None:
        super().__init__()
        self.value = value


class LetInst(Instruction):
    var: VariableRef
    value: Expression

    def __init__(self, var: VariableRef, value: Expression) -> None:
        super().__init__()
        self.var = var
        self.value = value


class IncInst(Instruction):
    var: VariableRef
    value: Expression

    def __init__(self, var: VariableRef, value: Expression) -> None:
        super().__init__()
        self.var = var
        self.value = value


class DecInst(Instruction):
    var: VariableRef
    value: Expression

    def __init__(self, var: VariableRef, value: Expression) -> None:
        super().__init__()
        self.var = var
        self.value = value


class GotoInst(Instruction):
    label: str

    def __init__(self, label: str) -> None:
        super().__init__()
        self.label = label


class JumpInst(Instruction):
    label: str
    condition: Expression

    def __init__(self, label: str, condition: Expression) -> None:
        super().__init__()
        self.label = label
        self.condition = condition


class Program:
    instructions: list[Instruction]
    labels: dict[str, int]

    def __init__(self) -> None:
        self.instructions = []
        self.labels = {}


class Parser(PointerClass[Token]):
    def __init__(self, items: Sequence[Token]) -> None:
        super().__init__(items)

    def consume_whitespace(self) -> None:
        while (t := self.peek()) and t.token_type in [TokenType.SPACE, TokenType.NEWLINE]:
            self.consume()

    def check_token_type(self, token_type: TokenType,  token: Token | None = None):
        if token is None:
            token = self.peek()
        return token is not None and token.token_type == token_type

    def collect_tokens(self, end: TokenType | None = None) -> list[Token]:
        tokens: list[Token] = []
        while (t := self.peek()) and t.token_type != end:
            tokens.append(t)
            self.consume()
        return tokens

    def parse_expression(self) -> Expression:
        def check_all_consumed():
            self.consume_whitespace()
            if self.peek() is not None:
                raise SyntaxError(f"Expression too long")
        self.consume_whitespace()
        t = self.consume()
        if t is None:
            raise SyntaxError(f"Empty expression")
        elif t.token_type == TokenType.TEXT:
            check_all_consumed()
            return VariableRef(t.content)
        elif t.token_type == TokenType.MINUS:
            next = Parser(self.items[1:]).parse_expression()
            if not isinstance(next, IntLiteral):
                raise SyntaxError(f"- sing not followed by an integer")
            return IntLiteral(-next.num)
        elif t.token_type == TokenType.NUMBER:
            check_all_consumed()
            return IntLiteral(int(t.content))
        else:
            raise SyntaxError(f"Invalid token in expression '{t}'")

    def parse_program(self) -> Program:
        self.consume_whitespace()
        program = Program()
        while (t := self.consume()):
            if t.token_type == TokenType.PRINT:
                self.consume_whitespace()
                program.instructions.append(
                    PrintInst(Parser(self.collect_tokens(TokenType.NEWLINE)).parse_expression()))
            elif t.token_type == TokenType.LET:
                self.consume_whitespace()
                var_token = self.consume()
                if var_token is None or var_token.token_type != TokenType.TEXT:
                    raise SyntaxError("Invalid variable name after LET")
                var = VariableRef(var_token.content)
                if not (t := self.consume()) or t.token_type != TokenType.EQUALS:
                    raise SyntaxError(f"No = after variable name in LET")
                val_tokens = self.collect_tokens(TokenType.NEWLINE)
                val = Parser(val_tokens).parse_expression()
                program.instructions.append(LetInst(var, val))
            elif t.token_type == TokenType.INC or t.token_type == TokenType.DEC:
                self.consume_whitespace()
                var_token = self.consume()
                if var_token is None or var_token.token_type != TokenType.TEXT:
                    raise SyntaxError("Invalid variable name after INC")
                var = VariableRef(var_token.content)
                self.consume_whitespace()
                val_tokens = self.collect_tokens(TokenType.NEWLINE)
                val = Parser(val_tokens).parse_expression()
                if t.token_type == TokenType.INC:
                    program.instructions.append(IncInst(var, val))
                else:
                    program.instructions.append(DecInst(var, val))
            elif t.token_type == TokenType.LABEL:
                self.consume_whitespace()
                name_token = self.consume()
                if name_token is None or name_token.token_type != TokenType.TEXT:
                    raise SyntaxError("Expected a name after LABEL")
                name = name_token.content
                program.labels[name] = len(
                    program.instructions)
            elif t.token_type == TokenType.GOTO:
                self.consume_whitespace()
                name_token = self.consume()
                if name_token is None or name_token.token_type != TokenType.TEXT:
                    raise SyntaxError("Expected a label name after GOTO")
                name = name_token.content
                program.instructions.append(GotoInst(name))
            elif t.token_type == TokenType.JUMP:
                self.consume_whitespace()
                name_token = self.consume()
                if name_token is None or name_token.token_type != TokenType.TEXT:
                    raise SyntaxError("Expected a label name after JUMP")
                name = name_token.content
                self.consume_whitespace()
                if_token = self.consume()
                if if_token is None or if_token.token_type != TokenType.IF:
                    raise SyntaxError("Expected IF after JUMP label name")
                condition_tokens = self.collect_tokens(TokenType.NEWLINE)
                condition = Parser(condition_tokens).parse_expression()
                program.instructions.append(JumpInst(name, condition))
            else:
                raise SyntaxError(f"Unexpected token '{t}'")
            self.consume_whitespace()
        return program
