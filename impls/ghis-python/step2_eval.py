#!/usr/bin/env python3

import readline
from reader import read_str
from printer import pr_str
from maltypes import MalList, MalSymbol, MalVector, MalMap


repl_env = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: int(a / b)
}


def READ(arg: str):
    return read_str(arg)


def EVAL(ast, env):
    match ast:
        case MalList() if len(ast) == 0:
            return ast
        case MalList():
            new_ast = eval_ast(ast, env)
            return new_ast[0](*new_ast[1:])
        case _:
            return eval_ast(ast, env)


def eval_ast(ast, env):
    match ast:
        case MalSymbol():
            return env[str(ast)]
        case MalList():
            return MalList((EVAL(x, env) for x in ast))
        case MalVector():
            return MalVector((EVAL(x, env) for x in ast))
        case MalMap():
            return MalMap({k: EVAL(v, env) for k, v in ast.items()})
        case _:
            return ast


def PRINT(arg) -> str:
    return pr_str(arg)


def rep(line: str) -> str:
    try:
        return PRINT(EVAL(READ(line), repl_env))
    except Exception as e:
        return str(e)


def main():
    while (True):
        try:
            line = input("user> ")
        except EOFError:
            break
        print(rep(line))


if __name__ == "__main__":
    main()
