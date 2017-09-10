#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
import time
import sys
assert sys.version_info.major == 3 and sys.version_info.minor == 6, \
    print("Not running python 3.6, running {}".format(sys.version_info))

class A(object):

    def __init__(self):
        pass

    def af_A(self, input):
        return input * 2

    def afo_A(self, input):
        return input * 4

class AA(A):

    def __init__(self):
        pass

    def aaf_AA(selfs, input):
        return input * 20

    def afo_A(self, input):
        return input ** 2

class B(object):
    def __init__(self):
        pass

    def bf_B(selfs, input):
        return input * 9



a = A()
aa = AA()

print("a.af_A(4) ", a.af_A(4))
print("a.afo_A(4) ", a.afo_A(4))
print("aa.aaf_AA(4) ", aa.aaf_AA(4))
print("aa.afo_A(4) ", aa.afo_A(4))

print("a.af_A('4') ", a.af_A('4'))
print("a.afo_A('4') ", a.afo_A('4'))
print("aa.aaf_AA('4') ", aa.aaf_AA('4'), flush=True)
try:
    print("aa.afo_A('4') ", aa.afo_A('4'))
except TypeError as t:
    time.sleep(1)
    print("Exception TypeError was raised, as expected, when calling aa.afo_A('4'))", file=sys.stderr)




