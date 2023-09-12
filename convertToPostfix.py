op = {'+', '-', '*', '/', '(', ')', '^'}
pr = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}


def infixToPostfix(expression):
    stack = []
    output = ''
    for character in expression:
        if character not in op:
            output += character
        elif character == '(':
            stack.append('(')
        elif character == ')':
            while stack and stack[-1] != '(':
                output += stack.pop()
            stack.pop()
        else:
            while stack and stack[-1] != '(' and pr[character] <= pr[stack[-1]]:
                output += stack.pop()
            stack.append(character)
    while stack:
        output += stack.pop()
    return output


expression = input()
print(infixToPostfix(expression))
