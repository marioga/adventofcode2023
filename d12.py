from pathlib import Path


def get_matches(template, amounts, tidx, aidx, cache):
    if (tidx, aidx) in cache:
        return cache[(tidx, aidx)]

    if tidx == len(template):
        ret = 1 if aidx == len(amounts) else 0
    elif template[tidx] == '.':
        ret = get_matches(template, amounts, tidx + 1, aidx, cache)
    elif template[tidx] == '#':
        if aidx == len(amounts):
            ret = 0
        else:
            delta = 1
            while delta < amounts[aidx] and tidx + delta < len(template) and template[tidx + delta] in '?#':
                delta += 1

            if delta < amounts[aidx]:
                ret = 0
            elif aidx + 1 < len(amounts):
                if tidx + delta == len(template) or template[tidx + delta] == '#':
                    ret = 0
                else:
                    ret = get_matches(template, amounts, tidx + delta + 1, aidx + 1, cache)
            else:
                ret = get_matches(template, amounts, tidx + delta, aidx + 1, cache)
    else:  # template[tidx] == '?'
        # Assume it's a '.' first
        ret = get_matches(template, amounts, tidx + 1, aidx, cache)
        # Assume it's a '#' next
        if aidx < len(amounts):
            delta = 1
            while delta < amounts[aidx] and tidx + delta < len(template) and template[tidx + delta] in '?#':
                delta += 1
            if delta == amounts[aidx]:
                if aidx + 1 == len(amounts):
                    ret += get_matches(template, amounts, tidx + delta, aidx + 1, cache)
                elif tidx + delta < len(template) and template[tidx + delta] in '?.':
                    ret += get_matches(template, amounts, tidx + delta + 1, aidx + 1, cache)

    cache[(tidx, aidx)] = ret
    return ret


if __name__ == '__main__':
    running_sum1 = running_sum2 = 0
    with Path('d12_input.txt').open() as f:
        for row in f:
            template, amounts = row.strip().split(' ')
            amounts = list(map(int, amounts.split(',')))
            running_sum1 += get_matches(template, amounts, 0, 0, {})
            running_sum2 += get_matches('?'.join([template] * 5), amounts * 5, 0, 0, {})
    print(running_sum1)
    print(running_sum2)

