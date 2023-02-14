import argparse
from datetime import datetime

from pythonlisp.interpreter import Interpretor


def get_args():
    parser = argparse.ArgumentParser("pythonlisp")
    parser.add_argument("-f", "--filename", required=False)
    return parser.parse_args()


def repl():
    interpreter = Interpretor()
    print("Welcome to PythonLisp!!!!!")
    print(f"Date: {datetime.now()}")
    print("Version:")
    print()
    while True:
        print("\u03BB  ", end="")
        line = input()
        if line == ":exit":
            print("Bye!!!")
            return
        print(interpreter.interpret(line))


def run(filename):
    with open(filename, "r") as f:
        program = f.read()
        Interpretor().interpret(program)


def main():
    args = get_args()
    if not args.filename:
        repl()
    else:
        run(args.filename)


if __name__ == "__main__":
    main()
