%{
#include <stdio.h>
int tokenListFlag = 0; // Declare tokenListFlag variable
%}

%option noyywrap

%%

"{"       { if (!tokenListFlag) printf("Tokenlist:\n"); tokenListFlag = 1; printf("(BEGIN_OBJECT, '{')\n"); }
"}"       { printf("(END_OBJECT, '}')\n"); }
"["       { printf("(BEGIN_ARRAY, '[')\n"); }
"]"       { printf("(END_ARRAY, ']')\n"); }
","       { printf("(COMMA, ',')\n"); }
":"       { printf("(COLON, ':')\n"); }

"true"    { printf("(LITERAL, 'true')\n"); }
"false"   { printf("(LITERAL, 'false')\n"); }
"null"    { printf("(LITERAL, 'null')\n"); }

[0-9]+    { printf("(NUMBER, %s)\n", yytext); }
-?[0-9]+\.[0-9]+([eE][-+]?[0-9]+)? { printf("(NUMBER, %s)\n", yytext); }

\"[^\"]*\" { printf("(STRING, %s)\n", yytext); }

[[:space:]]+  { /* Ignore whitespace */ }

.         { printf("Invalid token: %s\n"); }

%%

int main() {
    printf("Enter JSON (press Ctrl+D on a new line to end input):\n");
    while (1) {
        char input[1024];
        if (!fgets(input, sizeof(input), stdin)) {
            break;  // Exit the loop when the input ends (Ctrl+D on a new line).
        }

        // Perform lexical analysis on the input.
        yy_scan_string(input);
        yylex();
    }

    return 0;
}
