if __name__ == '__main__':
    with open('d8-input.txt') as f:
        lines = f.readlines()

    grid = [[int(t) for t in line.strip()] for line in lines]  # rows / columns
    i_start = j_start = 1
    i_end = len(grid) - 1
    j_end = len(grid[0]) - 1
    # initialize for outer lines of trees, only for the ones taller than 0
    visible = len([t > 0 for t in grid[0]]) + len([t > 0 for t in grid[-1]]) + \
              len([t > 0 for t in (grid[0][i] for i in range(1, i_end))]) + \
              len([t > 0 for t in (grid[-1][i] for i in range(1, i_end))])
    max_scenic_score = 0

    for i in range(i_start, i_end):
        for j in range(j_start, j_end):
            before_column = all(grid[r][j] < grid[i][j] for r in range(0, i))
            after_column = all(grid[r][j] < grid[i][j] for r in range(i + 1, i_end + 1))
            before_row = all(grid[i][c] < grid[i][j] for c in range(0, j))
            after_row = all(grid[i][c] < grid[i][j] for c in range(j + 1, j_end + 1))
            if any([before_column, before_row, after_column, after_row]):
                visible += 1
    print(f'[>] Number of visible trees: {visible}')

    for i in range(0, i_end + 1):
        for j in range(0, j_end + 1):
            try:
                blocker_before_column = max((r for r in range(0, i) if grid[r][j] >= grid[i][j]))
            except ValueError:
                blocker_before_column = 0
            try:
                blocker_after_column = min((r for r in range(i + 1, i_end + 1) if grid[r][j] >= grid[i][j]))
            except ValueError:
                blocker_after_column = i_end
            try:
                blocker_before_row = max((c for c in range(0, j) if grid[i][c] >= grid[i][j]))
            except ValueError:
                blocker_before_row = 0
            try:
                blocker_after_row = min((c for c in range(j + 1, j_end + 1) if grid[i][c] >= grid[i][j]))
            except ValueError:
                blocker_after_row = j_end
            tree_scenic_score = (i - blocker_before_column) * \
                                (blocker_after_column - i) * \
                                (j - blocker_before_row) * \
                                (blocker_after_row - j)
            if tree_scenic_score > max_scenic_score:
                max_scenic_score = tree_scenic_score
    print(f'[>] Maximum scenic score is: {max_scenic_score}')
