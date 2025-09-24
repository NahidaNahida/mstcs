"""
Provides functions for calculating the formula-based specification of the
`IntegerComparator` program.

This module defines two functions for deriving specifications with respect
to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).
The calculations are performed on CPU using algebraic operations on state
vectors and density operators. The implementation is straightforward,
making it useful for verifying the functionality of quantum programs.
"""


def PSTC_specification(n: int, number: int, L: int, sign: bool) -> list[float]:
    exp_probs = [0] * (2 ** n)
    if sign == True:
        exp_probs[int(number >= L)] = 1
    else:
        exp_probs[int(number < L)] = 1
    return exp_probs

def MSTC_specification(numbers: list[int], probs: list[float], L: int, sign: bool) -> list[float]:
    exp_probs = [0.0] * (len(numbers))    # [p(0), p(1)]
    for number in numbers:
        if sign == True:
            exp_probs[int(number >= L)] += probs[number]
        else:
            exp_probs[int(number < L)] += probs[number]
    return exp_probs
    