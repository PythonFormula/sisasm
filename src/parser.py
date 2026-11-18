"""Parser turns tokens into instructions.

Typical usage:
    instructions = Parser(tokens).parse_program()
"""

from typing import Sequence
from src.pointer import PointerClass
from src.lexer import Token, TokenType


class Expression:
    """Base class for all expressions.

    Expressions are the smaller pieces that make up instructions.
    """


class IntLiteral(Expression):
    """Expression that is a number.

    Attributes:
        num(int): The number this represents.
    """

    num: int

    def __init__(self, num: int) -> None:
        """Initializes an IntLiteral object.

        Args:
            num(int): The number this represents.
        """
        super().__init__()
        self.num = num


class VariableRef(Expression):
    """Expression that refers to a variable.

    This means a variable name in source code.

    Attributes:
        var_name(str): The name of the variable.
    """

    var_name: str

    def __init__(self, var_name: str) -> None:
        """Initializes a VariableRef object.

        Args:
            var_name(str): The name of the variable.
        """
        super().__init__()
        self.var_name = var_name


class EqComparison(Expression):
    """Represents an equality comparison.

    Techically the order doesn't matter, but doing it this way is good practice.

    Attributes:
        a(Expression): Left side of the comparison.
        b(Expression): Right side of the comparison.
    """

    a: Expression
    b: Expression

    def __init__(self, a: Expression, b: Expression) -> None:
        """Initializes an EqComparison object.

        Args:
            a(Expression): Left side of the comparison.
            b(Expression): Right side of the comparison.
        """
        super().__init__()
        self.a = a
        self.b = b


class Instruction:
    """Base class for all instructions.

    An instruction is basically one line of source code.
    """


class PrintInst(Instruction):
    """Represents a line in source code that starts with PRINT.

    Attributes:
        value(Expression): The value to print.
    """

    value: Expression

    def __init__(self, value: Expression) -> None:
        """Initializes a PrintInst object.

        Args:
            value(Expression): The value to print.
        """
        super().__init__()
        self.value = value


class LetInst(Instruction):
    """Represents a line is source code that starts with LET.

    Attributes:
        var(VariableRef): The variable to be set.
        value(Expression): The value the variable will get.
    """

    var: VariableRef
    value: Expression

    def __init__(self, var: VariableRef, value: Expression) -> None:
        """Initializes a LetInst object.

        Args:
            var(VariableRef): The variable to be set.
            value(Expression): The value the variable will get.
        """
        super().__init__()
        self.var = var
        self.value = value


class IncInst(Instruction):
    """Represents a line in source code starting with INC.

    Attributes:
        var(VariableRef): The variable to be incremented.
        value(Expression): The amount the variable should be incremented.
    """

    var: VariableRef
    value: Expression

    def __init__(self, var: VariableRef, value: Expression) -> None:
        """Initializes an IncInst object.

        Args:
            var(VariableRef): The variable to be incremented.
            value(Expression): The amount the variable should be incremented.
        """
        super().__init__()
        self.var = var
        self.value = value


class DecInst(Instruction):
    """Represents a line in source code starting with DEC.

    Attributes:
        var(VariableRef): The variable to be decremented.
        value(Expression): The amount the variable should be decremented.
    """

    var: VariableRef
    value: Expression

    def __init__(self, var: VariableRef, value: Expression) -> None:
        """Initializes an DecInst object.

        Args:
            var(VariableRef): The variable to be decremented.
            value(Expression): The amount the variable should be decremented.
        """
        super().__init__()
        self.var = var
        self.value = value


class GotoInst(Instruction):
    """Represents a line in source code starting with GOTO.

    Attributes:
        label(str): The name of the label to go to.
    """

    label: str

    def __init__(self, label: str) -> None:
        """Initializes a GotoInst object.

        Args:
            label(str): The name of the label to go to.
        """
        super().__init__()
        self.label = label


class JumpInst(Instruction):
    """Represents a line in source code starting with JUMP.

    Attributes:
        label(str): The name of the label to go to.
        condition(Expression): The condition to decide wheter to jump. Should
          evaluate to a boolean.
    """

    label: str
    condition: Expression

    def __init__(self, label: str, condition: Expression) -> None:
        """Initializes a JumpInst object.

        Args:
            label(str): The name of the label to go to.
            condition(Expression): The condition to decide wheter to jump.
              Should evaluate to a boolean.
        """
        super().__init__()
        self.label = label
        self.condition = condition


class Program:
    """Stores all instructions and labels for a program.

    Attributes:
        instructions(list[Instruction]): The instructions of the program.
        labels(dict[str, in]): Maps label names to the instruction they point
          to.
    """

    instructions: list[Instruction]
    labels: dict[str, int]

    def __init__(self) -> None:
        """Initializes a Program object.

        Args:
            instructions(list[Instruction]): The instructions of the program.
            labels(dict[str, in]): Maps label names to the instruction they
              point to.
        """
        self.instructions = []
        self.labels = {}


class Parser(PointerClass[Token]):
    """Parser takes a list of tokens and parses them to a program or an
    expression.

    Attributes:
        items(Sequence[Token]): The tokens representing the source code (or a
          part of it)
    """

    def __init__(self, items: Sequence[Token]) -> None:
        """Initializes a Parser object.

        Args:
            items(Sequence[Token]): The tokens representing the source code (or
             a part of it)
        """
        super().__init__(items)

    def consume_whitespace(self) -> None:
        """Consumes all whitespace, until the next token isn't whitespace."""
        while (t := self.peek()) and t.token_type in [
            TokenType.SPACE,
            TokenType.NEWLINE,
        ]:
            self.consume()

    def check_token_type(self, token_type: TokenType, token: Token | None = None):
        """Checks wether the given token is of a certain token type.

        If no token is given, the default is the current one.

        Args:
            token_type(TokenType): The type to be checked for.
            token(Token): The token to be checked, default is None, which will
              use the current one.
        """
        if token is None:
            token = self.peek()
        return token is not None and token.token_type == token_type

    def collect_tokens(self, end: TokenType | None = None) -> list[Token]:
        """Consumes and collects tokens until the next one is of a specific type
        or there are no more left.

        Args:
            end(TokenType | None): The token type which this should stop one, if
              None, this only stops when tokens end.

        Returns:
            tokens(list[Token]): All the tokens consumed, before the end.
        """
        tokens: list[Token] = []
        while (t := self.peek()) and t.token_type != end:
            tokens.append(t)
            self.consume()
        return tokens

    def parse_expression(self) -> Expression:
        """Parses the tokens into an expression.

        This is not meant to be run on a program, but just a part of an
        instruction

        Raises:
            SyntaxError: There are no tokens to parse.
            SyntaxError: There are no tokens after '=='
        """

        def parse_singelton() -> Expression | None:
            """Parses the next token into one expression.

            Returns None if there are no more tokens left.

            Raises:
                SyntaxError: The next token cannot be part of a single token
                  expression.
            """
            t = self.consume()
            if t is None:
                return None
            elif t.token_type == TokenType.TEXT:
                return VariableRef(t.content)
            elif t.token_type == TokenType.NUMBER:
                return IntLiteral(int(t.content))
            elif t.token_type == TokenType.MINUS:
                next_expr = parse_singelton()
                if not isinstance(next_expr, IntLiteral):
                    raise SyntaxError("- sing not followed by an integer")
                return IntLiteral(-next_expr.num)
            else:
                raise SyntaxError(f"Invalid token in singelton expression '{t}'")

        self.consume_whitespace()
        left = parse_singelton()
        if not left:
            raise SyntaxError("Empty expression")
        if ((t := self.peek()) and t.token_type == TokenType.EQUALS) and (
            (t := self.peek(1)) and t.token_type == TokenType.EQUALS
        ):
            self.consume()
            self.consume()
            right = parse_singelton()
            if not right:
                raise SyntaxError("Expected expression after '=='")
            left = EqComparison(left, right)
        return left

    def parse_program(self) -> Program:
        """Parses the tokens into a program.

        Raises:
            SyntaxError: Many reasons, usually there is a syntax error in the
              source code.
        """
        self.consume_whitespace()
        program = Program()
        while t := self.consume():
            # At this point, the pointer should be at the beginning of a line.
            # Each case should parse on line (except for trailing whitespace).
            if t.token_type == TokenType.PRINT:
                self.consume_whitespace()
                program.instructions.append(
                    PrintInst(
                        Parser(
                            self.collect_tokens(TokenType.NEWLINE)
                        ).parse_expression()
                    )
                )
            elif t.token_type == TokenType.LET:
                self.consume_whitespace()
                var_token = self.consume()
                if var_token is None or var_token.token_type != TokenType.TEXT:
                    raise SyntaxError("Invalid variable name after LET")
                var = VariableRef(var_token.content)
                if not (t := self.consume()) or t.token_type != TokenType.EQUALS:
                    raise SyntaxError("No = after variable name in LET")
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
                program.labels[name] = len(program.instructions)
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
