#! /usr/bin/python
# -*- coding: utf-8 -*-
#
# better_git_prompt.py
# This program does a better job of creating a prompt for a directory that has
# a git repository in it.
# IMHO, the better prompt should have 4 parts:
# Current directory in the default color
# Current git branch in a different color
# An asterisk, preferably red, if there are uncommitted tracked files
# A dollar sign in the default color if the user is *not* root or a pound sign
# if the if the user is root.
#
# If the current directory is *not* a git repository, then do not change the
# prompt
#
# This is motivated by the problems I've had with
# ~/.bash/git-aware-prompt/prompt.sh
#
# A repository is "dirty"

