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

def _circuit_complexity_info(
    program_version: str, 
    n_list: list[int], 
    matA_dict: dict[str, list], 
    vecB_dict: dict[str, list], 
    c_list: list[int], 
    num_outs: list[int], 
) -> None:

    qubits_list, gates_list, depths_list = [], [], []
    for n in n_list:
        A_list, b_list = matA_dict[f"qubit_num={n}"], vecB_dict[f"qubit_num={n}"]
        for A, b, c, num_out in product(A_list, b_list, c_list, num_outs):
            qc = QuantumCircuit(n + num_out, num_out)            

            # Append the tested quantum subroutine (quantum program) 
            func = get_target_version(version_dict, program_version)
            qc_test = func(num_result_qubits=num_out, quadratic=A, linear=b, offset=c)
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
    matA_dict = module.config_dict["all"]["matrix_A"]
    vecB_dict = module.config_dict["all"]["vector_B"]
    c_list = module.config_dict["all"]["integer_C"]
    num_outs = module.config_dict["all"]["num_outs"]

    for program_version in sorted(versions, key=lambda v: int(v[1:])):
        print(program_version)
        _circuit_complexity_info(
            program_version, 
            qubit_nums, 
            matA_dict,
            vecB_dict,
            c_list,
            num_outs
        )