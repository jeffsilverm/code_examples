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
    return n(3n-1)/2

def hn( n ):
    """Returns the nth hexagonal number"""
    return n(2n-1)

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
if len(sys.argv) != 1 :
    raise ValueError("This program takes exactly 1 argument, the maximum number iterations")
max_n = int(sys.argv[0])
if max_n <= 0 :
    raise ValueError("The number of iterations should be a counting number")

nt = 0
np = 0
nh = 0
p = -1
t = -1
h = -1
t_d = {}
p_d = {}
h_d = {}

for n in range(max_n):
    t_d[ tn( n ) ] = n
    p_d[ pn( n ) ] = n
    h_d[ hn( n ) ] = n

# while nt < max_n :  # for production
while nt < 287 :
    if nt in t_d :
        t = t_d[nt]
#        while nh < max_n :
        while nh < 146 :
            if nh in h_d :
                h = h_d[ nh ]
                if t == h :
                    print ("Remarkably, triangular number %d = T(%d) equals" % (t,nt)) +
                    ( "%d = H(%d)" % (h,nh))
                    for np in range(nt, nh):
                        p = p_d[ np ]
# The number T285 = P165 = H143 = 40755 is a triangular number, a pentagonal and a hexagonal
                        if ( nt == 285 and np == 165 and nh == 143 and
                        ( p != 40744 or h != 40744 or t != 40744 ) ):
                            raise AssertionError("The test values nt==285, np == 165, nh == 143 " +\
                                                 "do not yield 40744.  T=%d P=%d H=%d" % ( t, p, h))
# The only way to get here is if h == t
                        if p == h :
                            print ("***** You found it! " + "%d = T(%d) equals" % (t,nt)) +
                    ( "%d = P(%d) equals %d = H(%d) ***** " % (t,nh,p,np))
                            break
            if p == h :
                break
    if p == t :
        break
assert ( p == t and p == h ), "There is a bug in the software: t, p, h not equal! %d != %d != %d" %
    ( t, p, h)


    
    

