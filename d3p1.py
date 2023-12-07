from pathlib import Path


if __name__ == '__main__':
    ret = 0
    mat = []
    with Path('d3_input.txt').open() as f:
        for row in f:
            mat.append(list(row.strip()))

    for r, row in enumerate(mat):
        i = 0
        while i < len(row):
            if not row[i].isdigit():
                i += 1
                continue

            val = int(row[i])
            j = i + 1
            while j < len(row) and row[j].isdigit():
                val = 10 * val + int(row[j])
                j += 1

            is_symbol_adjacent = False
            if (i > 0 and row[i - 1] != '.') or (j < len(row) and row[j] != '.'):
                is_symbol_adjacent = True

            for k in range(max(i - 1, 0), min(j, len(row) - 1) + 1):
                if r > 0 and not (mat[r - 1][k].isdigit() or mat[r - 1][k] == '.'):
                    is_symbol_adjacent = True
                    break
                if r < len(mat) - 1 and not (mat[r + 1][k].isdigit() or mat[r + 1][k] == '.'):
                    is_symbol_adjacent = True
                    break

            if is_symbol_adjacent:
                ret += val

            i = j

    print(ret)

