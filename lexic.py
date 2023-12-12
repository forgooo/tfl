import re

keywords = ["for", "do"]


class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value


class LexemeTable:
    def __init__(self, tok, next=None):
        self.tok = tok
        self.next = next


lt = None
lt_head = None


def lexer(filename):
    try:
        with open(filename, 'r') as fd:
            CS = 'H'
            c = fd.read(1)

            while c:
                if CS == 'H':
                    while c.isspace():
                        c = fd.read(1)
                    if re.match(r'[A-Za-z_]', c):
                        CS = 'ID'
                    elif re.match(r'[0-9.]|[+-]', c):
                        CS = 'NM'
                    elif c == ':':
                        CS = 'ASGN'
                    else:
                        CS = 'DLM'

                if CS == 'ASGN':
                    colon = c
                    c = fd.read(1)
                    if c == '=':
                        tok = Token('ASGN', ':=')
                        add_token(tok)
                        c = fd.read(1)
                        CS = 'H'
                    else:
                        err_symbol = colon
                        CS = 'ERR'

                if CS == 'DLM':
                    if c in '();':
                        tok = Token('DELIM', c)
                        add_token(tok)
                        c = fd.read(1)
                        CS = 'H'
                    elif c in '<>=':
                        tok = Token('OPER', c)
                        add_token(tok)
                        c = fd.read(1)
                        CS = 'H'
                    else:
                        err_symbol = c
                        c = fd.read(1)
                        CS = 'ERR'

                if CS == 'ERR':
                    print(f"Unknown character: {err_symbol}")
                    CS = 'H'

                if CS == 'ID':
                    buf = c
                    c = fd.read(1)
                    while re.match(r'[A-Za-z0-9_]', c):
                        buf += c
                        c = fd.read(1)
                    if is_kword(buf):
                        tok = Token('KWORD', buf)
                    else:
                        tok = Token('IDENT', buf)
                    add_token(tok)
                    CS = 'H'

                if CS == 'NM':
                    buf = c
                    c = fd.read(1)
                    while re.match(r'[0-9eE.+-]', c):
                        buf += c
                        c = fd.read(1)
                    if is_num(buf):
                        tok = Token('NUM', buf)
                    else:
                        tok = Token('ERR', buf)
                    add_token(tok)
                    CS = 'H'

    except IOError:
        print(f"Cannot open file {filename}")


def is_kword(id):
    return id in keywords


def is_num(num):
    if re.match(r'^[+-]?\d+$', num):  # Целые
        return True
    if re.match(r'^[+-]?\d+\.\d*$', num) or re.match(r'^[+-]?\d*\.\d+$', num):  # Числа с плавающей точкой
        return True
    if re.match(r'^[+-]?\d+(\.\d*)?[eE][+-]?\d+$', num):  # e
        return True
    if num == '+' or num == '-' or num.lower() == 'e':
        return True
    return False


def add_token(tok):
    global lt, lt_head
    new_lexeme = LexemeTable(tok)
    if lt is None:
        lt = new_lexeme
        lt_head = new_lexeme
    else:
        lt.next = new_lexeme
        lt = new_lexeme


lexer("code.txt")

current = lt_head
while current:
    token_name = ""
    if current.tok.token_name == 'KWORD':
        token_name = "Keyword"
    elif current.tok.token_name == 'IDENT':
        token_name = "Identifier"
    elif current.tok.token_name == 'NUM':
        token_name = "Number"
    elif current.tok.token_name == 'OPER':
        token_name = "Operator"
    elif current.tok.token_name == 'DELIM':
        token_name = "Delimiter"
    elif current.tok.token_name == 'ASGN':
        token_name = "Assignment"
    else:
        token_name = "Unknown"
    print(f"{token_name}: {current.tok.token_value}")
    current = current.next

current = lt_head
while current:
    temp = current
    current = current.next
    del temp
