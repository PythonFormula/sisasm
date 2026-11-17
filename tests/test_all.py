import pytest
from lexer import Lexer
from parser import Parser
from exec import ExecutionEnvironment


def get_output(version: int, num: int) -> str:
    with open(f"tests\\v{version}\\program_{num}.sa", "r") as f:
        source = f.read()
    tokens = Lexer(source).tokenize()
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()
    return ExecutionEnvironment(program).np_exec()[0]


def get_result(version: int, num: int) -> str:
    with open(f"tests\\v{version}\\result_{num}.txt", "r") as f:
        return f.read()


def test_v1():
    assert get_output(1, 1).strip() == get_result(1, 1).strip()
    assert get_output(1, 2).strip() == get_result(1, 2).strip()
    assert get_output(1, 3).strip() == get_result(1, 3).strip()


def test_v2():
    assert get_output(2, 1).strip() == get_result(2, 1).strip()
    assert get_output(2, 2).strip() == get_result(2, 2).strip()
    assert get_output(2, 3).strip() == get_result(2, 3).strip()
    assert get_output(2, 4).strip() == get_result(2, 4).strip()


def test_v3():
    assert get_output(3, 1).strip() == get_result(3, 1).strip()
    assert get_output(3, 2).strip() == get_result(3, 2).strip()
    assert get_output(3, 3).strip() == get_result(3, 3).strip()
