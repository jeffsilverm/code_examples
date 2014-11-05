#! /usr/bin/env python
#
#
# Given a list of integers, write a function to return a list of elements that
# has duplicates. Order of the result list is not important.
#
# What if the order is important?
#
# What kind of efficiency?

import collections

ORDERED = False    # True => order is important  False => order is not important

def find_duplicates(input_list) :
   """This function finds duplicates in lists of integers.
Actually, it is general: it will handle lists of any hashable object"""

   dup_list = []
   count_dict = collections.Counter()
   
   for i in input_list :
      count_dict[i] += 1

   for i in ( sorted( count_dict.keys() ) if ORDERED else count_dict.keys() ) :
      if count_dict[i] > 1 :
         dup_list.append(i)
   return dup_list         

      
if __name__ == "__main__" :
   def test (question, answer, description ):
      """This subroutine tests the Find_duplicates class.  Each test has
an input list, question, and an expected answer, answer"""
      
      r = find_duplicates(question)
      if ORDERED :
         assert cmp(r, answer) == 0
      else :
# For all elements in answer, make sure that each element is in r (nothing missing)
# For all elements in r, make sure that each element is in answer (nothing that
# shouldn't be there.
         for i in answer :
            if i not in r :
               raise AssertionError("%d not in %s and should be" % ( i,
                                                      ",".join(r) ) )
         for i in r :
            if i not in answer :
               raise AssertionError("%d is not in %s and should be" % ( i,
                              ",".join(answer) ) )
      print "%s PASSED" % description

# Execute the test code   
   try :
      test ( [1, 2, 3], [1, 2, 3], "testing the test method" )
      test ( [1, 2, 3], [3, 2, 1], "testing the test method" )
   except AssertionError :
      print ("Successfully tested the test method")
   else:
      raise AssertionError ("The test method does not work properly - call a" +\
                            " software engineer")

   print "ORDERED is ", ORDERED
   test ( [1, 2, 3, 4], [], 'no duplicates, sorted input' )        # 
   test ( [1, 1, 2, 3], [1], "1 duplicate, sorted input" )
   test ( [1, 1, 2, 2, 3], [1, 2], "many duplicates, sorted input" )
   test ( [1, 7, 2, 3], [], 'no duplicates, unsorted input')
   test ( [1, 1, 3, 2], [1], "1 duplicate, unsorted input" )
   test ( [2, 2, 1, 1, 3], [1, 2], "many duplicates, unsorted input" )
   test ( [1, 2, 2, 4, 5], [2], "One duplicate, sorted input, duplicate in middle")
   test ( [1, 2, 3, 5, 5], [5], "One duplicate, sorted input, duplicate at end")
   test ( [9, 2, 2, 1, 0], [2], "One duplicate, unsorted input, duplicate in middle")
   test ( [9, 2, 3, 5, 5], [5], "One duplicate, unsorted input, duplicate at end")
   ORDERED = True
   print "ORDERED is ", ORDERED
   test ( [1, 2, 3, 4], [], 'no duplicates, sorted input' )        # 
   test ( [1, 1, 2, 3], [1], "1 duplicate, sorted input" )
   test ( [1, 1, 2, 2, 3], [1, 2], "many duplicates, sorted input" )
   test ( [1, 7, 2, 3], [], 'no duplicates, unsorted input')
   test ( [1, 1, 3, 2], [1], "1 duplicate, unsorted input" )
   test ( [2, 2, 1, 1, 3], [1, 2], "many duplicates, unsorted input" )
   test ( [1, 2, 2, 4, 5], [2], "One duplicate, sorted input, duplicate in middle")
   test ( [1, 2, 3, 5, 5], [5], "One duplicate, sorted input, duplicate at end")
   test ( [9, 2, 2, 1, 0], [2], "One duplicate, unsorted input, duplicate in middle")
   test ( [9, 2, 3, 5, 5], [5], "One duplicate, unsorted input, duplicate at end")
   
          



