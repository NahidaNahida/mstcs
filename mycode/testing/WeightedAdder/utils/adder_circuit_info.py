"""
This module is used to collect primary info for measuring the complexity
of the quantum circuits involved in program `WeightedAdder`, including 
the number of qubits (# Qubits), the number of basic gates (# Gates), and 
the circuit depth (Depths) shown in Table 3 of our TOSEM paper.

The results will be directly printed in the terminal.
"""


import os
import importlib
from qiskit import QuantumCircuit
import numpy as np
import math
from ....utils import (
    import_versions,
    get_target_version, 
    full_circuit_decomposition,
    gate_count,
    depth_count,
    qubit_count
)
 
from ..config import program_name

# =================================================================
# Get the file directory
current_dir = os.path.dirname(__file__)
version_dir = os.path.join(os.path.dirname(current_dir), "programs")
config_dir = os.path.join(os.path.dirname(current_dir), "config")

# Import the program versions under the same directory
version_dict = import_versions(program_name, version_dir)
 
def _circuit_complexity_info(
    program_version: str, 
    n_list: list[int], 
    weights_dict: dict[str, list[list]]
) -> None:
    qubits_list, gates_list, depths_list = [], [], []

    for n in n_list:            
        weights_list = weights_dict[f"qubit_num={n}"]  
        for weight in weights_list:    # Calculate the number of output qubits s
            if np.sum(weight) == 0:
                s = 1
            else:
                s = 1 + math.floor(math.log2(np.sum(weight)))
            
            # Append the tested quantum subroutine (quantum program) 
            func = get_target_version(version_dict, program_version)
            qc_test = func(n, weight)
            qc = QuantumCircuit(qc_test.num_qubits, s)
            qc.append(qc_test, qc.qubits)

            # Obtain the circuit being fully decomposed
            dec_qc = full_circuit_decomposition(qc)

            # Collect information of quantum circuits
            qubits_list.append(qubit_count(dec_qc))
            gates_list.append(gate_count(dec_qc))
            depths_list.append(depth_count(dec_qc))

    for name, values in {
        "qubits": qubits_list,
        "gates": gates_list,
        "depth": depths_list
    }.items():
        print(f"#{name} : [{min(values)}, {max(values)}]")
   
if __name__ == '__main__':
    versions = set()
    
    # We assume that the classical inputs do not vary with program versions.
    # We only discuss RQ1 for convenience.
    module = importlib.import_module(f"..config.RQ1_config", package=__package__)
    versions.update(module.config_dict["all"]["versions"])
    qubit_nums = module.config_dict["all"]["qubit_list"]
    weight_dict= module.config_dict["all"]["weight_dict"]

    for program_version in sorted(versions, key=lambda v: int(v[1:])):
        print(program_version)
        _circuit_complexity_info(
            program_version, 
            qubit_nums, 
            weight_dict
        )