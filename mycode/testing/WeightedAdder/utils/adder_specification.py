"""
Provides functions for calculating the formula-based specification of the
`WeightedAdder` program.

This module defines two functions for deriving specifications with respect
to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).
The calculations are performed on CPU using algebraic operations on state
vectors and density operators. The implementation is straightforward,
making it useful for verifying the functionality of quantum programs.
"""

import numpy as np

def PSTC_specification(
    s: int, 
    qubit_vals: list[bool], 
    lambda_vals: list[int]
) -> list[float]:
    # Initialize a probability vector of length 2^s with all zeros
    expProbs = (np.zeros(2 ** s)).tolist()
    expRes = 0
    
    # Compute the weighted sum of the qubit values using lambda coefficients
    # This represents the expected result index in the probability vector
    for i in range(len(lambda_vals)):
        expRes += lambda_vals[i] * qubit_vals[i]
    
    # Assign probability 1 to the computed index (deterministic outcome)
    expProbs[expRes] = 1
    return expProbs

def MSTC_specification(
    input_numbers: list[int], 
    input_probs: list[float], 
    n: int, 
    s: int, 
    lambda_vals: list[int]
) -> list[float]:
    # Initialize a probability vector of length 2^s with all zeros
    expProbs = (np.zeros(2 ** s)).tolist()
    
    # Iterate over all input numbers (decimal representation of basis states)
    for decimal_number in input_numbers:
        # Convert the decimal number to a binary string of length n
        binary_string = bin(decimal_number)[2:].zfill(n)
        
        # Convert to a list of bits and reverse the order to match qubit indexing
        qList = [int(bit) for bit in binary_string][::-1]
        
        # Compute the weighted sum of the qubit values with lambda coefficients
        expRes = 0
        for i in range(len(lambda_vals)):
            expRes += lambda_vals[i] * qList[i]
        
        # Accumulate probability at the computed index, weighted by input distribution
        expProbs[expRes] += input_probs[decimal_number]
    
    return expProbs