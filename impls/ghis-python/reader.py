import re
from contextlib import suppress
from maltypes import (
    MalDeref,
    MalList,
    MalMap,
    MalQuasiQuote,
    MalQuote,
    MalSpliceUnquote,
    MalVector,
    MalUnquote
)


__TOKENIZER_RE = re.compile(r"[\s,]*(~@|[\[\]{}()'`~^@]|\"(?:\\.|[^\\\"])*\"?|;.*|[^\s\[\]{}('\"`,;)]*)")


class ParseError(Exception):
    def __init__(self, message, token):
        super().__init__(message)
        self.token = token


class Reader:
    def __init__(self, tokens: tuple[str]):
        self._tokens = tokens
        self._position = 0

    def next(self) -> str:
        token = self._tokens[self._position]
        self._position = self._position + 1
        return token

    def peek(self) -> str:
        if self._position >= len(self._tokens):
            raise ParseError(message="Encountered EOF", token="")
        token = self._tokens[self._position]
        if not token:
            raise ParseError(message="Encountered EOF", token="")
        return self._tokens[self._position]


def read_str(arg: str):
    reader = Reader(tokenize(arg))
    try:
        return read_form(reader)
    except ParseError as e:
        return str(e)


def tokenize(arg: str) -> tuple[str]:
    return __TOKENIZER_RE.findall(arg)


def read_form(reader: Reader):
    try:
        tok = reader.peek()
    except ParseError:
        raise
    match tok:
        case "'":
            reader.next()
            return MalList((MalQuote, read_form(reader)))
        case "`":
            reader.next()
            return MalList((MalQuasiQuote, read_form(reader)))
        case "~":
            reader.next()
            return MalList((MalUnquote, read_form(reader)))
        case "~@":
            reader.next()
            return MalList((MalSpliceUnquote, read_form(reader)))
        case "@":
            reader.next()
            return MalList((MalDeref, read_form(reader)))
        case '(' | '[' | '{':
            return read_list(reader)
        case ')' | ']' | '}':
            reader.next()
            raise ParseError(message=f"Could not parse token {tok}", token=tok)
    return read_atom(reader)


def read_list(reader: Reader):
    tok = reader.next()
    match tok[0]:
        case '(':
            result = MalList()
        case '[':
            result = MalVector()
        case '{':
            result = MalMap()
        case _:
            raise ParseError("Expected collection start")

    while (True):
        try:
            result.append(read_form(reader))
        except ParseError as e:
            if not e.token or e.token[0] != result.end_delimiter:
                raise e
            break
    return result


def read_atom(reader: Reader):
    tok = reader.next()
    if tok[0] == '"':
        if any((
            len(tok) == 1,
            tok[-1] != '"',
            ((len(tok[:-1]) - len(tok[:-1].rstrip('\\'))) % 2 != 0)
        )):
            raise ParseError(f"Found unbalanced '\"' in {tok}", token=tok)
        return tok
    with suppress(ValueError):
        number = int(tok)
        return number
    with suppress(ValueError):
        number = float(tok)
        return number
    return tok
