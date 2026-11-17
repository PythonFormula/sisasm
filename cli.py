import argparse
from lexer import Lexer
from parser import Parser
from exec import ExecutionEnvironment


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
