"""
Quantum State Distribution Utilities
------------------------------------

This module provides helper functions for generating distributions,
state coverage, and control qubit settings in quantum software testing
using our proposed mixed-state test cases (MSTCs). 

Thie module is scalable for configuration that supports updating new modes.

Notes
-----
- The design follows a dictionary-based mode selection, making it
  straightforward to extend with additional distribution schemes,
  state coverage strategies, or control-target relationships.
- All outputs are plain Python lists or integers for compatibility.
"""

import numpy as np
from typing import Literal
 

def pure_state_distribution(qubit_num: int, mode: Literal["uniform"]) -> list[float]:
    r"""
    Generate a probability distribution over pure states. 

    That is to say, for a mixed state 
    
    $\rho = \sum_{z\in P} p_{\mathcal{Z}}(z) \ket{\varphi_z} \bra{\varphi_z}$,

    This function aims to control $p_{\mathcal{Z}}(z)$.

    Parameters
    ----------
    qubit_num : int
        Number of qubits in the system.
    mode : {"uniform"}
        Distribution scheme. Currently only "uniform" is supported,
        which assigns equal probability to all computational basis states.

    Returns
    -------
    list
        A list of probabilities (length 2**qubit_num), summing to 1.

    Examples
    --------
    >>> pure_state_distribution(2, mode="uniform")
    [0.25, 0.25, 0.25, 0.25]
    """
    distribution_dict = {
        # Uniform distribution of pure states
        "uniform": list(np.ones(2 ** qubit_num) / (2 ** qubit_num)) 
    }

    returned_distribution = distribution_dict[mode]
    return returned_distribution

def control_qubit_numbers(
    target_num: int,
    mode: Literal["equal"]
) -> int:
    control_qubit_num_dict = {
        # Equal numbers of control and target qubits (i.e., $m = n$)
        "equal": target_num
    }

    return control_qubit_num_dict[mode]