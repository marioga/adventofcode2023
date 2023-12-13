from pathlib import Path


def get_score(pattern, diff_count=0):
    m = len(pattern)
    n = len(pattern[0])

    for c in range(n - 1):
        i = 0
        diff = 0
        while c - i >= 0 and c + 1 + i < n:
            for r in range(m):
                if pattern[r][c - i] != pattern[r][c + 1 + i]:
                    diff += 1
                    if diff > diff_count:
                        break
            if diff > diff_count:
                break
            i += 1
        if diff == diff_count:
            return c + 1

    for r in range(m - 1):
        i = 0
        diff = 0
        while r - i >= 0 and r + 1 + i < m:
            for c in range(n):
                if pattern[r - i][c] != pattern[r + 1 + i][c]:
                    diff += 1
                    if diff > diff_count:
                        break
            if diff > diff_count:
                break
            i += 1
        if diff == diff_count:
            return 100 * (r + 1)


if __name__ == '__main__':
    with Path('d13_input.txt').open() as f:
        sol1 = 0
        sol2 = 0
        pattern = []
        for row in f:
            line = row.strip()
            if not line:
                sol1 += get_score(pattern)
                sol2 += get_score(pattern, 1)
                pattern.clear()
                continue

            pattern.append(list(line.strip()))

        sol1 += get_score(pattern)
        sol2 += get_score(pattern, 1)

        print(sol1)
        print(sol2)

