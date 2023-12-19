import heapq
import math
from pathlib import Path

# Directions
#  1
# 0X2
#  3

DIR_R = [0, -1, 0, 1]
DIR_C = [-1, 0, 1, 0]


def get_heat_loss(mat, r, c, new_dir, new_r, new_c):
    dr, dc = DIR_R[new_dir], DIR_C[new_dir]
    ret = 0
    curr_r, curr_c = r, c
    while (curr_r, curr_c) != (new_r, new_c):
        curr_r, curr_c = curr_r + dr, curr_c + dc
        ret += mat[curr_r][curr_c]
    return ret


def get_minimum_heat_loss(mat, m, n, stride_min, stride_max):
    graph = {}
    for r in range(m):
        for c in range(n):
            for _dir in range(4):
                curr = graph[(_dir, r, c)] = []
                for new_dir in range(4):
                    if new_dir == _dir or abs(_dir - new_dir) == 2:
                        # Gotta turn right or left
                        continue

                    dr, dc = DIR_R[new_dir], DIR_C[new_dir]
                    for stride in range(stride_min, stride_max + 1):
                        new_r, new_c = r + stride * dr, c + stride * dc
                        if 0 <= new_r < m and 0 <= new_c < n:
                            curr.append((new_dir, new_r, new_c))

    dists = {(_dir, 0, 0): 0 for _dir in range(4)}
    pq = [(0, (2, 0, 0)), (0, (3, 0, 0))]
    while pq:
        dist, (_dir, r, c) = heapq.heappop(pq)
        if dist > dists[(_dir, r, c)]:
            continue

        if (r, c) == (m - 1, n - 1):
            return dist

        for new_dir, new_r, new_c in graph.get((_dir, r, c), []):
            new_dist = dist + get_heat_loss(mat, r, c, new_dir, new_r, new_c)
            if new_dist < dists.get((new_dir, new_r, new_c), math.inf):
                dists[(new_dir, new_r, new_c)] = new_dist
                heapq.heappush(pq, (new_dist, (new_dir, new_r, new_c)))

    raise Exception("Should never get here")


if __name__ == '__main__':
    with Path('d17_input.txt').open() as f:
        mat = []
        for row in f:
            mat.append(list(map(int, row.strip())))

    m = len(mat)
    n = len(mat[0])

    print(get_minimum_heat_loss(mat, m, n, 1, 3))
    print(get_minimum_heat_loss(mat, m, n, 4, 10))

