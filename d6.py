import math
from pathlib import Path


def compute_range_len(_time, dist):
    sqrt_disc = math.sqrt(_time**2 - 4 * dist)
    return math.ceil((_time + sqrt_disc) / 2) - math.floor((_time - sqrt_disc) / 2) - 1


if __name__ == '__main__':
    with Path('d6_input.txt').open() as f:
        row_it = iter(f)
        times = next(row_it).strip().split(':')[1]
        times = [int(t) for t in times.split(' ') if t]
        dists = next(row_it).strip().split(':')[1]
        dists = [int(d) for d in dists.split(' ') if d]

        print(math.prod([compute_range_len(t, d) for t, d in zip(times, dists)]))

        large_time = int(''.join(map(str, times)))
        large_dist = int(''.join(map(str, dists)))
        print(compute_range_len(large_time, large_dist))

