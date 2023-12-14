from pathlib import Path


def transform(mat, m, n):
    last_hashtag = [-1] * n
    count_stones = [0] * n
    for r in range(m):
        for c in range(n):
            if mat[r][c] == '#':
                last_hashtag[c] = r
                count_stones[c] = 0
            elif mat[r][c] == 'O':
                new_r = last_hashtag[c] + count_stones[c] + 1
                if new_r < r:
                    mat[new_r][c] = 'O'
                    mat[r][c] = '.'
                count_stones[c] += 1


def rotate(mat, m, n):
    ret = [[None] * m for _ in range(n)]
    for r in range(m):
        for c in range(n):
            ret[c][m - 1 - r] = mat[r][c]
    return ret


def get_state(mat, m, n):
    ret = []
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 'O':
                ret.append(r * n + c)
    return tuple(ret)


def get_score(mat, m, n):
    score = 0
    for r in range(m):
        for c in range(n):
            if mat[r][c] == 'O':
                score += m - r
    return score


if __name__ == '__main__':
    with Path('d14_input.txt').open() as f:
        mat = []
        for row in f:
            mat.append(list(row.strip()))

    m = len(mat)
    n = len(mat[0])
    N = 10**9
    states = {get_state(mat, m, n): 0}
    scores = [get_score(mat, m, n)]
    offset = period = None
    for step in range(1, N + 1):
        for _ in range(4):
            transform(mat, m, n)
            mat = rotate(mat, m, n)

        if (state := get_state(mat, m, n)) in states:
            offset = states[state]
            period = step - offset
            break

        states[state] = step
        scores.append(get_score(mat, m, n))

    print(offset, period)
    print(scores[offset + (N - offset) % period])

