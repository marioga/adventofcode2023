from collections import deque
from pathlib import Path

#  1
# 0X2
#  3
DIRS = [0, -1, 0, 1, 0]

COMING_FROM = {
    '|': {1, 3},
    '-': {0, 2},
    'L': {3, 0},
    'J': {2, 3},
    '7': {1, 2},
    'F': {0, 1},
}


if __name__ == '__main__':
    matrix = []
    with Path('d10_input.txt').open() as f:
        s_r = s_c = None
        for r, line in enumerate(f):
            row = []
            for c, ch in enumerate(line.strip()):
                row.append(ch)
                if ch == 'S':
                    s_r, s_c = r, c
            matrix.append(row)

        m = len(matrix)
        n = len(matrix[0])

        dists = {(s_r, s_c): 0}
        queue = deque()
        for idx in range(4):
            dr, dc = DIRS[idx:idx + 2]
            if 0 <= s_r + dr < m and 0 <= s_c + dc < n:
                ch = matrix[s_r + dr][s_c + dc]
                if idx in (ch_dirs := COMING_FROM.get(ch, set())):
                    other_idx = next(iter(ch_dirs - {idx}))
                    queue.append(((s_r + dr, s_c + dc), (other_idx + 2) % 4))
                    dists[(s_r + dr, s_c + dc)] = 1

        max_dist = 0
        while queue:
            (r, c), idx = queue.popleft()
            max_dist = max(dists[(r, c)], max_dist)
            dr, dc = DIRS[idx:idx + 2]
            if 0 <= r + dr < m and 0 <= c + dc < n and (r + dr, c + dc) not in dists:
                ch = matrix[r + dr][c + dc]
                if idx in (ch_dirs := COMING_FROM.get(ch, set())):
                    other_idx = next(iter(ch_dirs - {idx}))
                    queue.append(((r + dr, c + dc), (other_idx + 2) % 4))
                    dists[(r + dr, c + dc)] = dists[(r, c)] + 1

        print(max_dist)

        for r in range(m):
            for c in range(n):
                if (r, c) not in dists:
                    matrix[r][c] = '.'

        # pick a node adjacent to 'S' and a direction to start
        rr, cc = next(k for k, v in dists.items() if v == 1)
        for idx in COMING_FROM[matrix[rr][cc]]:
            dr, dc = DIRS[idx:idx + 2]
            if 0 <= rr - dr < m and 0 <= cc - dc < n and (rr - dr, cc - dc) != (s_r, s_c):
                break
        _dir = (idx + 2) % 4

        right_hand = {}
        prev = {}
        # Ugh... this is gross but whatever
        while (rr, cc) != (s_r, s_c):
            if matrix[rr][cc] == '|':
                if 0 <= cc + 1 < n and matrix[rr][cc + 1] == '.':
                    right_hand[(rr, cc + 1)] = _dir == 1
                if 0 <= cc - 1 < n and matrix[rr][cc - 1] == '.':
                    right_hand[(rr, cc - 1)] = _dir == 3

                next_rr, next_cc = (rr + 1 if _dir == 3 else rr - 1), cc
            elif matrix[rr][cc] == '-':
                if 0 <= rr + 1 < m and matrix[rr + 1][cc] == '.':
                    right_hand[(rr + 1, cc)] = _dir == 2
                if 0 <= rr - 1 < m and matrix[rr - 1][cc] == '.':
                    right_hand[(rr - 1, cc)] = _dir == 0

                next_rr, next_cc = rr, (cc + 1 if _dir == 2 else cc - 1)
            elif matrix[rr][cc] == 'L':
                if 0 <= cc - 1 < n and matrix[rr][cc - 1] == '.':
                    right_hand[(rr, cc - 1)] = _dir == 2
                if 0 <= rr + 1 < m and matrix[rr + 1][cc] == '.':
                    right_hand[(rr + 1, cc)] = _dir == 2

                next_rr, next_cc = (rr, cc + 1) if _dir == 2 else (rr - 1, cc)
            elif matrix[rr][cc] == 'J':
                 if 0 <= cc + 1 < n and matrix[rr][cc + 1] == '.':
                    right_hand[(rr, cc + 1)] = _dir == 1
                 if 0 <= rr + 1 < m and matrix[rr + 1][cc] == '.':
                    right_hand[(rr + 1, cc)] = _dir == 1

                 next_rr, next_cc = (rr - 1, cc) if _dir == 1 else (rr, cc - 1)
            elif matrix[rr][cc] == '7':
                if 0 <= cc + 1 < n and matrix[rr][cc + 1] == '.':
                    right_hand[(rr, cc + 1)] = _dir == 0
                if 0 <= rr - 1 < m and matrix[rr - 1][cc] == '.':
                    right_hand[(rr - 1, cc)] = _dir == 0

                next_rr, next_cc = (rr, cc - 1) if _dir == 0 else (rr + 1, cc)
            elif matrix[rr][cc] == 'F':
                if 0 <= cc - 1 < n and matrix[rr][cc - 1] == '.':
                    right_hand[(rr, cc - 1)] = _dir == 3
                if 0 <= rr - 1 < m and matrix[rr - 1][cc] == '.':
                    right_hand[(rr - 1, cc)] = _dir == 3

                next_rr, next_cc = (rr + 1, cc) if _dir == 3 else (rr, cc + 1)

            rr, cc = next_rr, next_cc
            if _dir == 0:
                if matrix[rr][cc] == 'L':
                    _dir = 1
                elif matrix[rr][cc] == 'F':
                    _dir = 3
            elif _dir == 1:
                if matrix[rr][cc] == 'F':
                    _dir = 2
                elif matrix[rr][cc] == '7':
                    _dir = 0
            elif _dir == 2:
                if matrix[rr][cc] == '7':
                    _dir = 3
                elif matrix[rr][cc] == 'J':
                    _dir = 1
            elif _dir == 3:
                if matrix[rr][cc] == 'J':
                    _dir = 0
                elif matrix[rr][cc] == 'L':
                    _dir = 2

        queue = deque(right_hand.keys())
        while queue:
            r, c = queue.popleft()
            for idx in range(4):
                dr, dc = DIRS[idx:idx + 2]
                if 0 <= r + dr < m and 0 <= c + dc < n and matrix[r + dr][c + dc] == '.' and (r + dr, c + dc) not in right_hand:
                    right_hand[(r + dr, c + dc)] = right_hand[(r, c)]
                    queue.append((r + dr, c + dc))

        for r in range(m):
            for c in range(n):
                # assumes main loop doesn't cover entire border of matrix
                if (r in {0, m - 1} or c in {0, n - 1}) and (r, c) in right_hand:
                    right_hand_outside = right_hand[(r, c)]

        for r in range(m):
            for c in range(n):
                if (r, c) in right_hand:
                    print('O' if right_hand[(r, c)] == right_hand_outside else 'I', end='')
                else:
                    print(matrix[r][c], end='')
            print()

        print(sum(1 for v in right_hand.values() if v != right_hand_outside))

