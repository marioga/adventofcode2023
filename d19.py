import math
from collections import deque
from pathlib import Path


class Node:
    def __init__(self, name):
        self.name = name
        self.transitions = []


class Condition:
    def __init__(self, target, idx=None, _min=None, _max=None):
        self.idx = idx
        self._min = _min
        self._max = _max
        self.target = target

    @classmethod
    def from_str(cls, _input):
        parts = _input.split(':')
        if len(parts) == 1:
            return cls(parts[0])

        assert len(parts) == 2
        sign = parts[0][1]
        assert sign in '<>'
        idx = 'xmas'.index(parts[0][0])
        val = int(parts[0][2:])
        if sign == '<':
            return cls(parts[1], idx, _max=val - 1)
        else:
            return cls(parts[1], idx, _min=val + 1)

    def matches(self, rating):
        if self.idx is None:
            return True

        val = rating[self.idx]
        return (self._min is None or val >= self._min) and (self._max is None or val <= self._max)


def traverse(nodes, rating, debug_print=True):
    path = ['in']
    curr = nodes['in']
    while True:
        for trans in curr.transitions:
            if trans.matches(rating):
                curr = nodes[trans.target]
                path.append(trans.target)
                break

        if curr.name in 'AR':
            break

    if debug_print:
        print(' -> '.join(path))

    return curr.name


if __name__ == '__main__':
    nodes = {'R': Node(name='R'), 'A': Node(name='A')}
    ratings = []
    with Path('d19_input.txt').open() as f:
        row_it = iter(f)
        while (row := next(row_it).strip()):
            name, conds = row.split('{')
            conds = conds[:-1].split(',')
            node = nodes[name] = Node(name=name)
            for cond in conds:
                node.transitions.append(Condition.from_str(cond))

        while True:
            try:
                rating = [None] * 4
                for entry in next(row_it).strip()[1:-1].split(','):
                    k, v = entry.split('=')
                    rating['xmas'.index(k)] = int(v)
                ratings.append(rating)
            except StopIteration:
                break

    sol = 0
    for rating in ratings:
        if traverse(nodes, rating) == 'A':
            sol += sum(rating)

    # Part 1
    print(sol)

    queue = deque([('in', [[1, 4000], [1, 4000], [1, 4000], [1, 4000]])])
    sol = 0
    while queue:
        name, ranges = queue.popleft()
        if name == 'R':
            continue
        elif name == 'A':
            sol += math.prod(x[1] - x[0] + 1 for x in ranges)
            continue

        node = nodes[name]
        for cond in node.transitions:
            if (idx := cond.idx) is None:
                queue.append((cond.target, ranges))
                break

            new_ranges = [list(x) for x in ranges]
            if (_min := cond._min) is not None and _min <= new_ranges[idx][1]:
                new_ranges[idx] = [_min, new_ranges[idx][1]]
                queue.append((cond.target, new_ranges))
                ranges[idx] = [ranges[idx][0], _min - 1]
            elif (_max := cond._max) is not None and _max >= new_ranges[idx][0]:
                new_ranges[idx] = [new_ranges[idx][0], _max]
                queue.append((cond.target, new_ranges))
                ranges[idx] = [_max + 1, ranges[idx][1]]

    # Part 2
    print(sol)

