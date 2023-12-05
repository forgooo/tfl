class Token:
    def __init__(self, token_type, lexeme):
        self.token_type = token_type
        self.lexeme = lexeme
    def __str__(self):
        return f"Token({self.token_type}, '{self.lexeme}')"


from enum import Enum, auto


class TokenType(Enum):
    IDENTIFIER = auto()
    NUMBER = auto()
    FLOAT_NUMBER = auto()
    LOGICAL_CONST = auto()
    LETTER = auto()
    WORD = auto()
    RELATION_OP = auto()
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    SEMICOLON = auto()
    KEYWORD = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COMMENT = auto()
    HEXADECIMAL = auto()
    BINARY = auto()
    OCTAL = auto()
    COMMA = auto()
    PERIOD = auto()
    COLON = auto()


class State(Enum):
    H = 1
    DECIMAL_NUMBER = 2
    IDENTIFIER = 3
    DATA_TYPE = 4
    HEXADECIMAL = 5
    BINARY = 6
    OCTAL = 7
    ERROR = 8


lexeme_table = {
    'TW': 1,
    'TL': 2,
    'TN': 3,
    'TI': 4
}

number_tables = {
    TokenType.HEXADECIMAL: [],  # Используйте TokenType.HEXADECIMAL напрямую в качестве ключа
    TokenType.BINARY: [],
    TokenType.OCTAL: [],
}

keyword_table = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'for': 'FOR',
    'read': 'READ',
    'write': 'WRITE',
    '%': 'INT',
    '!': 'FLOAT',
    '$': 'BOOL',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
    'true': 'TRUE',
    'false': 'FALSE'
}

operator_table = {
    '+': 'ADD_OP',
    '-': 'ADD_OP',
    'or': 'ADD_OP',
    '*': 'MUL_OP',
    '/': 'MUL_OP',
    'and': 'MUL_OP',
    'not': 'UNARY_OP',
    '<>': 'RELATION_OP',
    '=': 'RELATION_OP',
    '<': 'RELATION_OP',
    '<=': 'RELATION_OP',
    '>': 'RELATION_OP',
    '>=': 'RELATION_OP'
    # ... другие операторы, если есть ...
}

identifier_table = {}

new_lexeme_table = {
    'IDENTIFIER': TokenType.IDENTIFIER,
    'NUMBER': TokenType.NUMBER,
    'LOGICAL_CONST': TokenType.LOGICAL_CONST,
    'IF': TokenType.KEYWORD,
    'ELSE': TokenType.KEYWORD,
    'WHILE': TokenType.KEYWORD,
    'FOR': TokenType.KEYWORD,
    'READ': TokenType.KEYWORD,
    'WRITE': TokenType.KEYWORD,
    'INT': TokenType.KEYWORD,
    'FLOAT': TokenType.KEYWORD,
    'BOOL': TokenType.KEYWORD,
    'AND': TokenType.KEYWORD,
    'OR': TokenType.KEYWORD,
    'NOT': TokenType.KEYWORD,
    'TRUE': TokenType.KEYWORD,
    'FALSE': TokenType.KEYWORD,
    '(': TokenType.LEFT_PAREN,
    ')': TokenType.RIGHT_PAREN,
    '[': TokenType.LEFT_BRACKET,
    ']': TokenType.RIGHT_BRACKET,
    '{': TokenType.LEFT_BRACE,
    '}': TokenType.RIGHT_BRACE,
    ',': TokenType.COMMA,
    ';': TokenType.SEMICOLON,
    '.': TokenType.PERIOD,
    ':': TokenType.COLON,
    '0b': TokenType.BINARY,
    '0o': TokenType.OCTAL,
    '0x': TokenType.HEXADECIMAL
}

tokens = ['IDENTIFIER', '+', 'NUMBER', '<', 'NUMBER', 'or', 'LOGICAL_CONST']
current_token_index = 0


def lexeme():
    global current_token_index
    if current_token_index < len(tokens):
        return tokens[current_token_index]
    else:
        return None  # Возвращает None, если достигнут конец списка лексем


def get_next_token():
    global current_token_index
    if current_token_index < len(tokens):
        current_token = tokens[current_token_index]
        current_token_index += 1
        return current_token
    else:
        return None  # Возвращает None, если достигнут конец списка лексем


def is_letter(char):
    return 'A' <= char <= 'Z' or 'a' <= char <= 'z'


def is_digit(char):
    return '0' <= char <= '9'


def error(message):
    print(f"Error: {message}")
    exit(1)  # Завершение выполнения программы с кодом ошибки 1


def identifier():
    lex = lexeme()
    if lex[0].isalpha():  # Проверяем, начинается ли лексема с буквы
        if all(char.isalnum() for char in lex):  # Проверяем, состоит ли лексема из букв и цифр
            get_next_token()
        else:
            error("Lexemas contain invalid characters")  # Если есть другие символы, вызываем ошибку
    else:
        error("The token must begin with a letter")  # Если первый символ не буква, вызываем ошибку


def number():
    lex = lexeme()
    if lex[:-1].isdigit():
        decimal()
    elif lex.endswith(('B', 'b')):
        binary()
    elif lex.endswith(('O', 'o')):
        octal()
    elif lex.endswith(('D', 'd')):
        decimal()
    elif lex.endswith(('H', 'h')):
        hexadecimal()
    else:
        error("Could not determine number type")
    get_next_token()  # Добавляем вызов get_next_token() для перехода к следующей лексеме


def binary():
    lex = lexeme()[:-1]  # Убираем символ обозначения двоичного числа (B/b)
    if all(bit in ('0', '1') for bit in lex):
        number = int(lex, 2)
        number_tables[TokenType.BINARY].append(number)  # Добавляем число в таблицу двоичных чисел
        lexeme_table[number] = TokenType.NUMBER  # Обновляем таблицу лексем
    else:
        error("Invalid binary number format")  # Если есть символы, отличные от 0 и 1, вызываем ошибку
    get_next_token()  # Добавляем вызов get_next_token() для перехода к следующей лексеме


def octal():
    lex = lexeme()  # получаем текущую лексему
    if lex.startswith('0') and all(digit in '01234567' for digit in lex):
        # Если начинается с '0' и содержит только восьмеричные цифры, это восьмеричное число
        number = int(lex, 8)
        number_tables[TokenType.OCTAL].append(number)  # Добавляем в таблицу восьмеричных чисел
        lexeme_table[number] = TokenType.OCTAL  # Обновляем таблицу лексем
    else:
        error("Incorrect octal number format")  # В противном случае, ошибка формата числа
    get_next_token()  # Переходим к следующей лексеме


def decimal():
    lex = lexeme()
    if not lex.startswith('0') and lex.isdigit():
        # Если не начинается с '0' и состоит только из цифр, это десятичное число
        number = int(lex)
        number_tables[TokenType.DECIMAL].append(number)
        lexeme_table[number] = TokenType.NUMBER
    else:
        error("Incorrect decimal format")
    get_next_token()


def hexadecimal():
    lex = lexeme()[:-1]  # Убираем символ обозначения шестнадцатеричного числа (H/h)
    valid_hex_chars = '0123456789ABCDEFabcdef'
    if all(char in valid_hex_chars for char in lex):
        number = int(lex, 16)
        number_tables[TokenType.HEXADECIMAL].append(number)  # Добавляем число в таблицу шестнадцатеричных чисел
        lexeme_table[number] = TokenType.NUMBER  # Обновляем таблицу лексем
    else:
        error("Invalid hexadecimal format")  # Если есть недопустимые символы, вызываем ошибку
    get_next_token()  # Добавляем вызов get_next_token() для перехода к следующей лексеме


def logical_constant():
    lex = lexeme()
    if lex == 'True' or lex == 'False':
        lexeme_table[lex] = TokenType.LOGICAL_CONST  # Добавляем логическую константу в таблицу лексем
    else:
        error(
            "Expected boolean constant True or False")  # Если лексема не является логической константой, вызываем ошибку


def multi_line_comment():
    if lexeme() == '/*':
        get_next_token()
        while lexeme() != '*/':
            if lexeme() is None:
                error(
                    "Reached end of file before closing comment")  # Если достигнут конец файла до закрытия комментария, вызываем ошибку
            get_next_token()
        get_next_token()  # Переходим к следующей лексеме после закрывающего тега '*/'
    else:
        error("Expected comment to start '/*'")  # Если не начат комментарий '/*', вызываем ошибку


def real():
    numerical_string()
    if lexeme() in {'E', 'e'}:
        get_next_token()
        if lexeme() in {'+', '-'}:
            get_next_token()
        numerical_string()


def numerical_string():
    if lexeme().isdigit():
        while lexeme().isdigit():
            get_next_token()
        if lexeme() == '.':
            get_next_token()
            while lexeme().isdigit():
                get_next_token()


def program():
    def program():
        if lexeme() == 'program':
            get_next_token()
            if lexeme() == 'var':
                get_next_token()
                description()
                if lexeme() == 'begin':
                    get_next_token()
                    program_operator()
                    while lexeme() == ';':
                        get_next_token()
                        program_operator()
                    if lexeme() == 'end':
                        get_next_token()
                    else:
                        error("Expected 'end' to terminate program")
                else:
                    error("Expected 'begin' after variable declaration")
            else:
                error("Expected 'var' for variable declaration")
        else:
            error("Expected 'program' to start the program")


def description():
    while lexeme() == 'IDENTIFIER':
        identifiers_list()
        if lexeme() == ':':
            get_next_token()
            data_type()
            if lexeme() == ';':
                get_next_token()
            else:
                error("Missing ';' after data type in description")
        else:
            error("Missing ':' after identifiers in description")



def assignment():
    identifier()
    if lexeme() == 'as':
        get_next_token()
        expression()  # Обработка выражения для присваивания
    else:
        error("Missing keyword 'as'")


def conditional():
    if lexeme() == 'if':
        get_next_token()
        expression()  # Обработка условия
        if lexeme() == 'then':
            get_next_token()
            program_operator()  # Обработка блока кода
            if lexeme() == 'else':
                get_next_token()
                program_operator()  # Обработка блока кода else
            else:
                error("Missing 'else' after if-then block")
        else:
            error("Missing 'then' after condition")
    else:
        error("Condition not met 'if'")


def fixed_loop():
    if lexeme() == 'for':
        get_next_token()
        assignment()  # Обработка инициализации
        if lexeme() == 'to':
            get_next_token()
            expression()  # Обработка условия цикла
            if lexeme() == 'do':
                get_next_token()
                program_operator()  # Обработка блока кода
            else:
                error("Missing 'do' after loop condition")  # Если отсутствует do после условия цикла, вызываем ошибку
        else:
            error("Missing 'to' after initialization")  # Если отсутствует to после инициализации, вызываем ошибку
    else:
        error("'for' condition not met")  # Если не выполнено условие 'for', вызываем ошибку


def conditional_loop():
    if lexeme() == 'while':
        get_next_token()
        expression()  # Обработка условия цикла
        if lexeme() == 'do':
            get_next_token()
            program_operator()  # Обработка блока кода
        else:
            error("Missing 'do' after loop condition")  # Если отсутствует do после условия цикла, вызываем ошибку
    else:
        error("'while' condition failed")  # Если не выполнено условие 'while', вызываем ошибку


def input_op():
    if lexeme() == 'read':
        get_next_token()
        if lexeme() == '(':
            get_next_token()
            while lexeme() != ')':
                if lexeme() == 'IDENTIFIER':
                    # Добавить идентификатор в таблицу ввода данных
                    identifier_table[lexeme()] = TokenType.IDENTIFIER
                    get_next_token()
                    if lexeme() == ',':
                        get_next_token()
                    elif lexeme() != ')':
                        error("Syntax error: missing ')'")  # Ошибка в синтаксисе
                else:
                    error("ID expected")  # Ожидается идентификатор
            get_next_token()  # Переходим к следующей лексеме после ')'
        else:
            error("Syntax error: missing '('")  # Ошибка в синтаксисе
    else:
        error("Error: Read operation 'read' was expected")  # Ошибка: ожидалась операция чтения 'read'


def output_op():
    if lexeme() == 'write':
        get_next_token()
        if lexeme() == '(':
            get_next_token()
            while lexeme() != ')':
                expression()  # Обработка выражения для вывода
                if lexeme() == ',':
                    get_next_token()
                elif lexeme() != ')':
                    error("Syntax error: missing ')'")  # Ошибка в синтаксисе
            get_next_token()  # Переходим к следующей лексеме после ')'
        else:
            error("Syntax error: missing '('")  # Ошибка в синтаксисе
    else:
        error("Error: 'write' operation expected")  # Ошибка: ожидалась операция записи 'write'


def variable_declaration():
    data_type()
    identifiers_list()


def data_type():
    if lexeme() in {'%', '!', '$'}:
        # This assumes that '%' corresponds to 'int', '!' to 'float', and '$' to 'bool'
        lexeme_table[lexeme()] = TokenType.DATA_TYPE
        get_next_token()
    else:
        error("Invalid data type specified")


def identifiers_list():
    identifier()
    while lexeme() == ',':
        get_next_token()
        if lexeme() == 'IDENTIFIER':
            get_next_token()
        else:
            error("Expected IDENTIFIER after ',' in identifiers_list")


def program_operator():
    if lexeme() == '{':
        compound()
    elif lexeme() == 'IDENTIFIER':
        assignment()
    elif lexeme() == 'if':
        conditional()
    elif lexeme() == 'for_fixed':
        fixed_loop()
    elif lexeme() == 'for':
        conditional_loop()
    elif lexeme() == 'input':
        input_op()
    elif lexeme() == 'output':
        output_op()
    else:
        error("None of the conditions are met")  # Если ни одно из условий не выполнено, вызываем ошибку


def compound():
    if lexeme() == '[':
        get_next_token()
        while lexeme() not in [']', 'EOF']:
            program_operator()
            if lexeme() in [':', 'NEWLINE']:
                get_next_token()
            else:
                error("Missing ':' or newline")
        if lexeme() == ']':
            get_next_token()
            if lexeme() not in [':', 'NEWLINE']:
                error("Missing ':' or newline after last operator in compound")
        else:
            error("Missing closing square bracket ']'")
    else:
        error("Missing opening square bracket '['")


# Константы и функции для обработки выражений
ADD_OPERATORS = {'+', '-', 'or'}
MUL_OPERATORS = {'*', '/', 'and'}
RELATIONAL_OPERATORS = {'<>', '=', '<', '<=', '>', '>='}


def term():
    factor()
    while lexeme() in MUL_OPERATORS:
        get_next_token()
        factor()


def operand():
    term()
    while lexeme() in ADD_OPERATORS:
        get_next_token()
        term()


def expression():
    operand()
    while lexeme() in RELATIONAL_OPERATORS:
        get_next_token()
        operand()


def factor():
    if lexeme() == 'IDENTIFIER':
        identifier()
    elif lexeme() == 'NUMBER':
        number()
    elif lexeme() == 'LOGICAL_CONST':
        logical_constant()
    elif lexeme() == 'UNARY_OP':
        get_next_token()
        factor()
    elif lexeme() == '(':
        get_next_token()
        expression()
        if lexeme() == ')':
            get_next_token()
        else:
            error("Missing closing bracket ')'")  # Если нет закрывающей скобки ')', вызываем ошибку
    else:
        error("Unidentified token")  # Если неопознанная лексема, вызываем ошибку


def analyze_input(input_string):
    global tokens
    tokens = []
    current_token = ""
    i = 0
    while i < len(input_string):
        if input_string[i].isspace():
            if current_token:
                tokens.append(current_token)
                current_token = ""
        elif input_string[i:i + 2] == '//':  # Обработка однострочных комментариев
            if current_token:
                tokens.append(current_token)
                current_token = ""
            end_of_line = input_string.find('\n', i + 2)
            if end_of_line == -1:  # Если нет символа новой строки, то комментарий до конца строки
                end_of_line = len(input_string)
            i = end_of_line if end_of_line != -1 else len(input_string)
        elif input_string[i:i + 2] == '/*':  # Обработка многострочных комментариев
            if current_token:
                tokens.append(current_token)
                current_token = ""
            end_comment = input_string.find('*/', i + 2)
            if end_comment == -1:  # Если нет символа закрытия комментария, вызываем ошибку
                print("Error: Unclosed multiline comment")
                return
            i = end_comment + 2
        elif input_string[i] in {'{', '}', ';', '(', ')'}:
            if current_token:
                tokens.append(current_token)
                current_token = ""
            tokens.append(input_string[i])
        else:
            current_token += input_string[i]
            if current_token.startswith(('0o', '0O')):
                octal_number = current_token[2:]
                if all(d in '01234567' for d in octal_number):
                    tokens.pop()
                    tokens.append(f"Token(TokenType.OCTAL, '{current_token}')")
                    current_token = ""
        i += 1

    if current_token:
        tokens.append(current_token)
    for token in tokens:
        if not token.startswith("Token(TokenType.COMMENT"):  # Игнорируем вывод комментариев
            # Выводим только токены, не являющиеся комментариями
            if token.isdigit():
                print(Token(TokenType.NUMBER, token))
            elif token.startswith(('0x', '0X')):
                print(Token(TokenType.HEXADECIMAL, token))
            elif token.startswith(('0b', '0B')):
                print(Token(TokenType.BINARY, token))
            elif token.startswith(('0o', '0O')) and all(d in '01234567' for d in token[2:]):
                print(Token(TokenType.OCTAL, token))
            elif token in operator_table:
                print(Token(operator_table[token], token))
            elif len(token) == 1 and token.isalpha():
                print(Token(TokenType.LETTER, token))
            elif token.isalpha():
                if token == 'true':
                    print(Token(TokenType.LOGICAL_CONST, token))
                elif token == 'false':
                    print(Token(TokenType.LOGICAL_CONST, token))
                elif token in keyword_table:
                    print(Token(TokenType.KEYWORD, token))
                else:
                    print(Token(TokenType.IDENTIFIER, token))
            elif '.' in token and token.replace('.', '').isdigit():
                print(Token(TokenType.FLOAT_NUMBER, token))
            else:
                if token.startswith("Token"):
                    print(token)
                elif token in new_lexeme_table:
                    print(Token(new_lexeme_table[token], token))
                else:
                    print(Token(TokenType.IDENTIFIER, token))


#<программа>::= program var <описание> begin <оператор> {;<оператор>} end.
input_string = 'program var x, y %; begin x = 123; y = 456; end.'
analyze_input(input_string)

"int x; int y; x = 123; y = 456; // Example"
"{ int x; int y; x = 5; y = 10; }"
"0 0xFF 0b1010 0765 true <= // Some comments"
"<>  =  <  <=  >  >= +  -  or *  / and not"
