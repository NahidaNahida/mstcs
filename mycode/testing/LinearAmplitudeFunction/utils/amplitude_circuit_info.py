"""
This module is used to collect primary info for measuring the complexity
of the quantum circuits involved in program `LinearAmplitudeFunction`, including 
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
        for slop, offset, domain, image in classical_inputs:
            # Append the tested quantum subroutine (quantum program) 
            func = get_target_version(version_dict, program_version)
            qc = func(n, slop, offset, domain=domain, image=image)

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

if __name__ == "__main__":
    qubit_nums = set()
    classical_inputs = set()
    versions = set()

    # We assume that the classical inputs do not vary with program versions.
    # We only discuss RQ1 and RQ3 comforting the follwing data format.
    for i in [1, 3]:  
        module = importlib.import_module(f"..config.RQ{i}_config", package=__package__)
        versions.update(module.config_dict["all"]["versions"])
        qubit_nums.update(module.config_dict["all"]["qubit_list"])
        # Collect classical inputs and convert the inner list or other non-hashed objects into tuples
        classical_inputs_tuple = product(
            (tuple(slop) if isinstance(slop, list) else slop for slop in module.config_dict["all"]["slop_list"]),
            (tuple(offset) if isinstance(offset, list) else offset for offset in module.config_dict["all"]["offset_list"]),
            (tuple(domain) if isinstance(domain, list) else domain for domain in module.config_dict["all"]["domain_list"]),
            (tuple(image) if isinstance(image, list) else image for image in module.config_dict["all"]["image_list"])
        )
        classical_inputs.update(classical_inputs_tuple)
 
    for program_version in sorted(versions, key=lambda v: int(v[1:])):
        print(program_version)
        _circuit_complexity_info(program_version, list(qubit_nums), list(classical_inputs))