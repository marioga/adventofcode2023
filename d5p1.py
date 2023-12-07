from pathlib import Path


if __name__ == '__main__':
    with Path('d5_input.txt').open() as f:
        row_it = iter(f)

        curr_ids = list(map(int, next(row_it).strip().split(': ')[1].split(' ')))
        curr_source = 'seed'
        # skip blank line
        next(row_it)

        done = False
        while not done:
            line = next(row_it).strip()

            line = line[:-len(' map:')]
            source, _, target = line.split('-')
            if source != curr_source:
                raise Exception(f"Invalid input: {source}, {curr_source}")

            curr_source = target

            mapped = {}
            try:
                while (line := next(row_it).strip()):
                    dst, src, range_len = map(int, line.split(' '))
                    for _id in curr_ids:
                        if src <= _id < src + range_len:
                            mapped[_id] = dst + (_id - src)
            except StopIteration:
                done = True

            curr_ids = [mapped.get(_id, _id) for _id in curr_ids]

        assert(target == 'location')
        print(min(curr_ids))

