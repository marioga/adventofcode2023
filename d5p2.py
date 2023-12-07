from pathlib import Path


def map_ids(curr_ids, range_to_range):
    events = []
    for s, e in curr_ids:
        events.append((s, 1, None))
        events.append((e, 2, None))

    for idx, (s, e, _) in enumerate(range_to_range):
        events.append((s, 0, idx))
        events.append((e, 3, idx))

    events = sorted(events)

    ret = []
    curr_idx = None
    for val, _type, _idx in events:
        if _type == 0:
            if ret and ret[-1][1] is None:
                if val > ret[-1][0]:
                    ret[-1][1] = val - 1
                    ret.append([val, None, _idx])
                else:
                    ret[-1][2] = _idx
            curr_idx = _idx
        elif _type == 1:
            ret.append([val, None, curr_idx])
        elif _type == 2:
            ret[-1][1] = val
        else:
            if ret and ret[-1][1] is None:
                ret[-1][1] = val
                ret.append([val + 1, None, None])
            curr_idx = None

    ret2 = []
    for s, e, _idx in ret:
        if _idx is None:
            ret2.append((s, e))
        else:
            src, _, dst = range_to_range[_idx]
            ret2.append((dst + (s - src), dst + (e - src)))

    return ret2


if __name__ == '__main__':
    with Path('d5_input.txt').open() as f:
        row_it = iter(f)

        curr_ids = list(map(int, next(row_it).strip().split(': ')[1].split(' ')))
        curr_ids = [(curr_ids[i], curr_ids[i] + curr_ids[i + 1] - 1) for i in range(0, len(curr_ids), 2)]
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

            range_to_range = []
            try:
                while (line := next(row_it).strip()):
                    dst, src, range_len = map(int, line.split(' '))
                    range_to_range.append((src, src + range_len - 1, dst))
            except StopIteration:
                done = True

            curr_ids = map_ids(curr_ids, range_to_range)

        assert(target == 'location')

    print(sorted(curr_ids)[0][0])

