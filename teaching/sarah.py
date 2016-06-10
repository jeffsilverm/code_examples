#! /usr/bin/python
# -*- coding: utf-8 -*-
# The line above is required for python 2 but is optional for python 3
#
# This program should work equally well under python 2 or python 3
import sys
print (sys.version)

sarah = u" הרש"

sarah_and_english = sarah + " Sarah"



ali=u" علي اصغر‎"
	
sheshech=u"현륜식"

unknown=u" 昨晩の障害について"

def decode_unicode(s) :
    """This function decodes a unicode string, character by character"""
    print (s)
    for c in s:
        print (c, ord(c) )

decode_unicode(sarah)
decode_unicode(sarah_and_english)
decode_unicode(ali)
decode_unicode(sheshech)
decode_unicode(unknown)



# Down here, it's too late
# -*- coding: utf-8 -*-
