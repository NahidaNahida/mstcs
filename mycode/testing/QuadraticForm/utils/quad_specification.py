import numpy as np

def PSTC_specification(x, A, b, c, num_out_qubits):
    """
    Single-input specification (PSTC).
    
    Computes the expected output probability distribution for a given input vector x,
    where the output is determined by the quadratic form:
        Q(x) = x^T A x + x^T b + c
    
    Args:
        x (list[int] or np.ndarray): Input vector (binary representation of variables).
        A (list[list[int]] or np.ndarray): Quadratic coefficient matrix.
        b (list[int] or np.ndarray): Linear coefficient vector.
        c (int): Constant term.
        num_out_qubits (int): Number of output qubits.
    
    Returns:
        list[float]: Probability distribution of output states, length = 2^num_out_qubits.
    """
    # Convert to NumPy arrays for safe matrix operations
    x = np.array(x)
    A = np.array(A)
    b = np.array(b)

    # Initialize probability distribution (all zeros)
    exp_probs = [0.0] * (2 ** num_out_qubits)

    # Compute Q(x) = x^T A x + x^T b + c
    Q = x.T @ A @ x + x.T @ b + c

    # Wrap result into [0, 2^num_out_qubits)
    exp_res = int(Q % (2 ** num_out_qubits))

    # Assign probability 1 to the expected result
    exp_probs[exp_res] = 1.0
    return exp_probs


def MSTC_specification(input_numbers, n, A, b, c, num_out_qubits, input_probs):
    """
    Multi-input specification (MSTC).
    
    Iterates through multiple input states, computes their expected output distributions
    using PSTC_specification, and accumulates probabilities weighted by input_probs.
    
    Args:
        input_numbers (list[int]): Set of input numbers (decimal representation).
        n (int): Number of input bits.
        A (list[list[int]] or np.ndarray): Quadratic coefficient matrix.
        b (list[int] or np.ndarray): Linear coefficient vector.
        c (int): Constant term.
        num_out_qubits (int): Number of output qubits.
        input_probs (list[float]): Probability distribution over input numbers.
    
    Returns:
        list[float]: Aggregated output probability distribution, length = 2^num_out_qubits.
    """
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
