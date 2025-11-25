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

if __name__ == "__main__":
    """
    Unit / Integration Testing for helper functions.
    Run:
        python mycode/utils/data_conversion.py
    """
    # ------------------------
    # Test inputs
    # ------------------------

    def test_input_generate_numbers():
        # Simple small case (n=2, m=2)
        return {"n": 2, "m": 2}

    def test_input_outputdict2probs():
        # Suppose 2 qubits, outcomes 0 and 3 appear equally
        return {"dict": {0: 5, 3: 5}, "n": 2}

    def test_input_outputdict2samps():
        return {"dict": {0: 2, 1: 1}}

    def test_input_covered_states():
        return {"probs": [0.0, 0.2, 0.0, 0.8]}
    
    # ------------------------
    # Unit Tests
    # ------------------------

    def unit_test_generate_numbers(inp):
        result = generate_numbers(inp["n"], inp["m"])

        # Expected length = m^n
        assert len(result) == inp["m"] ** inp["n"]

        # Check each element is a list of length n
        for entry in result:
            assert len(entry) == inp["n"]

        # Check lexicographic order for small test case
        if inp["n"] == 2 and inp["m"] == 2:
            assert result == [
                [0, 0],
                [0, 1],
                [1, 0],
                [1, 1],
            ]


    def unit_test_outputdict2probs(inp):
        prob = outputdict2probs(inp["dict"], inp["n"])
        assert np.isclose(sum(prob), 1.0)

        # For the example, only 0 and 3 should be 0.5 each
        assert np.isclose(prob[0], 0.5)
        assert np.isclose(prob[3], 0.5)
        assert prob[1] == 0
        assert prob[2] == 0


    def unit_test_outputdict2samps(inp):
        samps = outputdict2samps(inp["dict"])
        assert sorted(samps) == [0, 0, 1]   # frequency check
        assert len(samps) == 3


    def unit_test_covered_states(inp):
        covered = covered_pure_states(inp["probs"])
        assert covered == [1, 3]

    # ------------------------
    # Integration Tests
    # ------------------------

    def integration_test_probs_to_states(_):
        """
        Test pipeline:
            counts → probs → covered states
        """
        counts = {0: 1, 2: 3}
        probs = outputdict2probs(counts, n=2)
        covered = covered_pure_states(probs) # type: ignore

        # Only states 0 and 2 appear
        assert covered == [0, 2]
        assert np.isclose(sum(probs), 1.0)


    def integration_test_generate_and_check(_):
        """
        Ensure generate_numbers + coverage recognition works together.
        """
        states = generate_numbers(2, 2)
        # states = [(0,0),(0,1),(1,0),(1,1)]
        assert [0,0] in states
        assert [1,1] in states
        assert len(states) == 4

        # create arbitrary probability
        probs = [0.2, 0, 0.3, 0.5]
        covered = covered_pure_states(probs)
        assert covered == [0, 2, 3]

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {
            "input": test_input_generate_numbers,
            "function": unit_test_generate_numbers,
        },
        "1": {
            "input": test_input_outputdict2probs,
            "function": unit_test_outputdict2probs,
        },
        "2": {
            "input": test_input_outputdict2samps,
            "function": unit_test_outputdict2samps,
        },
        "3": {
            "input": test_input_covered_states,
            "function": unit_test_covered_states,
        },
        "4": {
            "input": lambda: None,
            "function": integration_test_probs_to_states,
        },
        "5": {
            "input": lambda: None,
            "function": integration_test_generate_and_check,
        }
    }

    for id, exec_dict in executed_test.items():
        print(f"test_id={id}:")
        test_input = exec_dict["input"]()
        try:
            exec_dict["function"](test_input)
            print("pass")
        except AssertionError as e:
            print("fail")
            raise