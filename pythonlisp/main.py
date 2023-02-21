import argparse
import importlib.metadata
from datetime import datetime

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
        + f"Version: {importlib.metadata.version('pythonlisp')}"
        + " " * 24
        + "*"
    )
    print("*" + " " * 48 + "*")
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
        try:
            Interpreter().interpret(program)
        except Exception as e:
            print(e)


def main():
    args = get_args()
    if not args.filename:
        repl()
    else:
        run(args.filename)


if __name__ == "__main__":
    main()
