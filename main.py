import csv
import random
import time

def neighbor_periodic(state, index):
    left = state[index-1] if index > 0 else state[-1]
    right = state[index+1] if index < len(state) - 1 else state[0]
    return left, right

def neighbor_absorbing(state, index):
    left = state[index-1] if index > 0 else 0
    right = state[index+1] if index < len(state) - 1 else 0
    return left, right

def get_user_intput():
    try:
        size = int(input("Podaj liczbę komórek: "))
        iterations = int(input("Podaj liczbę iteracji: "))
        if size <=0 or iterations <= 0:
            raise ValueError("Wartości muszą być większe od 0.")
        return size, iterations
    except ValueError as e:
        print("Błąd: ", e)
        return get_user_intput()

def binary_rule(rule_number):
    return f"{rule_number:08b}"

def apply_rule(rule_binary, left, centre, right):
    neighborhood = f"{left}{centre}{right}"

    mapping = {
        '111': 0,
        '110': 1,
        '101': 2,
        '100': 3,
        '011': 4,
        '010': 5,
        '001': 6,
        '000': 7
    }
    return int(rule_binary[mapping[neighborhood]])

def save_to_csv(results, filename="wyniki_automatu.csv"):
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)
    print(f"Wyniki zapisano do {filename}")

def display_state(state):
    display = ''.join('■' if cell == 1 else ' ' for cell in state)
    print(display)

def main():
    rules = []
    rules.append(41)
    rules.append(46)
    rules.append(57)
    rules.append(190)
    rules_binary = [binary_rule(rule) for rule in rules]

    size, iterations = get_user_intput()
    state = [random.randint(0,1) for _ in range(size)]
    results = [state.copy()]

    display_state(state)
    time.sleep(0.5)

    for _ in range(iterations):
        new_state = []
        for index in range(size):
            left, right = neighbor_periodic(state, index)
            center = state[index]
            new_value = apply_rule(rules_binary[0], left, center, right)
            new_state.append(new_value)

        state = new_state
        results.append(new_state)

        display_state(state)
        time.sleep(0.5)

    save_to_csv(results)

if __name__ == "__main__":
    main()
