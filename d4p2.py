from pathlib import Path


if __name__ == '__main__':
    ret = 0
    extra_copies = {}
    with Path('d4_input.txt').open() as f:
        for row in f:
            line = row.strip()
            card, line = line.split(': ')
            card_num = int(card[len("Card "):])
            winning, hand = line.split(' | ')
            winning = set(int(val) for val in winning.split(' ') if val)

            count = sum(1 for num in hand.split(' ') if num and int(num) in winning)
            copies = 1 + extra_copies.pop(card_num, 0)
            for i in range(count):
                extra_copies[card_num + 1 + i] = extra_copies.get(card_num + 1 + i, 0) + copies

            ret += copies

    print(ret)

