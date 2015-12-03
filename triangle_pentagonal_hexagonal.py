#! /usr/bin/env python
#
# Hi Jeff,
#
# It was great connecting with you today!
# 
# As promised, I have included the Coding Exercise question. Here is the link:
# https://gist.github.com/marndt/389c114200841ed0858c
# I will keep an eye out for your answers and updated resume.
# Let me know if you have any questions at all at this time.
# Jason Ames
# Recruiting Manager
# CAPABILITY IT
# main: 425.679.5762
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

TEST = True

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
if TEST :

# This table is taken directly from the github page
# Triangular	Tn = n(n+1)/2	1, 3, 6, 10, 15, ...
# Pentagonal	Pn = n(3n-1)/2	1, 5, 12, 22, 35, ...
# Hexagonal	Hn = n(2n-1)	1, 6, 15, 28, 45, ...
    t_table = [0, 1, 3,  6, 10, 15 ]
    p_table = [0, 1, 5, 12, 22, 35 ]
    h_table = [0, 1, 6, 15, 28, 45 ]
    for n in range(1,len(t_table)):
        assert tn(n) == t_table[n], "Triangular function fails on %d,\
returned %d should have returned %d" % ( n, tn(n), t_table[n])
        assert pn(n) == p_table[n], "Pentagonal function fails on %d,\
returned %d should have returned %d" % ( n, tn(n), p_table[n])
        assert hn(n) == h_table[n], "Hexagonal function fails on %d,\
returned %d should have returned %d" % ( n, tn(n), h_table[n])
    print("All functions returned correct values for their tests")   


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
# implementation note: if time permits, investigate using a counter instead of
# a dictionary.
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
                if nh == nh :
                    print ("Remarkably, triangular number %d = T(%d) equals \
%d = H(%d)" % (nt, t, nh, h ))
                    for np in range(nt, nh):
                        if np in p_d :
                            p = p_d[ np ]
# The number T285 = P165 = H143 =condemming 40755 is a triangular number, a pentagonal and a hexagonal
                            if ( nt == 285 and np == 165 and nh == 143 and
                            ( p != 40755 or h != 40755 or t != 40755 ) ):
                                raise AssertionError("The test values nt==285, np == 165, nh == 143 \
do not yield 40744.  T=%d P=%d H=%d" % ( t, p, h))
# The only way to get here is if h == t
                            if np == nh :
                                print ("***** You found it! %d = T(%d) equals %d = P(%d) equals %d = H(%d) ***** " \
                                   % (nt, h, pn, p, hn, h))
                                break
                        else :
                            p = -1   # np is not a pentagonal number so p reverts
                        if p == h and h == t :
                            break    # the np loop
            else :   # nh not in h_d
                h = -3   # nh is not a hexagonal number so h reverts
            if p == h and h == t :
                break    # the nh loop   
    else :
        t = -2     # nt is not a triangular number, so t reverts            
    if p == t and p == h :
        break     # the nt loop
assert ( p == t and p == h ), "There is a bug in the software: t, p, h not equal! %d != %d != %d" %\
    ( t, p, h)


    
    

