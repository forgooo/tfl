def get_priority(operation):
    if operation == "(":
        return 1
    elif operation in ("+", "-"):
        return 2
    elif operation in ("*", "/"):
        return 3
    else:
        return 0


def evaluate_expression(formula):
    enable_operations = ["+", "-", "*", "/", "("]
    stack = []
    output = []

    for item in formula.split():
        if item.isalnum():
            output.append(item)
        elif item in enable_operations:
            if item == "(":
                stack.append(item)
            else:
                while stack and get_priority(item) <= get_priority(stack[-1]):
                    output.append(stack.pop())
                stack.append(item)
        elif item == ")":
            while stack and stack[-1] != "(":
                output.append(stack.pop())
            stack.pop()

    output.extend(reversed(stack))
    return output


def calculate_result(expression):
    stack = []
    for item in expression:
        if item.isalnum():
            stack.append(item)
        elif item in ("+", "-", "*", "/"):
            second_operand = stack.pop()
            first_operand = stack.pop()
            stack.append(str(eval(first_operand + item + second_operand)))

    return stack[0]


formula = input("Enter a mathematical expression: ")
expression = evaluate_expression(formula)
print("Postfix expression:", " ".join(expression))

if not any(c.isalpha() for c in expression):
    result = calculate_result(expression)
    print("Result:", result)
