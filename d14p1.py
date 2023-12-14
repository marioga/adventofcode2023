from pathlib import Path


if __name__ == '__main__':
    with Path('d14_input.txt').open() as f:
        mat = []
        for row in f:
            mat.append(list(row.strip()))

    m = len(mat)
    n = len(mat[0])
    last_hashtag = [-1] * n
    count_stones = [0] * n
    running_sum = 0
    for r in range(m):
        for c in range(n):
            if mat[r][c] == '#':
                last_hashtag[c] = r
                count_stones[c] = 0
            elif mat[r][c] == 'O':
                running_sum += m - (last_hashtag[c] + count_stones[c] + 1)
                count_stones[c] += 1
    print(running_sum)

