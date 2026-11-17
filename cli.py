import argparse
from src.lexer import Lexer
from src.parser import Parser
from src.exec import ExecutionEnvironment


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("source")
    args = argparser.parse_args()
    with open(args.source, "r") as f:
        source = f.read()
    tokens = Lexer(source).tokenize()
    program = Parser(tokens).parse_program()
    eenv = ExecutionEnvironment(program)
    eenv.ip_exec()


if __name__ == "__main__":
    main()
