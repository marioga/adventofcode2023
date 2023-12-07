from pathlib import Path


if __name__ == '__main__':
    ret = 0
    with Path('d4_input.txt').open() as f:
        for row in f:
            line = row.strip()
            _, line = line.split(': ')
            winning, hand = line.split(' | ')
            winning = set(int(val) for val in winning.split(' ') if val)

            score = 0
            for num in hand.split(' '):
                if num and int(num) in winning:
                    if score == 0:
                        score = 1
                    else:
                        score *= 2

            ret += score

    print(ret)

