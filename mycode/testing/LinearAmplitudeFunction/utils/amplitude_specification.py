"""
Provides functions for calculating the formula-based specification of the
`LinearAmplitudeFunction` program.

This module defines two functions for deriving specifications with respect
to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).
The calculations are performed on CPU using algebraic operations on state
vectors and density operators. The implementation is straightforward,
making it useful for verifying the functionality of quantum programs.
"""

import math
import numpy as np

def PSTC_specification(
    n: int, 
    number: int, 
    slop: float, 
    offset: float,
    domain: list[float], 
    image: list[float]
) -> list[float]:
    a, b = domain[0], domain[1] 
    c, d = image[0], image[1] 
    slopm = slop * (b - a) / (2 ** n - 1) / (d - c)
    offsetm = (offset - c) / (d - c)
    theta = np.pi * (slopm * number + offsetm)
    
    res_vec = [math.cos(theta / 2), math.sin(theta / 2)] 
    exp_probs = [res_vec[0] ** 2, res_vec[1] ** 2]
    return exp_probs

def MSTC_specification(
    n: int, 
    numbers: list[int],
    input_probs: list[float], 
    slop: float, 
    offset: float, 
    domain: list[float], 
    image: list[float]
) -> list[float]:
    exp_probs = [0.0, 0.0]
    a, b = domain[0], domain[1] 
    c, d = image[0], image[1] 
    slopm = slop * (b - a) / (2 ** n - 1) / (d - c)
    offsetm = (offset - c) / (d - c)
    for number in numbers:
        theta = np.pi * (slopm * number + offsetm)
        exp_probs[0] += input_probs[number] * math.cos(theta / 2) ** 2
        exp_probs[1] += input_probs[number] * math.sin(theta / 2) ** 2
    return exp_probs