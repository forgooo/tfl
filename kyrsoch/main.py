from lexer import Lexical
from syntax import Syntax
from semantic import IdenTable

PRINT_INFO = True
PATH_TO_PROGRAM = "test"


def main():
    identifiersTable = IdenTable()
    lexer = Lexical(PATH_TO_PROGRAM, identifiersTable)
    lexer.analysis()
    if lexer.current.state != lexer.states.ERR:
        if PRINT_INFO:
            print("Result of Lexical Analyzer:")
            for i in lexer.lexeme_table:
                print(f"{i.token_name} {i.token_value}")


        syntaxAnalyzer = Syntax(lexer.lexeme_table, identifiersTable)
        syntaxAnalyzer.PROGRAMM()
        identifiersTable.check_if_all_described()
        print("!!!COMPILED")

if __name__ == "__main__":
    main()
