def get_elf_assignments(pair: str) -> tuple[int, int]:
    elf1, elf2 = pair.split(',')
    elf1 = (int(elf1.split('-')[0]), int(elf1.split('-')[1]))
    elf2 = (int(elf2.split('-')[0]), int(elf2.split('-')[1]))
    return elf1, elf2

if __name__ == '__main__':
    with open('d4-input.txt') as f:
        lines = f.readlines()
    lines = [line.strip() for line in lines]
    fully_contained_count = 0
    for pair in lines:
        elf1, elf2 = get_elf_assignments(pair)
        one_fully_two = (elf1[0] <= elf2[0]) and (elf1[1] >= elf2[1])
        two_fully_one = (elf2[0] <= elf1[0]) and (elf2[1] >= elf1[1])
        if one_fully_two or two_fully_one:
            fully_contained_count += 1
    print(f"[>] Found {fully_contained_count} fully overlapping pair assignments")

    ovelapping_count = 0
    for pair in lines:
        elf1, elf2 = get_elf_assignments(pair)
        one_part_two = elf1[0] <= elf2[0] <= elf1[1]
        two_part_one = elf2[0] <= elf1[0] <= elf2[1]
        if one_part_two or two_part_one:
            ovelapping_count += 1
    print(f"[>] Found {ovelapping_count} overlapping pair assignments")
