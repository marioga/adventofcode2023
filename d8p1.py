from pathlib import Path


if __name__ == '__main__':
    with Path('d8_input.txt').open() as f:
        row_it = iter(f)
        directions = next(row_it).strip()

        next(row_it)
        mapping = {}
        while True:
            try:
                src, tgt = next(row_it).strip().split(' = ')
                tgt = tgt[1:-1].split(', ')
            except StopIteration:
                break
            mapping[src] = tgt

    count = 0
    curr = 'AAA'
    i = 0
    while curr != 'ZZZ':
        dir_idx = int(directions[i] == 'R')
        i = (i + 1) % len(directions)
        curr = mapping[curr][dir_idx]
        count += 1

    print(count)

