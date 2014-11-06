#! /usr/bin/env python
#
#1. write 2 methods, 1 for serialize and 1 for deserialize.
#
# that serialize function takes a list of string and return 1 single  string
#
# and that deserialize function takes 1 single string (result from above) and
# deserialize back to list of string

import pickle

def serialize( list_of_str):
   """This function serializes a list of strings to a single string in json
format"""

   r = pickle.dumps( list_of_str)

   return r

def deserialize ( serialized_str ):
   """This function desiralizes a json format string into what it was"""
   r = pickle.loads( serialized_str )
   return r

test = ["This", "is", "a", "test."]

s = serialize( test )

result = deserialize (s)
print test
print s, type(s)
print result

assert cmp(test, result) == 0
