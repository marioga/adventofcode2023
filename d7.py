import math
from collections import Counter
from pathlib import Path


def score_key(hand, mapping):
    counter = Counter(hand)
    if len(counter) == 1:
        # five of a kind
        _type = 7
    elif len(counter) == 2:
        # four of a kind or full house
        _type = (6 if counter.most_common(1)[0][1] == 4 else 5)
    elif len(counter) == 3:
        # three of a kind or two pairs
        _type = (4 if counter.most_common(1)[0][1] == 3 else 3)
    elif len(counter) == 4:
        _type = 2
    else:
        _type = 1

    return (_type, *map(int, (mapping.get(ch, ch) for ch in hand)))


def score_key_with_joker(hand, mapping):
    counter = Counter(hand)
    num_jokers = counter.pop('J', 0)
    if len(counter) <= 1:
        # five of a kind with joker
        _type = 7
    elif len(counter) == 2:
        # four of a kind or full house
        _type = (6 if counter.most_common(1)[0][1] + num_jokers == 4 else 5)
    elif len(counter) == 3:
        # three of a kind or two pairs
        _type = (4 if counter.most_common(1)[0][1] + num_jokers == 3 else 3)
    elif len(counter) == 4:
        _type = 2
    else:
        _type = 1

    return (_type, *map(int, (mapping.get(ch, ch) for ch in hand)))


if __name__ == '__main__':
    with Path('d7_input.txt').open() as f:
        hand_scores = [entry.strip().split(' ') for entry in f]

    mapping = dict(zip('TJQKA', range(10, 16)))
    ret = 0
    hand_scores.sort(key=lambda h_s: score_key(h_s[0], mapping=mapping))
    for rank, (_, score) in enumerate(hand_scores, 1):
        ret += rank * int(score)
    print(ret)

    ret_jokers = 0
    # Turn 'J' into the weakest card
    mapping['J'] = 1
    hand_scores.sort(key=lambda h_s: score_key_with_joker(h_s[0], mapping=mapping))
    for rank, (_, score) in enumerate(hand_scores, 1):
        ret_jokers += rank * int(score)
    print(ret_jokers)

