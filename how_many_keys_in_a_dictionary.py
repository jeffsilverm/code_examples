#! /usr/bin/python3
# -*- coding: utf-8 -*-
#
# How many entries can be stuffed into a dictionary?

import random

ctr = 0
d = dict()
try:
    while True:
        if ctr % 1000000 == 0:		# Once every millionth count, let the world know
            print(f"ctr is now {ctr}")
        d[ctr] = random.randint(0, 0x7FFFFFFF)
        ctr += 1
except Exception as e:
    print("Counter is ", ctr)
    print("exception is ", str(e))
    raise
