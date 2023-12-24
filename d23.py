import sys
from collections import deque
from pathlib import Path

DIRS = {
    '.': [(-1, 0), (1, 0), (0, -1), (0, 1)],
    '<': [(0, -1)],
    '>': [(0, 1)],
    'v': [(1, 0)],
    '^': [(-1, 0)],
}


def get_longest_path(mat, m, n, start, end, longest_path, curr=None, visited=None):
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
    for dr, dc in DIRS[mat[r][c]]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < m and 0 <= nc < n and mat[nr][nc] != '#' and (nr, nc) not in visited:
            visited.add((nr, nc))
            curr.append((nr, nc))
            get_longest_path(mat, m, n, start, end, longest_path, curr, visited)
            # backtrack
            visited.remove((nr, nc))
            curr.pop()


def get_condensed_graph(mat, m, n, start, end):
    graph = {start: {}, end: {}}
    for r in range(m):
        for c in range(n):
            if mat[r][c] == '#':
                continue

            neigh = 0
            for dr, dc in DIRS['.']:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and mat[nr][nc] != '#':
                    neigh += 1

            if neigh >= 3:
                graph[(r, c)] = {}

    vertices = set(graph.keys())
    for r, c in vertices:
        seen = {(r, c)}
        queue = deque([(0, r, c)])
        while queue:
            d, cr, cc = queue.popleft()
            for dr, dc in DIRS['.']:
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < m and 0 <= nc < n and mat[nr][nc] != '#' and (nr, nc) not in seen:
                    if (nr, nc) in vertices:
                        graph[(r, c)][(nr, nc)] = d + 1
                    else:
                        queue.append((d + 1, nr, nc))
                    seen.add((nr, nc))

    return graph


def get_longest_path_in_graph(vertex, graph, end, longest_path, dist=0, visited=None):
    if visited is None:
        visited = {start}

    if vertex == end:
        if not longest_path:
            longest_path.append(dist)
        elif longest_path[0] < dist:
            longest_path[0] = dist
        return

    for next_vertex, weight in graph[vertex].items():
        if next_vertex not in visited:
            visited.add(next_vertex)
            get_longest_path_in_graph(next_vertex, graph, end, longest_path, dist + weight, visited)
            # backtrack
            visited.remove(next_vertex)


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
    get_longest_path(mat, m, n, start, end, longest_path)
    print(longest_path[0])

    # Part 2
    graph = get_condensed_graph(mat, m, n, start, end)
    longest_path = []
    get_longest_path_in_graph(start, graph, end, longest_path)
    print(longest_path[0])

