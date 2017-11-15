#! /usr/bin/env python
#
# This program produces a git-aware prompt
#
# The usage is to put the following line in your ~/.bashrc file (without the #)
# export PS1=`python git_aware_prompt`

from __future__ import print_function
import os
import six
import termcolor as tc
import subprocess


cd = os.getcwd()
hostname=os.uname()[1]
username=os.getlogin()
tc.cprint(username+"@"+hostname+":"+cd+" ", 'green', end=" ")




completed = subprocess.run(["git", "status", "--porcelain"],
            stdin=None, input=None,
            stdout=subprocess.PIPE, stderr=None,
            shell=False, timeout=None, check=False)
completed_str = completed.stdout.decode('ascii')
dirty = len(completed_str) > 0

completed = subprocess.run(["git", "branch", "--color=never"],
            stdin=None, input=None,
            stdout=subprocess.PIPE, stderr=None,
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







