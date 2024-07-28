#Emina Merlak Susman
#27151132

import os
import test_runner
from time import time

tests_path = 'Tests'


def compute_right_indexes(input_list):
    right_indexes = [None for _ in range(len(input_list))]
    stack = []
    stack.append((0, input_list[0]))
    for i, elt in enumerate(input_list):
        stack_top = stack[-1][1]
        if elt < stack_top:
            stack.append((i, elt))
        elif elt > stack_top:
            while elt > stack_top: 
                prev = stack.pop()
                right_indexes[prev[0]] = i
                if stack:
                    stack_top = stack[-1][1]
                else:
                    break
            stack.append((i, elt))
            
    for i in right_indexes[:-1]:
        print(i, end =' ')
    print(right_indexes[-1])
        
def compute_left_indexes(input_list):
    input_list = list(reversed(input_list))
    left_indexes = [None for _ in range(len(input_list))]
    stack = []
    stack.append((0, input_list[0]))
    for i, elt in enumerate(input_list):
        stack_top = stack[-1][1]
        if elt < stack_top:
            stack.append((i, elt))
        elif elt > stack_top:
            while elt > stack_top: 
                prev = stack.pop()
                index_of_prev_in_reverse = len(input_list) - prev[0] - 1
                index_of_elt_in_reverse = len(input_list) - i - 1
                left_indexes[index_of_prev_in_reverse] = index_of_elt_in_reverse
                if stack:
                    stack_top = stack[-1][1]
                else:
                    break
            stack.append((i, elt))
            
    for i in left_indexes[:-1]:
        print(i, end =' ')
    print(left_indexes[-1])

input_list = list(map(int, input().split()))

compute_left_indexes(input_list)
compute_right_indexes(input_list)