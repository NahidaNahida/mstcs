"""
This module is used to collect primary info for measuring the complexity
of the quantum circuits involved in program `IntegerComparator`, including 
the number of qubits (# Qubits), the number of basic gates (# Gates), and 
the circuit depth (Depths) shown in Table 3 of our TOSEM paper.

The results will be directly printed in the terminal.
"""

import os
from itertools import product
import importlib
from qiskit import QuantumCircuit

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

def _circuit_complexity_info(program_version: str, n_list: list[int], classical_inputs: list) -> None:
    qubits_list, gates_list, depths_list = [], [], []

    for n in n_list:
        for L, sign in classical_inputs:
            qc = QuantumCircuit(2 * n, n)   

            # Append the tested quantum subroutine (quantum program) 
            func = get_target_version(version_dict, program_version)
            qc_test = func(n, L, geq=sign)
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
    qubit_nums = set()
    classical_inputs = set()
    versions = set()

    # We assume that the classical inputs do not vary with program versions.
    # We only discuss RQ1 and RQ3 comforting the follwing data format.
    for i in [1, 3]:  
        module = importlib.import_module(f"..config.RQ{i}_config", package=__package__)
        versions.update(module.config_dict["all"]["versions"])
        qubit_nums.update(module.config_dict["all"]["qubit_list"])
        classical_inputs_tuple = product(
            module.config_dict["all"]["L_list"],
            module.config_dict["all"]["sign_list"]
         )
        classical_inputs.update(classical_inputs_tuple)

    for program_version in sorted(versions, key=lambda v: int(v[1:])):
        print(program_version)
        _circuit_complexity_info(program_version, list(qubit_nums), list(classical_inputs))