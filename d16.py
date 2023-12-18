from collections import deque
from pathlib import Path

# Directions:
#  1
# 0X2
#  3

OUTCOME = {
    '.': {
        0: [(0, (0, 1))],
        1: [(1, (1, 0))],
        2: [(2, (0, -1))],
        3: [(3, (-1, 0))],
    },
    '-': {
        0: [(0, (0, 1))],
        1: [(0, (0, 1)), (2, (0, -1))],
        2: [(2, (0, -1))],
        3: [(0, (0, 1)), (2, (0, -1))],
    },
    '|': {
        0: [(3, (-1, 0)), (1, (1, 0))],
        1: [(1, (1, 0))],
        2: [(3, (-1, 0)), (1, (1, 0))],
        3: [(3, (-1, 0))],
    },
    '/': {
        0: [(3, (-1, 0))],
        1: [(2, (0, -1))],
        2: [(1, (1, 0))],
        3: [(0, (0, 1))],
    },
    '\\': {
        0: [(1, (1, 0))],
        1: [(0, (0, 1))],
        2: [(3, (-1, 0))],
        3: [(2, (0, -1))],
    },
}


def get_energized(mat, m, n, initial_entrypoint=0, initial_x=0, initial_y=0, debug_print=False):
    queue = deque([(initial_entrypoint, (initial_x, initial_y))])
    visited = {(initial_x, initial_y): {initial_entrypoint}}
    while queue:
        entrypoint, (x, y) = queue.popleft()
        for new_entrypoint, (dx, dy) in OUTCOME[mat[x][y]][entrypoint]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < m and 0 <= new_y < n and \
                    new_entrypoint not in visited.get((new_x, new_y), set()):
                queue.append((new_entrypoint, (new_x, new_y)))
                visited.setdefault((new_x, new_y), set()).add(new_entrypoint)

    if debug_print:
        for x in range(m):
            for y in range(n):
                print('#' if (x, y) in visited else '.', end='')
            print()

    return len(visited)


if __name__ == '__main__':
    with Path('d16_input.txt').open() as f:
        mat = []
        for row in f:
            line = row.strip()
            mat.append(list(line))

    m = len(mat)
    n = len(mat[0])

    # Part 1
    print(get_energized(mat, m, n, debug_print=True))

    # Part 2
    best = -1
    for x in range(m):
        for y, entrypoint in [(0, 0), (n - 1, 2)]:
            best = max(best, get_energized(mat, m, n, entrypoint, x, y))
    for y in range(n):
        for x, entrypoint in [(0, 1), (m - 1, 3)]:
            best = max(best, get_energized(mat, m, n, entrypoint, x, y))

    print(best)

