import sys
from pathlib import Path

DIRS = {
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '<': [(0, -1)],
    '>': [(0, 1)],
    'v': [(1, 0)],
    '^': [(-1, 0)],
}


def get_paths(mat, m, n, start, end, longest_path, curr=None, visited=None, part1=True):
    if curr is None:
        curr = [start]
        visited = {start}
    elif curr[-1] == end:
        if not longest_path:
            longest_path.append(len(curr) - 1)
        elif longest_path[0] < len(curr) - 1:
            longest_path[0] = len(curr) - 1
        return

    r, c = curr[-1]
    _dirs = DIRS[mat[r][c]] if part1 else DIRS['.']
    for dr, dc in _dirs:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n and mat[nr][nc] != '#' and (nr, nc) not in visited:
            visited.add((nr, nc))
            curr.append((nr, nc))
            get_paths(mat, m, n, start, end, longest_path, curr, visited, part1)
            # backtrack
            visited.remove((nr, nc))
            curr.pop()


if __name__ == '__main__':
    with Path('d23_input.txt').open() as f:
        mat = []
        for row in f:
            mat.append(list(row.strip()))

    m = len(mat)
    n = len(mat[0])

    start = end = None
    for c in range(n):
        if mat[0][c] == '.':
            start = (0, c)
        if mat[m - 1][c] == '.':
            end = (m - 1, c)

    sys.setrecursionlimit(10000)

    # Part 1
    longest_path = []
    get_paths(mat, m, n, start, end, longest_path)
    print(longest_path[0])

    # Part 2... this is slow. Rethink at some point
    longest_path = []
    get_paths(mat, m, n, start, end, longest_path, part1=False)
    print(longest_path[0])
