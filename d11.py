from bisect import bisect_left
from pathlib import Path


if __name__ == '__main__':
    with Path('d11_input.txt').open() as f:
        matrix = [list(row.strip()) for row in f]

    m = len(matrix)
    n = len(matrix[0])

    empty_rows = []
    empty_cols = []
    for r, row in enumerate(matrix):
        if all(elem == '.' for elem in row):
            empty_rows.append(r)
    for c in range(n):
        if all(matrix[r][c] == '.' for r in range(m)):
            empty_cols.append(c)

    coords = []
    for r in range(m):
        for c in range(n):
            if matrix[r][c] == '#':
                coords.append((r, c))

    ret = [0, 0]
    mult = [1, 999999]
    for i in range(len(coords)):
        ri, ci = coords[i]
        for j in range(i + 1, len(coords)):
            rj, cj = coords[j]
            rlo = min(ri, rj)
            rhi = ri + rj - rlo
            clo = min(ci, cj)
            chi = ci + cj - clo
            for k in range(len(ret)):
                ret[k] += rhi - rlo + chi - clo + \
                    mult[k] * (bisect_left(empty_rows, rhi) - bisect_left(empty_rows, rlo) +
                               bisect_left(empty_cols, chi) - bisect_left(empty_cols, clo))

    for entry in ret:
        print(entry)

