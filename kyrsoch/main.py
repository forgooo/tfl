from LexicalAnalizer import LexicalAnalyzer
from SyntacticalAnalyzer import SyntacticalAnalyzer
from SemanticalAnalyzer import IdentifiersTable

PRINT_INFO = True
PATH_TO_PROGRAM = "second_program.poullang"


def main():
    identifiersTable = IdentifiersTable()
    lexer = LexicalAnalyzer(PATH_TO_PROGRAM, identifiersTable)
    lexer.analysis()
    if lexer.current.state != lexer.states.ERR:
        if PRINT_INFO:
            print("Result of Lexical Analyzer:")
            for i in lexer.lexeme_table:
                print(f"{i.token_name} {i.token_value}")


        syntaxAnalyzer = SyntacticalAnalyzer(lexer.lexeme_table, identifiersTable)
        syntaxAnalyzer.PROGRAMM()
        identifiersTable.check_if_all_described() # проверка что все Id описаны
        if PRINT_INFO:
            print(identifiersTable)
        print("+---------+")
        print("| SUCCESS |")
        print("+---------+")

if __name__ == "__main__":
    main()
