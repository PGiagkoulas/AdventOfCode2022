from string import ascii_lowercase as alc
from string import ascii_uppercase as auc
from collections import Counter


PRIORITIES = {c: i+1 for i, c in enumerate(alc+auc)}


if __name__ == '__main__':
    with open('d3-input.txt') as f:
        rucksack_contents = f.readlines()
    rucksack_contents = [rc.strip() for rc in rucksack_contents]
    all_lengths = [len(c) for c in rucksack_contents]

    print(f"[>] All even sizes: {all(l%2==0 for l in all_lengths)}")

    double_chars = []
    for contents in rucksack_contents:
        comp1 = contents[:len(contents)//2]
        comp2 = contents[len(contents)//2:]
        common_char = [c for c in comp1 if c in comp2][0]
        
        # print(f"[>] Found common character: {common_char}")

        double_chars.append(common_char)
    res = sum([PRIORITIES[c] for c in double_chars])
    print(f"[>] Total priority score of all double items: {res}")

    unique_rucksack_contents = [list(set(c)) for c in rucksack_contents]
    elf_group_contents = [unique_rucksack_contents[i] + unique_rucksack_contents[i+1] + unique_rucksack_contents[i+2]
                            for i in range(0, len(unique_rucksack_contents), 3)]
    all_counters = [Counter(egc) for egc in elf_group_contents]
    all_badges = [max(c, key=c.get) for c in all_counters]
    res = sum([PRIORITIES[c] for c in all_badges])
    print(f"[>] Total priority score of all badge items: {res}")


        
        
    

