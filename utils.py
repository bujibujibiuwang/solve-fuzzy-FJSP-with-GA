import numpy as np
import matplotlib.pyplot as plt

"""
(1) fuzzy operators
"""


def addition(s1, s2):
    a = s1[0] + s2[0]
    b = s1[1] + s2[1]
    c = s1[2] + s2[2]
    return [a, b, c]


def old_max(s1, s2):
    a = max(s1[0], s2[0])
    b = max(s1[1], s2[1])
    c = max(s1[2], s2[2])
    return [a, b, c]


def value(s):
    return (s[0] + 2 * s[1] + s[2]) / 4


def rank(s1, s2):
    if value(s1) > value(s2):
        return s1
    elif value(s1) < value(s2):
        return s2
    elif s1[1] > s2[1]:
        return s1
    elif s1[1] < s2[1]:
        return s2
    elif (s1[2] - s1[0]) > (s2[2] - s2[0]):
        return s1
    else:
        return s2


"""
(2) read instance
"""


def read(path):
    with open(path) as file:
        lines = file.read().split('\n')
    part = lines[0].split()
    job_nb, machine_nb, op_nb = int(part[0]), int(part[1]), int(part[2])

    job_fuzzy_pt = []
    total_fuzzy_pt = []

    for k in range(1, job_nb * op_nb + 1):
        line = lines[k]
        part = line.split()
        pt = [list(map(int, x)) for x in [a.split(',') for a in part[1:]]]
        job_fuzzy_pt.append(pt)
        if len(job_fuzzy_pt) == op_nb:
            total_fuzzy_pt.append(job_fuzzy_pt)
            job_fuzzy_pt = []
    return job_nb, machine_nb, op_nb, np.array(total_fuzzy_pt)


"""
(3) valid
"""


def check_valid(pop, op_nb, job_nb):
    pop = pop.tolist()
    for p in pop:
        for i in range(job_nb):
            if p.count(i) != op_nb:
                print('error')
    print('right')


"""
(4) plot
"""


def draw(best, mean):
    plt.figure()
    plt.plot(best, label='best')
    plt.plot(mean, label='mean')
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.legend()
    plt.show()
