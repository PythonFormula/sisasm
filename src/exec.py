"""Executes programs."""

from src.parser import (
    Program,
    Expression,
    IntLiteral,
    VariableRef,
    Instruction,
    LetInst,
    PrintInst,
    IncInst,
    DecInst,
    GotoInst,
    EqComparison,
    JumpInst,
)

# The types that a variable or an expression can have.
VarValType = int | bool


class ExecutionEnvironment:
    """Container to execute programs in.

    Attributes:
        variable_values(dict[str, VarValType]): Stores the values of all the
          variables during execution.
        line(int): The index of the instruction the program is on. This does not
          mathc with lines in the source code.
        program(Program): The program to execute.
        output_buffer(str): All the output gets first written here before it
          gets printed or processed.
    """

    variable_values: dict[str, VarValType]
    line: int
    program: Program
    output_buffer: str

    def __init__(self, program: Program) -> None:
        """Initializes an ExecutionEnvironment object.

        Args:
            program(Program): The program to be executed.
        """
        self.variable_values = {}
        self.line = 0
        self.program = program
        self.output_buffer = ""

    def reset(self) -> None:
        """Sets the values to their defaults, so that the program can be run
        again.
        """
        self.variable_values = {}
        self.line = 0
        self.output_buffer = ""

    @staticmethod
    def value_to_string(val: VarValType) -> str:
        """Takes a value from a variable or an expression and turns it into a
        string.

        Args:
            val(VarValType): The value to be converted to a string.
        """
        if isinstance(val, int):
            return str(val)
        elif isinstance(val, bool):
            # Use lowercase names instead of python's capitalized ones.
            return "true" if val else "false"
        else:
            raise ValueError(f"Invalid value type '{type(val)}'")

    def evaluate_expression(self, expr: Expression) -> VarValType:
        """Evaluates an expression.

        Args:
            expr(Expression): The expression to be evaluated.

        Returns:
            value(VarValType): The evaluation of the expression.
        """
        if isinstance(expr, IntLiteral):
            return expr.num
        elif isinstance(expr, VariableRef):
            return self.variable_values[expr.var_name]
        elif isinstance(expr, EqComparison):
            return self.evaluate_expression(expr.a) == self.evaluate_expression(expr.b)
        else:
            raise ValueError(f"Invalid expression type '{type(expr)}'")

    def execute_instruction(self, inst: Instruction) -> None:
        """Executes one instruction.

        The instruction needs to be given, this does not use the line attribute.

        Args:
            inst(Instruction): The instruction to be executed.
        """
        if isinstance(inst, LetInst):
            self.variable_values[inst.var.var_name] = self.evaluate_expression(
                inst.value
            )
        elif isinstance(inst, PrintInst):
            self.output_buffer += (
                f"{self.value_to_string(self.evaluate_expression(inst.value))}\n"
            )
        elif isinstance(inst, IncInst):
            self.variable_values[inst.var.var_name] += self.evaluate_expression(
                inst.value
            )
        elif isinstance(inst, DecInst):
            self.variable_values[inst.var.var_name] -= self.evaluate_expression(
                inst.value
            )
        elif isinstance(inst, GotoInst):
            # -1 to cancel out the line increment after executing this
            # instruction.
            self.line = self.program.labels[inst.label] - 1
        elif isinstance(inst, JumpInst):
            evaluated = self.evaluate_expression(inst.condition)
            # Jump condition must result in a boolean
            if not isinstance(evaluated, bool):
                raise RuntimeError(
                    f"Jump condition '{inst}' resulted in a non-boolean value"
                )
            if evaluated:
                # -1 to cancel out the line increment after executing this
                # instruction.
                self.line = self.program.labels[inst.label] - 1
        else:
            raise ValueError(f"Invalid instruction type '{type(inst)}'")

    def np_exec(self) -> tuple[str, int]:
        """Execute the program without printing and return all the output.

        Returns:
            output(str): All the output the program produced.
            exit_code(int): The exit code of the program.
        """
        self.reset()
        while self.line < len(self.program.instructions):
            try:
                self.execute_instruction(self.program.instructions[self.line])
                self.line += 1
            # Catching BaseException is fine, becouse we end execution
            # immidiately and put the error to the output.
            except BaseException as e:
                self.output_buffer += f"Error occured during execution: {e}\n"
                return self.output_buffer, 1
        return self.output_buffer, 0

    def ip_exec(self) -> int:
        """Execute the program and print after each instruction.

        Returns:
            exit_code(int): The exit code of the program.
        """
        self.reset()
        while self.line < len(self.program.instructions):
            try:
                self.execute_instruction(self.program.instructions[self.line])
                self.line += 1
            # Catching BaseException is fine, becouse we end execution
            # immidiately and print the error message.
            except BaseException as e:
                print(f"Error occured during execution: {e}\n")
                return 1
            print(self.output_buffer, end="")
            self.output_buffer = ""
        return 0
