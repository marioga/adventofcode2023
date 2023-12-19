from collections import deque
from pathlib import Path

DIRS = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1),
}


if __name__ == '__main__':
    path = [(0, 0)]
    min_r = max_r = min_c = max_c = 0

    with Path('d18_input.txt').open() as f:
        for row in f:
            _dir, num, _ = row.strip().split()
            dr, dc = DIRS[_dir]
            r, c = path[-1]
            for _ in range(int(num)):
                r += dr
                c += dc
                path.append((r, c))
                min_r = min(min_r, r)
                max_r = max(max_r, r)
                min_c = min(min_c, c)
                max_c = max(max_c, c)

    m = max_r - min_r + 1
    n = max_c - min_c + 1
    mat = [['.'] * n for _ in range(m)]
    for r, c in path:
        mat[r - min_r][c - min_c] = '#'

    queue = deque()

    for r in range(m):
        for c in [0, n - 1]:
            if mat[r][c] == '.':
                queue.append((r, c))

    for c in range(1, n - 1):
        for r in [0, m - 1]:
            if mat[r][c] == '.':
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and mat[nr][nc] == '.':
                mat[nr][nc] = '*'
                queue.append((nr, nc))

    print(sum(int(mat[r][c] in '.#') for r in range(m) for c in range(n)))

