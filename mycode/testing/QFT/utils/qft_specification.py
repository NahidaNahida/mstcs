"""
Provides functions for calculating the formula-based specification of the
`QuantumFourierTransform` program.

This module defines two functions for deriving specifications with respect
to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).
The calculations are performed on CPU using algebraic operations on state
vectors and density operators. The implementation is straightforward,
making it useful for verifying the functionality of quantum programs.
"""

import numpy as np
import math, cmath

def PSTC_specification(n: int, number: int, if_swap: bool) -> list[float]:
    for index in range(n):
        theta = 2 * math.pi * number / (2 ** (index + 1))
        temp_state_vec = 1 / math.sqrt(2) * np.array([1, cmath.exp(theta * 1j)])
        if index == 0:
            state_vec = temp_state_vec
        else:
            if if_swap:
                state_vec = np.kron(state_vec, temp_state_vec)
            else:
                state_vec = np.kron(temp_state_vec, state_vec)
    exp_probs = (abs(state_vec) ** 2).tolist()
    return exp_probs

def MSTC_specification(
    numbers: list[int], 
    input_probs: list[float], 
    n: int, 
    if_swap: bool
) -> list[float]:
    exp_probs = np.array([0] * (2 ** n))
    for number in numbers:
        cond_probs = PSTC_specification(n, number, if_swap)
        add_probs = np.array(cond_probs) * input_probs[number]
        exp_probs = exp_probs + add_probs
    return exp_probs.tolist()