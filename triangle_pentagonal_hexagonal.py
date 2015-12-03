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
#
# Googling 40755 and hexagonal, pentagonal, and hexagonal reveals
# that the next answer is 1,533,776,805
# (http://www.mathblog.dk/project-euler-45-next-triangle-pentagonal-hexagonal-number/)
#
# Looking for the first number 40755, worked relatively well, returning an answer in
# 0.145 seconds.  Looking for the second number, 1,533,776,805, was excruitingly
# slow.  Looking at top, I see that the process has used 28GBytes of RAM and still growing.
# Eventually, the out of memory (OOM) killer killed it.
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
if max_n <= 285 :
    raise ValueError("The indexes of the numbers should be larger than 285")
 

BIG_T = 40755    

# implementation note: if time permits, investigate using a counter instead of
# a dictionary.
t_d = {}
p_d = {}
h_d = {}

# This is counter intuitive (at least to me). A number T is triangular if it in
# dictionary t_d.  We're looking for the nth triangular number.  So, for example,
# 6 is a triangular number.  We can tell by looking at t_d[6] that the 2nd triangular
# is 6.  Searching for a key in a dictionary is very fast.
for n in range(1, max_n):
    t_d[ tn( n ) ] = n
    p_d[ pn( n ) ] = n
    h_d[ hn( n ) ] = n
# I am programming very defensively here to bolster my intuition that this is the right way
# to solve the problem.  Maybe using a counter is not such a good idea: there must be a limit
# on the number of key/value pairs you can have in a dictionary
assert 4 not in t_d, "Your intuition is blown.  4 is not supposed to be in t_d"
assert t_d[3] == 2, "The directory t_d was not initialized properly: the 2nd triangular \
number is not 6 it is %d" % t_d[3]
assert p_d[12] == 3, "The directory p_d was not initialized properly: the 3rd pentagonal \
number is not 12, it is %d" % p_d[12]
assert h_d[28] == 4, "The directory h_d was not initialized properly: the 4th pentagonal \
number is not 28, it is %d" % h_d[28]
# The number T285 = P165 = H143 = 40755 is a triangular number, a pentagonal
# number, and a hexagonal number.
assert t_d[BIG_T] == 285 and p_d[BIG_T] == 165 and h_d[BIG_T] == 143, \
        "The test case in the problem statement failed. t_d[BIG_T]=%d (should be 285), p_d[40755]=%d (should be 165)\
, h_d[40755]=%d (should be 143)" % \
        (t_d[BIG_T], p_d[BIG_T], h_d[BIG_T] )

for t in range(1, max_n+1) :
    if t in t_d :    # is t a triangular number?
        nt = t_d[t] # Yes, what is its index?
        if t in h_d : # is t also a hexagonal number?
            nh = h_d[t]         # yes, what is its index?
            if t in p_d :       # is it also a pentagonal number ?
                np = p_d[t]    # yes, what is its index ?
# The number T285 = P165 = H143 = 40755 is a triangular number, a pentagonal and a hexagonal
                if ( nt == 285 and np == 165 and nh == 143 and
                ( t != BIG_T) ):
                    raise AssertionError("The test values nt==285, np == 165, nh == 143 \
do not yield 40755.  nt=%d np=%d nh=%d T=%d" % ( t_d[t], p_d[t], h_d[t], t))                    
                print ("***** You found one! %d = T(%d) equals %d = P(%d) equals %d = H(%d) ***** " \
                   % (t, nt, t, np, t, nh ))




    
    

