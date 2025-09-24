"""
Provides functions for calculating the formula-based specification of the
`LinearPauliRotations` program.

This module defines two functions for deriving specifications with respect
to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).
The calculations are performed on CPU using algebraic operations on state
vectors and density operators. The implementation is straightforward,
making it useful for verifying the functionality of quantum programs.
"""

import math

def PSTC_specification(
    number: int, 
    slope: float, 
    offset: float
) -> list[float]:
    exp_probs = [0.0, 0.0]
    a, b = slope / 2, offset / 2
    exp_probs[0] = math.cos(a * number + b) ** 2
    exp_probs[1] = math.sin(a * number + b) ** 2
    return exp_probs

def MSTC_specification(
    numbers: list[int], 
    input_probs: list[float], 
    slope: float, 
    offset: float
) -> list[float]:
    exp_probs = [0.0, 0.0]   # [p(0), p(1)]
    a, b = slope / 2, offset / 2
    for number in numbers:
        exp_probs[0] += input_probs[number] * math.cos(a * number + b) ** 2
        exp_probs[1] += input_probs[number] * math.sin(a * number + b) ** 2
    return exp_probs