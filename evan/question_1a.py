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

class Find_duplicates() :
   """This class has methods for finding duplicates in lists of integers.
Actually, it is general: it will handle lists of any hashable object"""

   def __init__ ( self ) :
      self.count_dict = collections.Counter()
      self.ordering_list = list()

   def input_list ( self, list_of_ints ) :
      """Call this method to provide the list of ints that this class searches
for duplicates on"""
      if ORDERED :
         self.ordering_list = list(list_of_ints)
      for i in list_of_ints :
         self.count_dict[i] += 1

   def output_list_of_duplicates(self):
      """Call this method to get the list of duplicates"""

      dup_list = []
      if ORDERED :
         for i in self.ordering_list :
            if self.count_dict[i] > 1 :
               dup_list.append(i)
      else :
         for i in self.count_dict.keys() :
            if self.count_dict[i] > 1 :
               dup_list.append(i)
      return dup_list         

      
if __name__ == "__main__" :
   def test (question, answer ):
      
      c = Find_duplicates()
      c.input_list(question)
      r = c.output_list_of_duplicates()
      if ORDERED :
         assert r == answer
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
   
   try :
      test ( [1, 2, 3], [1, 2, 3] )
   except AssertionError :
      print ("Successfully tested the test method")
   else:
      raise AssertionError ("The test method does not work properly - call a" +\
                            " software engineer")
             
   test ( [1, 2, 3, 4], [])        # no duplicates, sorted input
   test ( [1, 1, 2, 3], [1])       # 1 duplicate, sorted input
   test ( [1, 1, 2, 2, 3], [1, 2]) # many duplicates, sorted input
   
          



