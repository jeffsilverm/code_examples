# -*- coding: utf-8 -*-
#
# The following 4 imports are to make the same code run on both python 2.6+ and
# python 3.3+
import future
import builtins
import past
import six
import time

import ansiescapes as ae
for q in range(40):
  print(q*2*"{}")
for q in range(5):  
  print(q, end="", flush=True)
  time.sleep(1)
  print(ae.eraseLine, end="", flush=True)
print(ae.ESC+"2J", end="", flush=True)
print(ae.cursorTo(0,0) + "cursoTo(0,0) This should be in the upper left corner", end="", flush=True)
print(ae.cursorMove(0,10) + "cursoTo(0,10) This should be 10 lines down at the left margin", end="", flush=True)
print(ae.cursorDown(count = 1) + "Down one", end="", flush=True)
print(ae.cursorDown(count = 2) + "Down two", end="", flush=True)
print(ae.cursorForward(count = 4) + "Forward 4", flush=True)
print(ae.cursorTo(3,20) + "cursoTo(3,20) somewhere on the third line", end="", flush=True)
for w in range (50):
  print(ae.cursorBackward(count = 4)+"w", end="", flush=True)
  time.sleep(0.5)
print(ae.cursorTo(0,0) + "cursoTo(0,0) This should be in the upper left corner", end="", flush=True)
print(ae.eraseLines(count = 1), end="", flush=True)
# print(image(buf, opts = {}):
# def setCwd(cwd = os.getcwd()):
