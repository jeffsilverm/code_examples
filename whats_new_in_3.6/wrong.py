#! /usr/bin/python3.6
# -*- coding: utf-8 -*-

def find_in_string ( to_search_for, string_to_search):
    start_idx = string_to_search.find(to_search_for)
    return start_idx


ans_1 = find_in_string ( string_to_search="Take a left on broadway, then right",
                        to_search_for="left")

print("This should work: ", ans_1)

ans_2 = find_in_string ( string_to_search=12,
                        to_search_for="left")

print("This should fail: ", ans_2)


