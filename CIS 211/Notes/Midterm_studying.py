"""
Mini-challenge:  Determine how to choose a subset of
positive integers from a list to sum to a target number.
"""

import typing
from typing import List

import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)

def sum_to(target: int , choices: List[int]) -> List[int]:
    """Choices is a list that represents a bag of
    positive numbers.   If elements of the bag can be summed
    to target, then we return a list of those elements.
    Otherwise return the empty list.
    example:  sum_to(8, [5, 2, 3]) -> [5, 3]
              sum_to(8, [2, 4, 5]) -> [ ]
              sum_to(8, [2, 2, 4, 5]) -> [2, 2, 4]
    """
    chosen = [ ]
    solved = _backtrack_to_sum(target, choices.copy(), chosen)
    if solved:
        return chosen
    return [ ]

# The actual back-tracking function returns a boolean
# but modifies the choices list.  Careful!
#
def _backtrack_to_sum(target: int, choices: List[int], chosen: List[int]) -> bool:


    if sum(choices) < target:
        return False
    if sum(choices) == target:
        chosen.append(choices)
        return True

    """
    for i in choices:
        print("len {}".format(len(choices)))
        for j in choices:
            if i != j and i + j == target:
                chosen.append([i, j])
                return True
    """

    



        return _backtrack_to_sum(target, choices, chosen)

    # The rest is up to you

# These aren't real unit tests, but they'll do:
print("sum_to(8, [5, 2]) -> [] got {}".format(sum_to(8, [])))
print("sum_to(7, [5, 2]) -> [5, 2] got {}".format(sum_to(7, [])))
print("sum_to(8, [5, 2, 3]) -> [5, 3] got {}".format(sum_to(8, [5, 2, 3])))
print("sum_to(8, [2, 4, 5]) -> [ ] got {}".format(sum_to(8, [2, 4, 5])))
print("sum_to(8, [2, 2, 4, 5]) -> [2, 2, 4], got {}".format(
    sum_to(8, [2, 2, 4, 5])))