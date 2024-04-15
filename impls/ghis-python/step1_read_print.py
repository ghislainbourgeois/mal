#!/usr/bin/env python3

import readline
from reader import read_str
from printer import pr_str


def READ(arg: str):
    return read_str(arg)


def EVAL(arg):
    return arg


def PRINT(arg) -> str:
    return pr_str(arg)


def rep(line: str) -> str:
    return PRINT(EVAL(READ(line)))


def main():
    while (True):
        try:
            line = input("user> ")
        except EOFError:
            break
        print(rep(line))


if __name__ == "__main__":
    main()
