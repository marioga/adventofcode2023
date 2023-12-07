from pathlib import Path


if __name__ == '__main__':
    running_sum = 0
    with Path('d1_input.txt').open() as f:
        for row in f:
            first = last = None
            for ch in row.strip():
                if ch.isdigit():
                    if first is None:
                        first = int(ch)
                    last = int(ch)
            running_sum += 10 * first + last
    print(running_sum)

    running_sum = 0
    DIGITS = {d: i for i, d in enumerate(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine'], 1)}
    with Path('d1_input.txt').open() as f:
        for row in f:
            line = row.strip()
            i = 0
            first = last = None
            while i < len(line):
                val = None
                if (ch := line[i]).isdigit():
                    val = int(ch)
                else:
                    for d in range(3, 6):
                        if (word := line[i:i + d]) in DIGITS:
                            val = DIGITS[word]
                            break

                if val is not None:
                    if first is None:
                        first = val
                    last = val
                i += 1
            running_sum += 10 * first + last
    print(running_sum)

