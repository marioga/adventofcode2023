from collections import deque
from pathlib import Path

DIRS = (0, -1, 0, 1, 0)


def get_new_coords(n, world_x, world_y, nr, nc):
    if nr == -1:
        world_y -= 1
        nr = n - 1
    elif nr == n:
        world_y += 1
        nr = 0
    if nc == -1:
        world_x -= 1
        nc = n - 1
    elif nc == n:
        world_x += 1
        nc = 0

    return world_x, world_y, nr, nc


if __name__ == '__main__':
    mat = []
    with Path('d21_input.txt').open() as f:
        for row in f:
            mat.append(list(row.strip()))

    # Input matrix is square. Simplify things by assuming this everywhere
    n = len(mat)
    assert n == len(mat[0])

    queue = deque()
    dists = {}
    for r in range(n):
        for c in range(n):
            if mat[r][c] == 'S':
                mat[r][c] = '.'
                dists[(0, 0, r, c)] = 0
                queue.append((0, 0, 0, r, c))
                break

    LIMIT = 2
    while queue:
        dist, world_x, world_y, r, c = queue.popleft()
        for idx in range(4):
            dr, dc = DIRS[idx:idx + 2]
            nworld_x, nworld_y, nr, nc = get_new_coords(n, world_x, world_y, r + dr, c + dc)
            if mat[nr][nc] == '.' and (nworld_x, nworld_y, nr, nc) not in dists and -LIMIT <= nworld_x <= LIMIT and -LIMIT <= nworld_y <= LIMIT:
                dists[(nworld_x, nworld_y, nr, nc)] = dist + 1
                queue.append((dist + 1, nworld_x, nworld_y, nr, nc))

    validated = True
    for nworld_x in [-LIMIT, LIMIT]:
        for nworld_y in range(-LIMIT, LIMIT + 1):
            for r in range(n):
                for c in range(n):
                    if (nworld_x, nworld_y, r, c) in dists and \
                            dists[(nworld_x, nworld_y, r, c)] - dists[(nworld_x - nworld_x // LIMIT, nworld_y, r, c)] != n:
                        validated = False

    for nworld_y in [-LIMIT, LIMIT]:
        for nworld_x in range(-LIMIT, LIMIT + 1):
            for r in range(n):
                for c in range(n):
                    if (nworld_x, nworld_y, r, c) in dists and \
                            dists[(nworld_x, nworld_y, r, c)] - dists[(nworld_x, nworld_y - nworld_y // LIMIT, r, c)] != n:
                        validated = False

    assert validated

    DIST = 64
    sol = 0
    for r in range(n):
        for c in range(n):
            if (0, 0, r, c) in dists and (dist := dists[(0, 0, r, c)]) <= DIST and dist % 2 == DIST % 2:
                sol += 1

    # Part 1
    print(sol)

    # Part 2. Makes some assumptions; for example, that distances between instances of same point
    # grow by n as we move farther away from grid (except first few layers). This is validated
    # for second layer above. Answer below would need modifications if period would stabilize
    # beyong second layer from origin
    assert LIMIT == 2

    DIST = 26501365
    sol = 0
    # Count inside the initial square first
    valid_positions = set()
    for k, dist in dists.items():
        if k[0] == k[1] == 0:
            valid_positions.add(k[2:])
            # First condition is superfluous but whatever
            if dist <= DIST and dist % 2 == DIST % 2:
                sol += 1

    # Below works for odd n; could be tweaked for even n
    assert n % 2 == 1
    for pos in valid_positions:
        for quadrant in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
            initial = dists[(*quadrant, *pos)]
            cap = (DIST - initial) // n
            if initial % 2 == DIST % 2:
                sol += (cap // 2 + 1)**2
            else:
                sol += ((cap + 1) // 2) * ((cap + 1) // 2 + 1)

        for strip in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            initial = dists[(*strip, *pos)]
            cap = (DIST - initial) // n
            if initial % 2 == DIST % 2:
                sol += cap // 2 + 1
            else:
                sol += (cap + 1) // 2

    print(sol)

