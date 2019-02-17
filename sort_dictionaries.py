#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# This program demonstrates the difference between dictionaries, dictionaries
# where the keys have been sorted, and ordered dictionaries

import random
import collections


def ordinary_dict(k_list: list) -> dict:
    dl = {}
    for k7 in k_list:
        dl[k7] = random.randint(0, LENGTH)
    return dl

def ordered_dict(k_list: list) -> dict:
    ds = collections.OrderedDict()
    for k7 in k_list:
        ds[k7] = random.randint(0, LENGTH)
    return ds


key_list = [0, 5, 2, 1, 2]
LENGTH = len(key_list)
d = ordinary_dict(key_list)
print("unsorted")
for k in d.keys():
    print(f"d[{k}] is {d[k]}")

print("sorted")
for k in sorted(d.keys()):
    print(f"d[{k}] is {d[k]}")

d = ordinary_dict(key_list)
print("ordered dictionary")
for k in d.keys():
    print(f"d[{k}] is {d[k]}")



