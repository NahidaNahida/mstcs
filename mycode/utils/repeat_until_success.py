import random
import copy
from collections import defaultdict
from qiskit import QuantumCircuit
from .circuit_execution import circuit_execution

def repeat_until_success(qc: QuantumCircuit, shots: int, invalid_list: list[int]) -> dict[int, int]:
    """
    Execute a quantum circuit repeatedly until all measurement results are valid.

    This function is designed to repeatedly execute a quantum circuit and discard 
    any measurement outcomes that are considered invalid. It ensures that the final 
    result distribution contains only valid outputs, e.g., producing samples that 
    follow a uniform distribution over a specific set of values.

    Parameters
    ----------
    qc : QuantumCircuit
        The quantum circuit to be executed.
    shots : int
        The total number of measurements (shots) to collect.
    invalid_list : list of int
        List of measurement outcomes (in decimal) that are considered invalid and 
        should be excluded from the final result.

    Returns
    -------
    dict
        A dictionary mapping each valid measurement outcome to its observed count.

    Example
    -------
    >>> # Prepare a quantum circuit with 3 qubits and 3 classical bits
    >>> qc = QuantumCircuit(3, 3)
    >>> qc.h(qc.qubits[:2])
    >>> qc.measure(qc.qubits[:], qc.clbits[:])
    
    >>> # Collect 1000 valid samples, excluding 3 as invalid
    >>> final_counts = repeat_until_success(qc, 1000, [3])
    >>> print(final_counts)
    >>> # Possible output: {0: 336, 1: 307, 2: 357}
    """
    flag = 0  # Indicates the first run
    while True:
        # Execute the circuit and get raw measurement counts
        dict_counts = circuit_execution(qc, shots)
        temp_dict_counts = copy.deepcopy(dict_counts)

        # Remove invalid measurement outcomes
        keys_to_remove = [key for key in temp_dict_counts if key in invalid_list]
        for key in keys_to_remove:
            del temp_dict_counts[key]

        if flag == 0:
            # First run: initialize final_counts with valid outcomes
            flag = 1
            final_counts = copy.deepcopy(temp_dict_counts)
        else:
            # For subsequent runs, randomly sample the remaining counts to reach total shots
            samps_list = list(temp_dict_counts.keys())
            counts_list = list(temp_dict_counts.values())
            sel_samps = random.choices(samps_list, weights=counts_list, k=remained_samps)
            
            sampled_dict = {}
            # Aggregate counts from selected samples
            for sample in sel_samps:
                if sample in sampled_dict:
                    sampled_dict[sample] += 1
                else:
                    sampled_dict[sample] = 1

            # Merge new counts with previously collected valid counts
            final_counts = defaultdict(int, final_counts)
            for key, value in sampled_dict.items():
                final_counts[key] += value

        # Calculate the number of valid samples collected so far
        temp_samps = sum(final_counts.values())
        remained_samps = shots - temp_samps

        # If enough valid samples collected, return final counts
        if remained_samps == 0:
            return final_counts


def generate_invalid_numbers(total_bits: int, con_bits: int, invalid_con_list: list[int]) -> list[int]:
    """
    Generate all possible invalid measurement results given invalid control qubit values.

    When certain control qubit values are considered invalid, this function generates 
    the complete list of decimal measurement outcomes that would be invalid, assuming 
    all qubits (control + target) are measured.

    Parameters
    ----------
    total_bits : int
        Total number of qubits involved in the circuit (control + target).
    con_bits : int
        Number of control qubits.
    invalid_con_list : list of int
        List of invalid control qubit values (decimal).

    Returns
    -------
    list of int
        List of all invalid measurement outcomes in decimal form.

    Example
    -------
    n = 2  # number of target qubits
    m = 3  # number of control qubits
    invalid_con_list = [6, 7]
    invalid_num_list = generate_invalid_numbers(n + m, m, invalid_con_list)
    print(invalid_num_list)
    # Output: [6, 7, 14, 15, 22, 23, 30, 31]
    """
    high_bits = total_bits - con_bits  # Number of target qubits

    invalid_num_list = []
    for high in range(2**high_bits):
        for invalid_con in invalid_con_list:
            # Combine high bits (target qubits) and low bits (invalid control qubits)
            combined_binary = (high << con_bits) | invalid_con
            invalid_num_list.append(combined_binary)

    return invalid_num_list
