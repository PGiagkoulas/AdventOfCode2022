

if __name__ == '__main__':
    with open('d1-input.txt') as f:
        lines = f.readlines()
    lines = [int(line.strip()) if len(line) > 1 else line for line in lines]
    lines.append('\n')

    elf_start = 0
    elf_end = -1  # initialization
    elf_calories = []
    while elf_end < len(lines)-1:
        elf_start = elf_end + 1
        elf_end = lines.index('\n', elf_start+1)
        elf_calories.append(sum(lines[elf_start:elf_end]))
    print(f"[>] Top elf calories: {max(elf_calories)}")
    
    top_n_calories = 0
    n = 3
    for i in range(0,n):
        top_cal = max(elf_calories)
        top_n_calories += top_cal
        elf_calories.remove(top_cal)

    print(f"[>] Sum of top-{n} elf calories: {top_n_calories}")
        
