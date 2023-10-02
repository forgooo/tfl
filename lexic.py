import re

class Token:
    def __init__(self, token_name, token_value):
        self.token_name = token_name
        self.token_value = token_value

    def __str__(self):
        return f'Token({self.token_name}, {self.token_value})'

class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.keywords = set(["for", "do"])
        self.symbols = set(["(", ")", ";", "<", ">", "="])
        self.current_position = 0

    def is_keyword(self, word):
        return word in self.keywords

    def is_symbol(self, char):
        return char in self.symbols

    def lex(self):
        tokens = []
        while self.current_position < len(self.input_string):
            char = self.input_string[self.current_position]
            if char.isspace():
                self.current_position += 1
            elif char in self.symbols:
                tokens.append(Token("DLM", char))
                self.current_position += 1
            elif char == ":" and self.input_string[self.current_position + 1] == "=":
                tokens.append(Token("ASGN", ":="))
                self.current_position += 2
            elif re.match(r"[a-zA-Z_]", char):
                word = ""
                while self.current_position < len(self.input_string) and \
                        re.match(r"[a-zA-Z0-9_]", self.input_string[self.current_position]):
                    word += self.input_string[self.current_position]
                    self.current_position += 1
                if self.is_keyword(word):
                    tokens.append(Token("KWORD", word))
                else:
                    tokens.append(Token("IDENT", word))
            elif re.match(r"[0-9]", char) or (char == "-" and re.match(r"[0-9]", self.input_string[self.current_position + 1])):
                number = ""
                while self.current_position < len(self.input_string) and \
                        re.match(r"[0-9.+-eE]", self.input_string[self.current_position]):
                    number += self.input_string[self.current_position]
                    self.current_position += 1
                tokens.append(Token("NM", number))
            else:
                tokens.append(Token("ERR", char))
                self.current_position += 1
        return tokens

# Чтение строки из файла
with open('file.txt', 'r') as file:
    input_string = file.read()

lexer = Lexer(input_string)
tokens = lexer.lex()

for token in tokens:
    print(token)
