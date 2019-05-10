#!/usr/bin/python
import random
import math

M = 3                                        # amount of types of devices
LAMBDAS = [40 * 1e-6, 10 * 1e-6, 80 * 1e-6]  # lambdas of types
N = 35000                                    # special parameter, see task
T = 8760                                     # work time
P = 0.99                                     # see task
P_START = P                                  # probability to stop coordinate descent
FIND_STEPS = 2                               #
AMOUNT_OF_DEVICES = [3, 2, 3]                # amount of devices for each type


def get_random_time(lamb):
    return -math.log(random.random(), math.e) / lamb


def lsfr_part(part_index, broken_times: list, work_time):
    elements = []
    for i in range(len(broken_times)):
        elements.append(broken_times[i] > work_time)
    if part_index == 0:
        return (elements[0] and elements[1]) or (elements[2])
    if part_index == 1:
        return elements[0] and elements[1]
    if part_index == 2:
        return elements[0] or elements[1] or elements[2]


def lsfr(broken_times: list, work_time):
    return (lsfr_part(0, broken_times[:3], work_time)
            and lsfr_part(1, broken_times[3:5], work_time)
            and lsfr_part(2, broken_times[5:], work_time))


def run_simulation(n, m, lamb: list, amount_of_devices: list, reserve: list, work_time, logic_function: callable):
    if len(lamb) != m:
        raise ValueError("m should be equals len(lamb)")
    if len(amount_of_devices) != m:
        raise ValueError("m should be equals len(amount_of_devices)")

    d = 0
    for i in range(n):
        broken_times = []
        for j in range(m):
            random_times = [get_random_time(lamb[j]) for i in range(amount_of_devices[j])]
            for i in range(reserve[j]):
                min_time = min(random_times)
                broken_index = random_times.index(min_time)
                random_times[broken_index] += get_random_time(lamb[j])
            broken_times += random_times
        if not logic_function(broken_times, work_time):
            d += 1
    return 1 - d / N


def brute_force_finding(start, steps):
    """
    Find solution via brute forcing
    :param start: start positions
    :type: list
    :param steps: types for brute forcing
    :type: int
    :return: none
    """
    for i1 in range(start[0], start[0] + steps):
        for i2 in range(start[1], start[1] + steps):
            for i3 in range(start[2], start[2] + steps):
                p = run_simulation(N, M, LAMBDAS, AMOUNT_OF_DEVICES, [i1, i2, i3], T, lsfr)
                if p >= P:
                    print(p, (i1, i2, i3))


def main():
    brute_force_finding([1 for _ in range(M)], 4)


def fast_search():
    reserve = []
    for i in range(M):
        p = 0
        res = 0
        while p < P_START:
            res += 1
            p = run_simulation(N, 1, [LAMBDAS[i]], [AMOUNT_OF_DEVICES[i]], [res], T,
                               lambda broken, work_time: lsfr_part(i, broken, work_time))
        reserve.append(res)
    print(reserve, run_simulation(N, M, LAMBDAS, AMOUNT_OF_DEVICES, reserve, T, lsfr))
    brute_force_finding(reserve, FIND_STEPS)


if __name__ == '__main__':
    print("search type 1")
    main()
    print("search type 2")
fast_search()

