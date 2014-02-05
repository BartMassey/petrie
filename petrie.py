#!/usr/bin/python3
# Copyright (c) 2014 Bart Massey
# [This program is licensed under the GPL version 3 or later.]
# Please see the file COPYING in the source
# distribution of this software for license terms.

# Evaluate a Petrie Multiplier model for various
# conversations.

from sys import argv

cum = False
if len(argv) > 0 and argv[1] == "-c":
    cum = True
    del argv[1]

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

print("i =  ", end="")
for i in range(N):
    d = len(str(i))
    pre = 3 - int(d / 2)
    print(' ' * pre + str(i) + ' ' * (5 - d - pre), end="")
print()
for (name, f) in [("phm", phm), ("phf", phf)]:
    print(name + ": ", end="")
    pt = 0.0
    for i in range(0, N + 1):
        p = f(i, N)
        if not cum:
            pt = p
        print(" " + "{0:5.3f}".format(pt)[1:], end="")
        if i > N / 8 and p < 0.001:
            break
        pt += p
    print()
