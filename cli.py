"""This is the script that combines everything together.

This file is meant to be called from the command line, and should be given a
file with the source code as an argument.

Example usage:
    python cli.py ./some_file.sa
"""

import argparse
from src.lexer import Lexer
from src.parser import Parser
from src.exec import ExecutionEnvironment


def main():
    """The main function that gets executed when this file is called."""
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source")
    argparser.add_argument("-v", action="store_true")
    args = argparser.parse_args()
    with open(args.source, "r", encoding="utf-8") as f:
        source = f.read()
    try:
        tokens = Lexer(source).tokenize()
        program = Parser(tokens).parse_program(strict_var_names=args.v)
    except BaseException as e:  # pylint: disable=broad-exception-caught
        print(f"Error occured during compiling: {e}")
        return
    eenv = ExecutionEnvironment(program)
    eenv.ip_exec()


if __name__ == "__main__":
    main()
