from lexer import Lexical
from syntax import Syntax
from semantic import IdenTable


def main():
    identifiersTable = IdenTable()
    lexer = Lexical("test", identifiersTable)
    lexer.analysis()
    if lexer.current.state != lexer.states.ERR:
        print("Result of Lexical Analyzer:")
        for i in lexer.lexeme_table:
            print(f"{i.token_name} {i.token_value}")


        syntaxAnalyzer = Syntax(lexer.lexeme_table, identifiersTable)
        syntaxAnalyzer.PROGRAMM()
        identifiersTable.check_if_all_described()
        print("!!!COMPILED")


if __name__ == "__main__":
    main()
