#!/usr/bin/env python3

import readline


def READ(arg: str) -> str:
    return arg


def EVAL(arg: str) -> str:
    return arg


def PRINT(arg: str) -> str:
    return arg


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
