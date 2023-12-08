import heapq
from pathlib import Path


def get_period(start, directions, mapping):
    count = 0
    slow = fast = 0
    slow_curr = fast_curr = start
    ret = {}
    while True:
        dir_slow_idx = int(directions[slow] == 'R')
        slow_curr = mapping[slow_curr][dir_slow_idx]
        slow = (slow + 1) % len(directions)
        count += 1
        for _ in range(2):
            dir_fast_idx = int(directions[fast] == 'R')
            fast_curr = mapping[fast_curr][dir_fast_idx]
            fast = (fast + 1) % len(directions)

        if slow_curr.endswith('Z'):
            ret.setdefault(slow_curr, []).append(count)

        if slow == fast and slow_curr == fast_curr:
            break

    ptr = 0
    ptr_curr = start
    pre_cycle = 0
    while not (ptr == slow and ptr_curr == slow_curr):
        if pre_cycle > 0 and slow_curr.endswith('Z'):
            ret.setdefault(slow_curr, []).append(count)

        pre_cycle += 1
        count += 1
        dir_slow_idx = int(directions[slow] == 'R')
        slow_curr = mapping[slow_curr][dir_slow_idx]
        slow = (slow + 1) % len(directions)
        dir_ptr_idx = int(directions[ptr] == 'R')
        ptr_curr = mapping[ptr_curr][dir_ptr_idx]
        ptr = (ptr + 1) % len(directions)

    # return Z-ending positions, length before cycle, length of cycle
    return ret, pre_cycle, count - pre_cycle


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def solve(crt):
    start, moduli = crt[0]
    for idx in range(1, len(crt)):
        a, n = crt[idx]
        i = 1
        while (start + i * moduli - a) % n != 0:
            i += 1
        start = start + i * moduli
        assert gcd(moduli, n) == 1
        moduli *= n
    return start


if __name__ == '__main__':
    with Path('d8_input.txt').open() as f:
        row_it = iter(f)
        directions = next(row_it).strip()

        next(row_it)
        mapping = {}
        start = []
        while True:
            try:
                src, tgt = next(row_it).strip().split(' = ')
                tgt = tgt[1:-1].split(', ')
            except StopIteration:
                break
            mapping[src] = tgt
            if src.endswith('A'):
                start.append(src)

        # collect data for chinese remained theorem
        crts = [[] for _ in range(len(start))]
        total_gcd = None
        for idx, entry in enumerate(start):
            Z_positions, pre_cycle, cycle = get_period(entry, directions, mapping)
            # Assumes Z-ending doesn't occur pre-cycle
            for values in Z_positions.values():
                for v in values:
                    assert v >= pre_cycle
                    crts[idx].append((v % cycle, cycle))
            if total_gcd is None:
                total_gcd = cycle
            else:
                total_gcd = gcd(total_gcd, cycle)

        crts = [[(a, n // total_gcd) for a, n in _list] for _list in crts]

        num_crts = 1
        for crt in crts:
            num_crts *= len(crt)

        best = None
        for multi_idx in range(num_crts):
            idxs = []
            for crt in crts:
                idxs.append(multi_idx % len(crt))
                multi_idx //= len(crt)

            sol = solve([crt[idx] for idx, crt in zip(idxs, crts)])
            if best is None or best > sol:
                best = sol

        print(best * total_gcd)

