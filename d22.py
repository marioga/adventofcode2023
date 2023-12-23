import heapq
from pathlib import Path


def get_block_falls(block, supports, supported_by):
    prev_removed = set()
    removed = {block}
    while len(prev_removed) < len(removed):
        prev_removed = removed.copy()
        tentative = set()
        for entry in prev_removed:
            tentative |= supports.get(entry, set())

        for entry in tentative:
            if supported_by[entry].issubset(prev_removed):
                removed.add(entry)

    return len(removed - {block})


if __name__ == '__main__':
    with Path('d22_input.txt').open() as f:
        blocks = []
        for i, row in enumerate(f):
            first, second = row.strip().split('~')
            first = list(map(int, first.split(',')))
            second = list(map(int, second.split(',')))
            assert all(f <= s for f, s in zip(first, second))
            assert len([i for i in range(3) if first[i] != second[i]]) <= 1
            blocks.append((first[2], i, *first, *second))

    num_blocks = len(blocks)
    heapq.heapify(blocks)

    ground_height = {}
    supports = {}
    supported_by = {}
    while blocks:
        _, i, x1, y1, z1, x2, y2, z2 = heapq.heappop(blocks)
        if x1 == x2 and y1 == y2:
            curr_height, curr_block = ground_height.get((x1, y1), (0, None))
            assert curr_height + 1 <= z1

            ground_height[(x1, y1)] = (curr_height + z2 - z1 + 1, i)
            if curr_block is not None:
                supports.setdefault(curr_block, set()).add(i)
                supported_by[i] = {curr_block}
        elif x1 == x2 and z1 == z2:
            highest = -1
            highest_blocks = set()
            for y in range(y1, y2 + 1):
                curr_height, curr_block = ground_height.get((x1, y), (0, None))
                assert curr_height + 1 <= z1
                if curr_height > highest:
                    highest = curr_height
                    highest_blocks.clear()
                elif curr_height < highest:
                    continue
                if curr_block is not None:
                    highest_blocks.add(curr_block)

            for y in range(y1, y2 + 1):
                ground_height[(x1, y)] = (highest + 1, i)
            if highest_blocks:
                supported_by[i] = highest_blocks
                for _block in highest_blocks:
                    supports.setdefault(_block, set()).add(i)
        elif y1 == y2 and z1 == z2:
            highest = -1
            highest_blocks = set()
            for x in range(x1, x2 + 1):
                curr_height, curr_block = ground_height.get((x, y1), (0, None))
                assert curr_height + 1 <= z1
                if curr_height > highest:
                    highest = curr_height
                    highest_blocks.clear()
                elif curr_height < highest:
                    continue
                if curr_block is not None:
                    highest_blocks.add(curr_block)

            for x in range(x1, x2 + 1):
                ground_height[(x, y1)] = (highest + 1, i)
            if highest_blocks:
                supported_by[i] = highest_blocks
                for _block in highest_blocks:
                    supports.setdefault(_block, set()).add(i)
        else:
            raise Exception("Unexpected input!")

    non_support_blocks = set(range(num_blocks))
    for bottom_block, above_blocks in supports.items():
        for above_block in above_blocks:
            above_block_supports = supported_by.get(above_block, set())
            assert bottom_block in above_block_supports
            if len(above_block_supports) == 1:
                non_support_blocks.remove(bottom_block)
                break

    # Part 1
    print(len(non_support_blocks))

    # Part 2
    print(sum(get_block_falls(block, supports, supported_by) for block in range(num_blocks)))

