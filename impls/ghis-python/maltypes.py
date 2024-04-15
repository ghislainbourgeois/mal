import collections


class MalSymbol:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return self.__name


MalQuote = MalSymbol("quote")
MalQuasiQuote = MalSymbol("quasiquote")
MalUnquote = MalSymbol("unquote")
MalSpliceUnquote = MalSymbol("splice-unquote")
MalDeref = MalSymbol("deref")


class MalCollection(collections.UserList):
    start_delimiter = ''
    end_delimiter = ''

    def __str__(self):
        return self.start_delimiter + " ".join(str(x) for x in self.data) + self.end_delimiter


class MalList(MalCollection):
    start_delimiter = '('
    end_delimiter = ')'


class MalVector(MalCollection):
    start_delimiter = '['
    end_delimiter = ']'


class MalMap(collections.UserDict):
    start_delimiter = '{'
    end_delimiter = '}'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._previous_key = None

    def append(self, item):
        if self._previous_key:
            self.data[self._previous_key] = item
            self._previous_key = None
        else:
            self._previous_key = item

    def __str__(self):
        return self.start_delimiter + " ".join(f"{str(k)} {str(v)}" for k, v in self.data.items()) + self.end_delimiter
