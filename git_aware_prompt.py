#! /usr/bin/env python
#
# This program produces a git-aware prompt
#
# The usage is to put the following line in your ~/.bashrc file (without the #)
# export PS1="\$(python ~/git_aware_prompt.py)"
# Explanation: Anything in $() is considered a command line command.  However,
# in this case, we want the PS1 to contain the string *with* the $, so the
# command is executed each time the command line prompt is referenced



from __future__ import print_function
import os
import sys
import termcolor as tc
import subprocess
import pwd


cd = os.getcwd()
hostname=os.uname()[1]

# os.getlogin doesn't work reliably.  If this program is invoked from a terminal
# session started with Alt-T, then the os.getlogin() call fails with a file not
# found exception.
# This solution was suggested by https://github.com/parmentelat/apssh/issues/1


try:
    username=os.getlogin()
except FileNotFoundError:
# It clear to me that this will work under Windows, but then, the error might
# not happen under windows, either.
    username = pwd.getpwuid(os.getuid())[0]

tc.cprint(username+"@"+hostname+":"+cd+" ", 'green', end=" ")

completed = subprocess.run(["git", "status", "--porcelain"],
            stdin=None, input=None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=False, timeout=None, check=False)
# If the git status command fails, then assume we're in a directory that is not
# a git repository.  In this case, just output a $ and be done with it
if completed.returncode != 0:
    tc.cprint("$ ", 'white')
    sys.exit(0)
completed_str = completed.stdout.decode('ascii')
dirty = len(completed_str) > 0

completed = subprocess.run(["git", "branch", "--color=never"],
            stdin=None, input=None,
            stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            shell=False, timeout=None, check=False)
completed_str = completed.stdout.decode('ascii')
branch_list=completed_str.split("\n")
for branch in branch_list:
    if "*" in branch:
        break
else:
    raise AssertionError("* not found in branch_list: " + str(branch_list))

tc.cprint("(%s)"%branch[2:], 'cyan', end=" " )

if dirty:
  tc.cprint("* ", "red", end=" $ ")
else:
  tc.cprint(" ", 'white', end=" $ ")



