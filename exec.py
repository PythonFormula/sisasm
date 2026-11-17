from parser import (
    Program,
    Expression,
    IntLiteral,
    VariableRef,
    Instruction,
    LetInst,
    PrintInst,
    IncInst,
    DecInst,
    GotoInst
)

VarValType = int


class ExecutionEnvironment:
    variable_values: dict[str, VarValType]
    line: int
    program: Program
    output_buffer: str

    def __init__(self, program: Program) -> None:
        self.variable_values = {}
        self.line = 0
        self.program = program
        self.output_buffer = ""

    @staticmethod
    def value_to_string(val: VarValType) -> str:
        if isinstance(val, int):
            return str(val)
        else:
            raise ValueError(f"Invalid value type '{type(val)}'")

    def evaluate_expression(self, expr: Expression) -> VarValType:
        if isinstance(expr, IntLiteral):
            return expr.num
        elif isinstance(expr, VariableRef):
            return self.variable_values[expr.var_name]
        else:
            raise ValueError(f"Invalid expression type '{type(expr)}'")

    def execute_instruction(self, inst: Instruction) -> None:
        if isinstance(inst, LetInst):
            self.variable_values[inst.var.var_name] = self.evaluate_expression(
                inst.value)
        elif isinstance(inst, PrintInst):
            self.output_buffer += f"{self.value_to_string(self.evaluate_expression(inst.value))}\n"
        elif isinstance(inst, IncInst):
            self.variable_values[inst.var.var_name] += self.evaluate_expression(
                inst.value)
        elif isinstance(inst, DecInst):
            self.variable_values[inst.var.var_name] -= self.evaluate_expression(
                inst.value)
        elif isinstance(inst, GotoInst):
            self.line = self.program.labels[inst.label]-1
        else:
            raise ValueError(f"Invalid instruction type '{type(inst)}'")

    def np_exec(self) -> tuple[str, int]:
        self.output_buffer = ""
        while self.line < len(self.program.instructions):
            try:
                self.execute_instruction(self.program.instructions[self.line])
                self.line += 1
            except BaseException as e:
                self.output_buffer += f"Error occured during execution: {e}\n"
                return self.output_buffer, 1
        return self.output_buffer, 0

    def ip_exec(self) -> int:
        self.output_buffer = ""
        while self.line < len(self.program.instructions):
            try:
                self.execute_instruction(self.program.instructions[self.line])
                self.line += 1
            except BaseException as e:
                print(f"Error occured during execution: {e}\n")
                return 1
            print(self.output_buffer, end="")
            self.output_buffer = ""
        return 0
