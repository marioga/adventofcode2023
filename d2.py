import math
from pathlib import Path


if __name__ == '__main__':
    COUNTS = {'red': 12, 'green': 13, 'blue': 14}

    ret = 0
    with Path('d2_input.txt').open() as f:
        for row in f:
            line = row.strip()
            game, shows = line.split(': ')
            game = int(game[len("Game "):])
            shows = shows.split('; ')

            failed = False
            for show in shows:
                elems = show.split(', ')
                for count, color in map(lambda s: s.split(' '), elems):
                    if int(count) > COUNTS[color]:
                        failed = True
                        break

                if failed:
                    break

            if not failed:
                ret += game
    print(ret)

    ret = 0
    with Path('d2_input.txt').open() as f:
        for row in f:
            line = row.strip()
            _, shows = line.split(': ')
            shows = shows.split('; ')

            best = {key: 0 for key in COUNTS}
            for show in shows:
                elems = show.split(', ')
                for count, color in map(lambda s: s.split(' '), elems):
                    best[color] = max(best[color], int(count))
            ret += math.prod(best.values())
    print(ret)
