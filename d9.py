from pathlib import Path


def extrapolate(nums):
    ret = 0
    all_zeros = False
    while not all_zeros:
        ret += nums[-1]
        diffs = []
        all_zeros = True
        for i in range(len(nums) - 1):
            diff = nums[i + 1] - nums[i]
            if diff != 0:
                all_zeros = False
            diffs.append(diff)
        nums = diffs
    return ret


def extrapolate_left(nums):
    ret = 0
    all_zeros = False
    mult = 1
    while not all_zeros:
        ret += mult * nums[0]
        mult *= -1
        diffs = []
        all_zeros = True
        for i in range(len(nums) - 1):
            diff = nums[i + 1] - nums[i]
            if diff != 0:
                all_zeros = False
            diffs.append(diff)
        nums = diffs
    return ret


if __name__ == '__main__':
    running_sum_1 = 0
    running_sum_2 = 0
    with Path('d9_input.txt').open() as f:
        for line in f:
            nums = list(map(int, line.strip().split()))
            running_sum_1 += extrapolate(nums)
            running_sum_2 += extrapolate_left(nums)
    print(running_sum_1)
    print(running_sum_2)

