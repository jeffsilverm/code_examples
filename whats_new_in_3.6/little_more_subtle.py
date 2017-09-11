#! /usr/bin/python3.6
# -*- coding: utf-8 -*-

def find_in_string ( to_search_for : str, string_to_search : str ) -> int:
    start_idx = string_to_search.find(to_search_for)
    return start_idx

def return_directions(return_int):
    if return_int :
        return 12
    else :
        return "twelve"

ans_1 = find_in_string ( string_to_search="Take a left on broadway, then right",
                        to_search_for="left")

print("This should work: ", ans_1)

directions=return_directions(True)
ans_2a = find_in_string ( string_to_search=directions,
                        to_search_for="left")

print("This should fail: ", ans_2a)

directions=return_directions(False)
ans_2b = find_in_string ( string_to_search=directions,
                        to_search_for="left")
print("This should work: ", ans_2b)

