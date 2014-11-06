#! /usr/bin/env python
#
# #2 classic  programming question
# input  as a string "mom dad sister son daughter mom"
# output => "mom" 2 times, "dad" 1 time
# find how many words is that string is same when you read from the front and
# from the back (ex. "mom", dad")
import collections

TESTING = True

def reflective ( word ) :
   """This function returns True if the word is reflective, i.e., it reads
the same whether viewed left to right or from right to left.  Examples include
mom, dad, deed, toot, a, i, elle (technically, a French word, but the problem
statement doesn't mention language), sees, tet (A Vietnamese word), stats (m-w.com
says that stat means statistic and is usually used in the plural, hence stats."""
   for i in range(0, len(word)/2):
      if word[i] != word[-i-1] :
         return False
   return True

if TESTING :
   def test( question, answer ):
      print question, "FAILS" if reflective(question) != answer else "PASSES"

   test ("toot", True )  # Even number of characters
   test ("tet", True )   # Odd number of characters
   test ("EeeeeE", True )# not a real word, but a good test case
   test ("EeeFeeE", True)# not a real word, but a good test case
   test ("Lima", False ) # Even number of characters
   test ("red", False )  # Odd number of characters
   test ("I", True )     # Degenerate case
   test ("", True )      # Another Degenerate case

def count ( words ) :
   """This function returns a Counter of reflexive words in the input string"""
   list_of_words = words.split()
   c = collections.Counter()
   for w in list_of_words :
      if reflective(w) :
         c[w] += 1
   return c

if __name__ == "__main__" :
   words = "mom dad sister son daughter mom"
   c = count( words )
   print "String is %s" % words
   for k in c.keys() :
      print k,c[k]
   



