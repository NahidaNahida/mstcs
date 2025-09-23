import numpy as np
 

def generate_numbers(n: int, m: int) -> list[list]:
    """
    Generate all possible n-digit numbers in base-m representation.

    Args:
        n (int): The number of digits (e.g., qubits in a quantum setting).
        m (int): The base (e.g., number of states for each digit).

    Returns:
        list[list[int]]: A list of all n-digit m-ary numbers.
                         Each number is represented as a list of integers.

    Example:
        >>> generate_numbers(3, 2)
        [[0, 0, 0],
         [0, 0, 1],
         [0, 1, 0],
         [0, 1, 1],
         [1, 0, 0],
         [1, 0, 1],
         [1, 1, 0],
         [1, 1, 1]]
    """

    if n <= 0:
        return [[]]  # base case: return an empty list when no digits are required

    if n == 1:
        return [[i] for i in range(m)]  # base case: single-digit m-ary numbers

    # Recursive case:
    # First, generate all (n-1)-digit m-ary numbers
    smaller_numbers = generate_numbers(n - 1, m)

    # Then, prepend each possible digit (0..m-1) to the smaller numbers
    number_list = []
    for digit in range(m):
        for smaller_number in smaller_numbers:
            number_list.append([digit] + smaller_number)

    return number_list


def outputdict2probs(output_dic: dict[int, int], n: int) -> np.ndarray:
    """
    Convert raw measurement outcomes into a normalized probability distribution.

    Args:
        output_dic (dict[int, int]): 
            Dictionary mapping measurement outcomes (as integers) to their counts.  
            For example, {0: 5, 3: 7} means outcome |00> occurred 5 times, |11> occurred 7 times.
        n (int): 
            Number of qubits. Defines the dimension of the Hilbert space (2**n outcomes).

    Returns:
        numpy.ndarray: 
            A 1D NumPy array of length 2**n, where each entry represents the probability 
            of observing the corresponding computational basis state.  
            The array is normalized such that `sum(prob_dist) == 1`.

    Notes:
        - Outcomes not present in `output_dic` are assigned probability 0.
        - The function assumes keys in `output_dic` are integers in the range [0, 2**n - 1].
        - The ordering follows binary encoding: index `i` corresponds to the basis state 
          given by the n-bit binary representation of `i`.

    Example:
        >>> counts = {0: 500, 3: 500}  # suppose 1000 shots with 2 qubits
        >>> outputdict2probs(counts, n=2)
        array([0.5, 0. , 0. , 0.5])  # corresponds to |00>, |01>, |10>, |11>
    """

    # Convert Qiskit counts object to dictionary {int_outcome: frequency}
    total_shots = sum(output_dic.values())
    prob_dist = np.zeros(2**n, dtype=float)
    for outcome, count in output_dic.items():
        prob_dist[outcome] = count / total_shots

    return prob_dist

def outputdict2samps(dict_counts: dict[int, int]) -> list[int]:
    """
    Expand a dictionary of outcome counts into a list of raw samples.

    Args:
        dict_counts (dict[int, int]):
            A dictionary mapping outcome (as an integer) to the number of times 
            it was observed. Typically derived from Qiskit measurement results.

    Returns:
        list[int]:
            A flat list of samples, where each outcome is repeated according to its frequency.

    Example:
        >>> dict_counts = {0: 2, 3: 1}
        >>> outputdict2samps(dict_counts)
        [0, 0, 3]
    """
    samps = []
    # Expand counts: repeat each outcome `value` times
    for key, value in dict_counts.items():
        samps += [key] * value
    return samps

def covered_pure_states(probs: list[float]) -> list[int]:
    """
    Identify the basis states that are covered (i.e., have non-zero probability).

    Args:
        probs (list[float]):
            A probability distribution over basis states, typically of length 2**n.

    Returns:
        list[int]:
            The indices of basis states whose probability is non-zero.

    Example:
        >>> covered_pure_states([0.0, 0.5, 0.0, 0.5])
        [1, 3]
    """
    covered_states: list[int] = []
    # Collect indices of states with non-zero probability
    for idx, prob in enumerate(probs):
        if prob != 0:
            covered_states.append(idx)
    return covered_states