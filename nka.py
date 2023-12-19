def epsilon_closure(states, transitions, epsilon='eps'):
    closure = set(states)
    stack = list(states)
    while stack:
        state = stack.pop()
        for transition in transitions:
            if transition[0] == state and transition[1] == epsilon:
                if transition[2] not in closure:
                    closure.add(transition[2])
                    stack.append(transition[2])
    return closure


def move(states, transitions, symbol):
    result = set()
    for state in states:
        for transition in transitions:
            if transition[0] == state and transition[1] == symbol:
                result.add(transition[2])
    return result


def nfa_to_dfa(states, alphabet, transitions, initial_states, final_states):
    dfa_states = []
    dfa_transitions = []
    dfa_initial_state = frozenset(epsilon_closure(initial_states, transitions))
    dfa_states.append(dfa_initial_state)
    stack = [dfa_initial_state]

    while stack:
        current_dfa_state = stack.pop()
        for symbol in alphabet:
            next_nfa_state = epsilon_closure(move(current_dfa_state, transitions, symbol), transitions)
            if next_nfa_state not in dfa_states:
                dfa_states.append(next_nfa_state)
                stack.append(next_nfa_state)
            dfa_transitions.append((current_dfa_state, symbol, next_nfa_state))

    dfa_final_states = [state for state in dfa_states if any(s in state for s in final_states)]

    return dfa_states, alphabet, dfa_transitions, dfa_initial_state, dfa_final_states


def main():
    states = input("Enter set of states: ").split()
    alphabet = input("Enter the input alphabet: ").split()
    transitions_input = input("Enter state-transitions function (current state, input character, next state): ").split()
    transitions = [tuple(t.strip()[1:-1].split(',')) for t in transitions_input]
    initial_states = input("Enter a set of initial states: ").split()
    final_states = input("Enter a set of final states: ").split()

    dfa_states, dfa_alphabet, dfa_transitions, dfa_initial_state, dfa_final_states = nfa_to_dfa(
        states, alphabet, transitions, initial_states, final_states)

    # Преобразуйте наборы состояний в ожидаемый формат
    dfa_states_str = [''.join(sorted(state)) for state in dfa_states]
    dfa_final_states_str = [''.join(sorted(state)) for state in dfa_final_states]

    print("DFA:")
    print("Set of states: " + ', '.join(dfa_states_str))
    print("Input alphabet: " + ', '.join(dfa_alphabet))
    print("State-transitions function:")
    for transition in dfa_transitions:
        current_state = ''.join(sorted(transition[0]))
        next_state = ''.join(sorted(transition[2]))
        print(f'D({current_state}, {transition[1]}) = {next_state}')
    initial_state_str = ''.join(sorted(dfa_initial_state))
    print("Initial states: " + initial_state_str)
    print("Final states: " + ', '.join(dfa_final_states_str))


if __name__ == "__main__":
    main()


'''
1 2 3
a b
(1,a,1) (1,a,2) (1,b,3) (2,a,2) (2,b,1) (2,b,3) (3,a,3) (3,b,3)
1
3
'''
