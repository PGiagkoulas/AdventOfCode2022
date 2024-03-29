import math

MOVES = {
    'U': (0, 1)
    , 'D': (0, -1)
    , 'R': (1, 0)
    , 'L': (-1, 0)
    , 'UR': (1, 1)
    , 'UL': (-1, 1)
    , 'DR': (1, -1)
    , 'DL': (-1, -1)
}

DY_DY_VECTOR_MOVE_MAP = {v: k for k, v in MOVES.items()}

HOR_VERT_MOVES = ['U', 'D', 'R', 'L']

ALL_BOARD_POSITIONS = [(j, i) for i in range(13, -13, -1) for j in range(-13, 13, 1)]


def initialize_parameters():
    return (0, 0), (0, 0), (0, 0), 0, [(0, 0)], [(0, 0)], []


def calculate_head_tail_distance(h: tuple[int, int], t: tuple[int, int]) -> int:
    return max(abs(h[0] - t[0]), abs(h[1] - t[1]))


def calculate_dx_dy_vector(p1: tuple[int, int], p2: tuple[int, int]) -> tuple[int, int]:
    return (p1[0] - p2[0]), (p1[1] - p2[1])


def calculate_dx_dy_distance(p1: tuple[int, int], p2: tuple[int, int]) -> float:
    return math.sqrt(math.pow(p2[0] - p1[0], 2) + math.pow(p2[1] - p1[1], 2))


def calculate_move_distances(p1: tuple[int, int], p2: tuple[int, int]) -> dict[str, float]:
    return {m: calculate_dx_dy_distance((p1[0]+s[0], p1[1]+s[1]), p2) for m, s in MOVES.items()}


def get_dict_key_min_value(d: dict) -> str:
    min_dist = min(d.values())
    min_dist_ind = list(d.values()).index(min_dist)
    return list(d.keys())[min_dist_ind]


def get_least_distance_move(p1: tuple[int, int], p2: tuple[int, int]) -> str:
    moves_distances = calculate_move_distances(p1, p2)
    return get_dict_key_min_value(moves_distances)


def calc_tail_step_update(step_history: list[str], step_dir: str) -> tuple[bool, str]:
    if len(step_history) > 0:
        latest_step_dir, latest_step_dist = step_history[-1].split(' ')
        if latest_step_dir == step_dir:
            return False, latest_step_dir + ' ' + str(int(latest_step_dist)+1)
        else:
            return True, step_dir + ' 1'
    else:
        return True, step_dir + ' 1'


if __name__ == '__main__':
    with open('d9-input.txt') as f:
        steps = f.readlines()
    steps = [s.strip() for s in steps]
    print(steps)
    knot_positions = [(0, 0)] * 10
    num_unique_tail_pos = 0
    # Assume the head and the tail both start at the same position, overlapping.
    # Rope with 10 knots
    # n moves, check distance and possibly update n+1
    # if n+1 was updated, do again for n+1 and n+2 ...

    # take all knot movements one by one, as every one's movements rely only on the knot before it
    for i in range(1, 10):
        start_pos, head_pos, tail_pos, head_tail_distance, all_head_pos, all_tail_pos, all_tail_steps \
            = initialize_parameters()
        # last_head_follow_pos = None
        for step in steps:
            direction = step.split(' ')[0]
            distance = int(step.split(' ')[1])
            # print(f"[>] Moving {direction} for {distance} spaces")
            for _ in range(distance):
                # 1. update last head position to follow
                last_head_follow_pos = head_pos
                # 2. move head
                head_pos = (head_pos[0] + MOVES[direction][0], head_pos[1] + MOVES[direction][1])
                all_head_pos.append(head_pos)
                dist = calculate_head_tail_distance(head_pos, tail_pos)
                print(f"  - New head position: {head_pos} with {dist} distance from tail")
                # 3. check distance to tail
                if dist > 1:
                    # 3a. not adjacent -> calculate tail step
                    tail_step_dir = get_least_distance_move(tail_pos, head_pos)
                    new_step, step = calc_tail_step_update(all_tail_steps, tail_step_dir)
                    if new_step:
                        all_tail_steps.append(step)
                    else:
                        all_tail_steps[-1] = step

                    tail_pos = (tail_pos[0] + MOVES[tail_step_dir][0], tail_pos[1] + MOVES[tail_step_dir][1])
                    print(f"  - New tail position: {tail_pos} after performing step {tail_step_dir}")
                    all_tail_pos.append(tail_pos)
        steps = all_tail_steps  # steps for next head, based on steps of tail
        knot_positions[i-1] = head_pos  # positions of knots after finished moving

        num_unique_head_pos = len(set(all_head_pos))
        num_unique_tail_pos = len(set(all_tail_pos))
        print(f"[>] Head knot {i} visited {num_unique_head_pos} positions at least once")
        print(f"[>] Tail knot {i+1} steps {all_tail_steps}")
    print(f"[>] Last tail knot visited {num_unique_tail_pos} unique positions")
