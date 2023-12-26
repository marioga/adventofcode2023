from pathlib import Path

import numpy as np


MIN_XY = 200000000000000
MAX_XY = 400000000000000


def get_intersection(s0, v0, s1, v1):
    x0, y0 = s0
    vx0, vy0 = v0
    x1, y1 = s1
    vx1, vy1 = v1
    num = y0 - y1 + vy1 / vx1 * x1 - vy0 / vx0 * x0
    denom = vy1 / vx1 - vy0 / vx0
    if denom == 0:
        assert num != 0, "Same line!?!?!?"
        return None

    x = num / denom
    if (x - x0) / vx0 <= 0 or (x - x1) / vx1 <= 0:
        # crossed in the past for some stone
        return None

    y = y0 + vy0 / vx0 * (x - x0)
    return x, y



if __name__ == '__main__':
    slist = []
    vlist = []
    with Path('d24_input.txt').open() as f:
        for row in f:
            s, v = row.strip().split(' @ ')
            s = list(map(int, s.split(', ')))
            v = list(map(int, v.split(', ')))
            slist.append(s)
            vlist.append(v)

    n = len(slist)
    count = 0
    for i in range(n):
        for j in range(i):
            ret = get_intersection(slist[i][:-1], vlist[i][:-1], slist[j][:-1], vlist[j][:-1])
            if ret is None:
                continue

            if all(MIN_XY <= val <= MAX_XY for val in ret):
                count += 1
    # Part 1
    print(count)

    # Part 2
    # (x0 - x1) * VY + (vy0 - vy1) * X + (y1 - y0) * VX + (vx1 - vx0) * Y = y1 * vx1 - x1 * vy1 + x0 * vy0 - y0 * vx0
    x0, y0 = slist[0][:-1]
    vx0, vy0 = vlist[0][:-1]
    mat = []
    b = []
    for i in range(1, 5):
        xi, yi = slist[i][:-1]
        vxi, vyi = vlist[i][:-1]
        mat.append([x0 - xi, vy0 - vyi, yi - y0, vxi - vx0])
        b.append(yi * vxi - xi * vyi + x0 * vy0 - y0 * vx0)
    mat = np.array(mat)
    b = np.array(b).reshape(len(b), 1)
    sol = np.round(np.linalg.solve(mat, b)).astype(int)
    vy, x, vx, y = sol.squeeze().tolist()

    y0, z0 = slist[0][1:]
    vy0, vz0 = vlist[0][1:]
    mat = []
    b = []
    for i in range(1, 5):
        yi, zi = slist[i][1:]
        vyi, vzi = vlist[i][1:]
        mat.append([y0 - yi, vz0 - vzi, zi - z0, vyi - vy0])
        b.append(zi * vyi - yi * vzi + y0 * vz0 - z0 * vy0)
    mat = np.array(mat)
    b = np.array(b).reshape(len(b), 1)
    sol = np.round(np.linalg.solve(mat, b)).astype(int)
    vz, y2, vy2, z = sol.squeeze().tolist()
    assert y == y2 and vy == vy2

    print(x, y, z, vx, vy, vz)
    print(x + y + z)

