def move_cargo_lifo(stacks: list[list[str]], actions: list[list[str]]) -> list[list[str]]:
    for crates_to_move, from_stack, to_stack in actions:
        for ctm in range(int(crates_to_move)):
            popped = stacks[int(from_stack) - 1].pop()
            stacks[int(to_stack) - 1].append(popped)
    return stacks


def move_cargo_stack(stacks: list[list[str]], actions: list[list[str]]) -> list[list[str]]:
    for crates_to_move, from_stack, to_stack in actions:
        stacks[int(to_stack)-1].extend(stacks[int(from_stack)-1][-int(crates_to_move):])
        for ctm in range(int(crates_to_move)):
            stacks[int(from_stack) - 1].pop()
    return stacks


if __name__ == '__main__':
    with open('d5-input.txt') as f:
        lines = f.readlines()
    cargo_setup = lines[:8]
    cargo_size = int(lines[8].strip()[-1])
    cargo_setup = [csu.strip().replace('    ', ' ').replace(' ', '|').split('|') for csu in cargo_setup]
    rearrangement_process = lines[10:]

    cargo_by_stack = [[] for _ in range(cargo_size)]
    for line in reversed(cargo_setup):
        [cargo_by_stack[s].append(line[s]) for s in range(cargo_size) if line[s] != '']

    process_actions = [s.strip().replace('move ', '').replace('from ', '').replace('to ', '').split(' ')
                       for s in rearrangement_process]

    # cargo_by_stack_lifo = cargo_by_stack
    # cargo_by_stack_lifo = move_cargo_lifo(cargo_by_stack_lifo, process_actions)
    # top_of_cargo = ''.join(c[-1] for c in cargo_by_stack_lifo).replace('[', '').replace(']', '')
    # print(f'Top crates on each stack using lifo: {top_of_cargo}')

    cargo_by_stack_stacked = cargo_by_stack
    cargo_by_stack_stacked = move_cargo_stack(cargo_by_stack_stacked, process_actions)
    top_of_cargo = ''.join(c[-1] for c in cargo_by_stack_stacked).replace('[', '').replace(']', '')
    print(f'Top crates on each stack using stacks: {top_of_cargo}')
