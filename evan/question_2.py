#! /usr/bin/env python
#
#
# Given a UI for calculating prime number:
# 
# - A text box in which the user can enter an int. correspond to this text box
# is the function set_value() which we can use for automation
# - A button the user can push which take the above number and determine if the
# number is a prime one. The automated function for this button is push_button()
#  A label, which will display "True" or "False" indicating if the number in
# the text box a prime number or not. The automated function for this label is
# get_result()
#
# Question: How do I measure the performance of the function which determine
# the number's prime-ness.

TESTING = False   # True if testing the prime number subroutine
BENCHMARKING = True  # True if we want to benchmark the is_prime function
text_box = ""

def set_value(integer):
   """Call this function to emulate the user entering a value into the test
box"""
   global text_box
   text_box = str(integer)

def get_result( answer ):
   """Call this function with the answer, as a string"""
   return str(answer)


def push_button():
   """Call this function to emulate the user pushing the submit button.  This
function returns the integer in the text_box.  Raise ValueError if the input
string is not a valid positive integer"""
   integer = int(text_box)
   if integer <0 :
      raise ValueError("Enter a *positive* integer")
   prime = is_prime(integer)
   get_result ( prime )
   return prime

# This is from
# http://rosettacode.org/wiki/Miller-Rabin_primality_test#Python:_Proved_correct_up_to_large_N
# My reasoning for plagarizing is that the objective is to get the job done
# quickly, so using the internet as a resource is A Good Thing.
"""This function tests if the input integer is composite"""
def _try_composite(a, d, n, s):
# Return x to the power y; if z is present, return x to the power y, modulo z
# (computed more efficiently than pow(x, y) % z).
 if pow(a, d, n) == 1:
     return False
 for i in range(s):
     if pow(a, 2**i * d, n) == n-1:
         return False
 return True # n  is definitely composite



def is_prime(n, _precision_for_huge_n=16):



    if n in _known_primes or n in (0, 1):
        return True
    if any((n % p) == 0 for p in _known_primes):
        return False
    d, s = n - 1, 0
    while not d % 2:
        d, s = d >> 1, s + 1
    # Returns exact according to http://primes.utm.edu/prove/prove2_3.html
    if n < 1373653: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3))
    if n < 25326001: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5))
    if n < 118670087467: 
        if n == 3215031751: 
            return False
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7))
    if n < 2152302898747: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11))
    if n < 3474749660383: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13))
    if n < 341550071728321: 
        return not any(_try_composite(a, d, n, s) for a in (2, 3, 5, 7, 11, 13, 17))
    # otherwise
    return not any(_try_composite(a, d, n, s) 
                   for a in _known_primes[:_precision_for_huge_n])
 
_known_primes = [2, 3]
_known_primes += [x for x in range(5, 1000, 2) if is_prime(x)]

if __name__ == "__main__" :
# Do a little unit testing
   if TESTING :
# This file has format suitable for gnuplot
      timing_file = open("timing_file", "w")
   
      def test ( question, answer ):
         if is_prime ( question ) == answer :
            print "%d PASSED" % question
         else :
            raise AssertionError( "%d FAILED, should be %s" % (question, answer) )

      # from http://primes.utm.edu/lists/small/1000.txt
      for i in [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,\
                71, 73, 79, 83, 89, 97,
101,    103,    107,    109,    113, 
   2221,   2237,   2239,   2243, 2251, 2267, 2269, 2273, 2281, 2287, \
      7649, 7669, 7673,   7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, \
                7753, 7757, 7759, 7789, 7793, 7817, 7823, 7829, \
      7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907,7919 ] :
         test ( i, True)
      for i in [4, 6, 18, 24, 240, 1000, 10000, 100000, 100004, 500, 82, 7907*7919,
            7901*7907*7919] :
         test ( i, False)

# We don't need to do a lot of testing, because the unit testing was already done
# above.  This is testing the UI interface
   for i in ['4', '6', '8'] :
      set_value(i)
      r = push_button()
      assert not r 
   print "Testing composite numbers PASSED"
   for i in ['5', '7', '11'] :
      set_value(i)
      r = push_button()
      assert r
   print "Testing prime numbers PASSED"
# Test that bad input will be detected
   try:
      set_value(-1)
      r = push_button()
   except ValueError:
      print "Detected a negative number"
   else :
      print "EPIC FAIL!!!!! Did *not* detect a negative number"
   try:
      set_value("A")
      r = push_button()
   except ValueError:
      print "Detected an invalid number string"
   else :
      print "EPIC FAIL!!!!! Did *not* detect a string"
   try:
      set_value([15])
      r = push_button()
   except ValueError:
      print "Detected a list (this would be a programming error)"
   else :
      print "EPIC FAIL!!!!! Did *not* detect a list"

   if BENCHMARKING :
      import timeit

      def benchmark(n, f):
         execution_time = timeit.timeit("is_prime(%d)" % n,
                                 setup="from %s import is_prime" % __name__,
                                 number=10000)
         f.write(str(n)+" "+ str(execution_time)+"\n")
         print n, execution_time


      number_list = [5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67,\
                71, 73, 79, 83, 89, 97,
    127,    131,    137,    139,    149,    151,    157,    163,    167,    173, 
    179,    181,    191,    193,    197,    199,    211,    223,    227,    229, 
    233,    239,    241,    251,    257,    263,    269,    271,    277,    281, 
    283,    293,    307,    311,    313,    317,    331,    337,    347,    349, 
    353,    359,    367,    373,    379,    383,    389,    397,    401,    409, 
    419,    421,    431,    433,    439,    443,    449,    457,    461,    463, 
    467,    479,    487,    491,    499,    503,    509,    521,    523,    541, 
    547,    557,    563,    569,    571,    577,    587,    593,    599,    601, 
    607,    613,    617,    619,    631,    641,    643,    647,    653,    659, 
    661,    673,    677,    683,    691,    701,    709,    719,    727,    733, 
    739,    743,    751,    757,    761,    769,    773,    787,    797,    809, 
    811,    821,    823,    827,    829,    839,    853,    857,    859,    863, 
    877,    881,    883,    887,    907,    911,    919,    929,    937,    941, 
    947,    953,    967,    971,    977,    983,    991,    997,   1009,   1013, 
   1019,   1021,   1031,   1033,   1039,   1049,   1051,   1061,   1063,   1069, 
   1087,   1091,   1093,   1097,   1103,   1109,   1117,   1123,   1129,   1151, 
   1153,   1163,   1171,   1181,   1187,   1193,   1201,   1213,   1217,   1223, 
   1229,   1231,   1237,   1249,   1259,   1277,   1279,   1283,   1289,   1291, 
   1297,   1301,   1303,   1307,   1319,   1321,   1327,   1361,   1367,   1373, 
   1381,   1399,   1409,   1423,   1427,   1429,   1433,   1439,   1447,   1451, 
   1453,   1459,   1471,   1481,   1483,   1487,   1489,   1493,   1499,   1511, 
   1523,   1531,   1543,   1549,   1553,   1559,   1567,   1571,   1579,   1583, 
   1597,   1601,   1607,   1609,   1613,   1619,   1621,   1627,   1637,   1657, 
   1663,   1667,   1669,   1693,   1697,   1699,   1709,   1721,   1723,   1733, 
   1741,   1747,   1753,   1759,   1777,   1783,   1787,   1789,   1801,   1811, 
   1823,   1831,   1847,   1861,   1867,   1871,   1873,   1877,   1879,   1889, 
   1901,   1907,   1913,   1931,   1933,   1949,   1951,   1973,   1979,   1987, 
   1993,   1997,   1999,   2003,   2011,   2017,   2027,   2029,   2039,   2053, 
   2063,   2069,   2081,   2083,   2087,   2089,   2099,   2111,   2113,   2129, 
   2131,   2137,   2141,   2143,   2153,   2161,   2179,   2203,   2207,   2213, 


                     2243, 2251, 2267, 2269, 2273, 2281, 2287, \
      7649, 7669, 7673,   7681, 7687, 7691, 7699, 7703, 7717, 7723, 7727, 7741, \
                7753, 7757, 7759, 7789, 7793, 7817, 7823, 7829, \
      7841, 7853, 7867, 7873, 7877, 7879, 7883, 7901, 7907,7919 ]
      f = open("prime_execution_times.txt", "w")
      for n in number_list :
# Test the prime number
         benchmark(n, f)
# n+1 is always composite.  What I am trying to do is pick a value that is "close"
# to a prime number but which is composite.  It should take much less time
# but maybe because n+1 is always a multiple of 2
         benchmark(n+1, f)
      f.close()
      
