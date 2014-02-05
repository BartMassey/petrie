#!/usr/bin/python3
# Copyright (c) 2014 Bart Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Evaluate a Petrie Multiplier model for various
# conversations.

from sys import argv

N = int(argv[1])
pm = float(argv[2])   # probability of male in population
# in binary intra-gender conversation...
psm = float(argv[3])   # probability male partner makes sexist remark
psf = float(argv[4])   # probability female partner makes sexist remark

phf11 = pm * psm
phm11 = (1 - pm) * psf

# ph memo table
memo = {}

def ph(ph11, i, n):
    if i < 0:
        return 0.0
    if i > n:
        return 0.0
    if i == 0 and n == 1:
        return 1 - ph11
    if i == 1 and n == 1:
        return ph11
    if (ph11, i, n) in memo:
        return memo[(ph11, i, n)]
    newmemo = ph(ph11, i, n - 1) * (1 - ph11) + ph(ph11, i - 1, n - 1) * ph11
    memo[(ph11, i, n)] = newmemo
    return newmemo

def phm(i, n):
    return ph(phm11, i, n)

def phf(i, n):
    return ph(phf11, i, n)

for (name, f) in [("phm", phm), ("phf", phf)]:
    print(name)
    for n in range(1, N + 1):
        for i in range(0, n + 1):
            print(" " + "{0:5.3f}".format(f(i, n))[1:], end="")
        print()
    print()
