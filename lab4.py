#!/usr/bin/python
import random
import math

LAMBDA = 'lambda'
TYPE = 'type'


def get_random_time(lamb):
    return -math.log(random.random(), math.e) / lamb


def get_random_times(devices: list):
    times = []
    for dev in devices:
        times.append(get_random_time(dev[LAMBDA]))
    return times


def lsfr_part(part_index, broken_times: list, work_time):
    elements = []
    for i in range(len(broken_times)):
        elements.append(broken_times[i] > work_time)
    if part_index == 0:
        return (elements[0] and elements[1]) or (elements[2] and elements[3])
    if part_index == 1:
        return elements[0] and elements[1]
    if part_index == 2:
        return elements[0] or elements[1] or elements[2]
    if part_index == 3:
        return (elements[0] or elements[1]) and (elements[2] or elements[3])


def lsfr(broken_times: list, work_time):
    return (lsfr_part(0, broken_times[:4], work_time)
            and lsfr_part(1, broken_times[4:6], work_time)
            and lsfr_part(2, broken_times[6:9], work_time)
            and lsfr_part(3, broken_times[9:], work_time))


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


M = 4
LAMBDAS = [40 * 1e-6, 10 * 1e-6, 80 * 1e-6, 30 * 1e-6]
N = 35000
T = 8760
AMOUNT_OF_DEVICES = [4, 2, 3, 4]
P = 0.995
P_START = P + 0.001
FIND_STEPS = 2


def main():
    for i1 in range(1, 5):
        for i2 in range(1, 5):
            for i3 in range(1, 5):
                for i4 in range(1, 5):
                    p = run_simulation(N, M, LAMBDAS, AMOUNT_OF_DEVICES, [i1, i2, i3, i4], T, lsfr)
                    if p >= P:
                        print(p, (i1, i2, i3, i4))


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
    for i1 in range(reserve[0], reserve[0] + FIND_STEPS):
        for i2 in range(reserve[1], reserve[1] + FIND_STEPS):
            for i3 in range(reserve[2], reserve[2] + FIND_STEPS):
                for i4 in range(reserve[3], reserve[3] + FIND_STEPS):
                    p = run_simulation(N, M, LAMBDAS, AMOUNT_OF_DEVICES, [i1, i2, i3, i4], T, lsfr)
                    if p >= P:
                        print(p, (i1, i2, i3, i4))


if __name__ == '__main__':
    print("search type 1")
    main()
    print("search type 2")
    fast_search()
