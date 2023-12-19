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
    all_nums = 0

    with Path('d18_input.txt').open() as f:
        for row in f:
            _, _, rgb = row.strip().split()
            num = int(rgb[2:-2], 16)
            _dir = 'RDLU'[int(rgb[-2])]
            dr, dc = DIRS[_dir]
            r, c = path[-1]
            r = r + num * dr
            c = c + num * dc
            path.append((r, c))
            min_r = min(min_r, r)
            max_r = max(max_r, r)
            min_c = min(min_c, c)
            max_c = max(max_c, c)
            all_nums += num

    m = max_r - min_r + 1
    n = max_c - min_c + 1
    path = [(r - min_r, c - min_c) for r, c in path]

    area = 0
    boundary_points = 0
    for i in range(len(path) - 1):
        xp, yp = path[i]
        xn, yn = path[i + 1]
        boundary_points += abs(xn - xp) + abs(yn - yp)
        area += xp * yn - xn * yp

    # Shoelace + Pick's Theorem
    print(abs(area // 2) + boundary_points // 2 + 1)


