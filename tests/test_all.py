"""Unit tests using the examples from ville"""

import pytest  # pylint: disable=unused-import
from src.lexer import Lexer
from src.parser import Parser
from src.exec import ExecutionEnvironment


def get_output(version: int, num: int) -> str:
    """Gets the output that gets produced by a given test program.

    Args:
        version(int): The version (v1-v4) which the test program belongs to.
        num(int): The number of the program inside the version's folder.
    """
    with open(f"tests\\v{version}\\program_{num}.sa", "r", encoding="utf-8") as f:
        source = f.read()
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()
    return ExecutionEnvironment(program).np_exec()[0]


def get_result(version: int, num: int) -> str:
    """Gets the correct output for a certain test program.

    Args:
        version(int): The version (v1-v4) which the test program belongs to.
        num(int): The number of the program inside the version's folder.
    """
    with open(f"tests\\v{version}\\result_{num}.txt", "r", encoding="utf-8") as f:
        return f.read()


def test_v1():  # pylint: disable=missing-function-docstring
    assert get_output(1, 1).strip() == get_result(1, 1).strip()
    assert get_output(1, 2).strip() == get_result(1, 2).strip()
    assert get_output(1, 3).strip() == get_result(1, 3).strip()


def test_v2():  # pylint: disable=missing-function-docstring
    assert get_output(2, 1).strip() == get_result(2, 1).strip()
    assert get_output(2, 2).strip() == get_result(2, 2).strip()
    assert get_output(2, 3).strip() == get_result(2, 3).strip()
    assert get_output(2, 4).strip() == get_result(2, 4).strip()


def test_v3():  # pylint: disable=missing-function-docstring
    assert get_output(3, 1).strip() == get_result(3, 1).strip()
    assert get_output(3, 2).strip() == get_result(3, 2).strip()
    assert get_output(3, 3).strip() == get_result(3, 3).strip()


def test_v4():  # pylint: disable=missing-function-docstring
    assert get_output(4, 1).strip() == get_result(4, 1).strip()
    assert get_output(4, 2).strip() == get_result(4, 2).strip()
    assert get_output(4, 3).strip() == get_result(4, 3).strip()
