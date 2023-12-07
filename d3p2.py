from collections import defaultdict
from pathlib import Path


if __name__ == '__main__':
    mat = []
    with Path('d3_input.txt').open() as f:
        for row in f:
            mat.append(list(row.strip()))

    star_adjacent = defaultdict(list)
    for r, row in enumerate(mat):
        i = 0
        while i < len(row):
            if not row[i].isdigit():
                i += 1
                continue

            val = int(row[i])
            j = i + 1
            while j < len(row) and row[j].isdigit():
                val = 10 * val + int(row[j])
                j += 1

            if i > 0 and row[i - 1] == '*':
                star_adjacent[(r, i - 1)].append(val)

            if j < len(row) and row[j] == '*':
                star_adjacent[(r, j)].append(val)

            for k in range(max(i - 1, 0), min(j, len(row) - 1) + 1):
                if r > 0 and mat[r - 1][k] == '*':
                    star_adjacent[(r - 1, k)].append(val)

                if r < len(mat) - 1 and mat[r + 1][k] == '*':
                    star_adjacent[(r + 1, k)].append(val)

            i = j

    ret = 0
    for values in star_adjacent.values():
        if len(values) == 2:
            ret += values[0] * values[1]

    print(ret)

