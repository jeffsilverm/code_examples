#! /usr/bin/env python
#
# Find a number that is simultaneously triangular, pentagonal and hexagonal.
# This is fairly well known problem in number theory.
#
# The nth triangular number is Tn = n(n+1)/2
# The nth pentagonal number is Pn = n(3n-1)/2
# The nth Hexagonal number is Hn = n(2n-1)
#
# The number T285 = P165 = H143 = 40755 is a triangular number, a
# pentagonal number, and a hexagonal number. Write code to find the next
# number like this.
import sys

def tn( n ):
    """Returns the nth triangular number"""
    return n*(n+1)/2

def pn( n ):
    """Returns the nth pentagonal number"""
    return n*(3*n-1)/2

def hn( n ):
    """Returns the nth hexagonal number"""
    return n*(2*n-1)

# Now, are there some numbers n1, n2, and n3 such that
# tn ( n1 ) == pn( n2) == hn( n3 )
# Comparing three numbers has computational complexity O(n^3). Is there a way
# can reduce this complexity?
# How about dictionaries that are key'd by tn, pn, and hn?  The value would be
# n If a number is in the dictionary, then it is whatever the dictionary is.
# That is O(1).  However, the computation complexity still increases as O(n^2)
# The number T285 = P165 = H143 = 40755 is a triangular number, a pentagonal
# number, and a hexagonal number. 
# Also, we know that if tn ( n1 ) == hn( n3 ) that n1 <= n2 <= n3 so that will
# simplify the search for n2 such that tn(n1) == pn(n2) == hn(n3)
# The number T285 = P165 = H143 = 40755 is a triangular number, a pentagonal
# number, and a hexagonal number. Write code to find the next number like this.
#
if len(sys.argv) != 2 :
    raise ValueError("This program takes exactly 1 argument, the maximum number iterations")
max_n = int(sys.argv[1])
if max_n < 285 :
    raise ValueError("The number of iterations should be a counting number larger than 285")
 
    

nt = 0
np = 0
nh = 0
# These variables have to be initialized because they will be referenced before
# they are assigned otherwise.  Furthermore, they have to initialized to
# different values, because they will be tested for equality and those tests
# should fail before good values are found.
p = -1
t = -2
h = -3
t_d = {}
p_d = {}
h_d = {}

for n in range(1, max_n):
    t_d[ tn( n ) ] = n
    p_d[ pn( n ) ] = n
    h_d[ hn( n ) ] = n

# for nt in range(1, max_n) :  # for production
for nt in range(1, 287) :   # for test
    if nt in t_d :
        t = t_d[nt]
#        for nh in range(1, max_n) :   # for production
        for nh in range(1,146) :  # for test
            if nh in h_d :
                h = h_d[ nh ]
                if t == h :
                    print ("Remarkably, triangular number %d = T(%d) equals \
%d = H(%d)" % (t,nt, h, nt ))
                    for np in range(nt, nh):
                        if np in p_d :
                            p = p_d[ np ]
# The number T285 = P165 = H143 = 40755 is a triangular number, a pentagonal and a hexagonal
                            if ( nt == 285 and np == 165 and nh == 143 and
                            ( p != 40755 or h != 40755 or t != 40755 ) ):
                                raise AssertionError("The test values nt==285, np == 165, nh == 143 \
do not yield 40744.  T=%d P=%d H=%d" % ( t, p, h))
# The only way to get here is if h == t
                            if p == h :
                                print ("***** You found it! %d = T(%d) equals %d = P(%d) equals %d = H(%d) ***** " \
                                   % (t,nt, p, pn, h, hn))
                                break
                        else :
                            p = -1   # np is not a pentagonal number so p reverts
                else :
                    h = -3   # nh is not a hexagonal number so h reverts
    else :
        t = -2     # nt is not a triangular number, so t reverts
# I'd like break out of two loops at this point.  The following two tests will
# will break out
            if p == h and h == t :
                break
    if p == t and p == h :
        break
assert ( p == t and p == h ), "There is a bug in the software: t, p, h not equal! %d != %d != %d" %\
    ( t, p, h)


    
    

