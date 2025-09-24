"""
Provides functions for calculating the formula-based specification of the
`QuadraticForm` program.

This module defines two functions for deriving specifications with respect
to pure-state test cases (PSTCs) and mixed-state test cases (MSTCs).
The calculations are performed on CPU using algebraic operations on state
vectors and density operators. The implementation is straightforward,
making it useful for verifying the functionality of quantum programs.
"""

import numpy as np

from typing import Sequence

def PSTC_specification(
    x: list[int], 
    A: list[list], 
    b: list[int], 
    c: int, 
    num_out_qubits: int
) -> list[float]:
    # Convert to NumPy arrays for safe matrix operations
    x = np.array(x) # pyright: ignore[reportAssignmentType]
    A = np.array(A) # pyright: ignore[reportAssignmentType]
    b = np.array(b) # pyright: ignore[reportAssignmentType]

    # Initialize probability distribution (all zeros)
    exp_probs = [0.0] * (2 ** num_out_qubits)

    # Compute Q(x) = x^T A x + x^T b + c
    Q = x.T @ A @ x + x.T @ b + c  # pyright: ignore[reportAttributeAccessIssue]

    # Wrap result into [0, 2^num_out_qubits)
    exp_res = int(Q % (2 ** num_out_qubits))

    # Assign probability 1 to the expected result
    exp_probs[exp_res] = 1.0
    return exp_probs


def MSTC_specification(
    input_numbers: list[int],
    n: int, 
    A: list[list], 
    b: list[int], 
    c: int, 
    num_out_qubits: int, 
    input_probs: list[float]
) -> list[float]:
    # Initialize global output distribution
    exp_probs = [0.0] * (2 ** num_out_qubits)

    for decimal_number in input_numbers:
        # Convert input number to binary list of length n (little-endian order)
        binary_list = [int(bit) for bit in bin(decimal_number)[2:].zfill(n)][::-1]

        # Get single-input distribution using PSTC
        single_dist = PSTC_specification(binary_list, A, b, c, num_out_qubits)

        # Accumulate into overall distribution with input probability weight
        exp_probs = [p + input_probs[decimal_number] * q 
                    for p, q in zip(exp_probs, single_dist)]

    return exp_probs
