import argparse
from datetime import datetime

import pkg_resources

from pythonlisp.interpreter import Interpreter


def get_args():
    parser = argparse.ArgumentParser("pythonlisp")
    parser.add_argument("-f", "--filename", required=False)
    return parser.parse_args()


def repl():
    interpreter = Interpreter()
    print()
    print("*" * 50)
    print("*" + " " * 48 + "*")
    print("*" + " " * 10 + "Welcome to PythonLisp!!!!!" + " " * 12 + "*")
    print("*" + " " * 10 + f"Date: {datetime.now()}" + " " * 6 + "*")
    print(
        "*"
        + " " * 10
        + f"Version: {pkg_resources.get_distribution('pythonlisp').version}"
        + " " * 24
        + "*"
    )
    print("*" * 50)
    print()
    print()
    while True:
        print("\u03BB  ", end="")
        try:
            line = input()
            if line == ":exit":
                print("Bye!!!")
                return
            print(interpreter.interpret(line))
        except Exception as e:
            print(e)


def run(filename):
    with open(filename, "r") as f:
        program = f.read()
        Interpreter().interpret(program)


def main():
    args = get_args()
    if not args.filename:
        repl()
    else:
        run(args.filename)


if __name__ == "__main__":
    main()
