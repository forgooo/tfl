from typing import NamedTuple


class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value
    def __repr__(self):
        return f"{self.token_name} ::= {self.token_value}"


class States(NamedTuple):
    H: str
    COMM: str
    ID: str
    ERR: str
    NM: str
    DLM: str


class Tokens(NamedTuple):
    KWORD: str
    IDENT: str
    NUM: str
    OPER: str
    DELIM: str
    NUM2: str
    NUM8: str
    NUM10: str
    NUM16: str
    REAL: str
    TYPE: str
    ARITH: str


class Current:
    def __init__(self, symbol: str = "", eof_state: bool = False, line_number: int = 0, pos_number: int = 0,
                 state: str = ""):
        self.symbol = symbol
        self.eof_state = eof_state
        self.line_number = line_number
        self.pos_number = pos_number
        self.state = state

    def re_assign(self, symbol: str, eof_state: bool, line_number: int, pos_number: int):
        self.symbol = symbol
        self.eof_state = eof_state
        self.line_number = line_number
        self.pos_number = pos_number


class Error:
    def __init__(self, filename: str, symbol: str = "", line: int = 0, pos_in_line: int = 0):
        self.filename = filename
        self.symbol = symbol
        self.line = line
        self.pos_in_line = pos_in_line

def fgetc_generator(filename: str):
    with open(filename) as fin:
        s = list(fin.read())
        s.append('\n')
        counter_pos, counter_line = 1, 1
        for i in range(len(s)):
            yield s[i], s[i] == "@", counter_line, counter_pos
            if s[i] == "\n":
                counter_pos = 0
                counter_line += 1
            else:
                counter_pos += 1
