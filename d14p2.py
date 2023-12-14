from enum import Enum, auto
from pathlib import Path


class Direction(Enum):
    NORTH = auto()
    WEST = auto()
    SOUTH = auto()
    EAST = auto()


def transform(mat, m, n, _dir):
    """ Kinda gross... could be simplified but meh """
    if _dir == Direction.NORTH:
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
    elif _dir == Direction.WEST:
        last_hashtag = [-1] * m
        count_stones = [0] * m
        for c in range(n):
            for r in range(m):
                if mat[r][c] == '#':
                    last_hashtag[r] = c
                    count_stones[r] = 0
                elif mat[r][c] == 'O':
                    new_c = last_hashtag[r] + count_stones[r] + 1
                    if new_c < c:
                        mat[r][new_c] = 'O'
                        mat[r][c] = '.'
                    count_stones[r] += 1
    elif _dir == Direction.SOUTH:
        last_hashtag = [n] * n
        count_stones = [0] * n
        for r in range(m - 1, -1, -1):
            for c in range(n - 1, -1, -1):
                if mat[r][c] == '#':
                    last_hashtag[c] = r
                    count_stones[c] = 0
                elif mat[r][c] == 'O':
                    new_r = last_hashtag[c] - count_stones[c] - 1
                    if new_r > r:
                        mat[new_r][c] = 'O'
                        mat[r][c] = '.'
                    count_stones[c] += 1
    elif _dir == Direction.EAST:
        last_hashtag = [m] * m
        count_stones = [0] * m
        for c in range(n - 1, -1, -1):
            for r in range(m - 1, -1, -1):
                if mat[r][c] == '#':
                    last_hashtag[r] = c
                    count_stones[r] = 0
                elif mat[r][c] == 'O':
                    new_c = last_hashtag[r] - count_stones[r] - 1
                    if new_c > c:
                        mat[r][new_c] = 'O'
                        mat[r][c] = '.'
                    count_stones[r] += 1

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
    for i in range(N):
        for _dir in [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]:
            transform(mat, m, n, _dir)
        state = get_state(mat, m, n)
        if state in states:
            break

        states[state] = i + 1
        scores.append(get_score(mat, m, n))

    offset = states[state]
    period = i + 1 - offset
    print(offset, period)
    print(scores[offset + (N - offset) % period])

