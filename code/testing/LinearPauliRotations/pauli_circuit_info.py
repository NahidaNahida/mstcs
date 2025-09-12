from qiskit.circuit import QuantumCircuit
import numpy as np
 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pauli_defect1 import LinearPauliRotations_defect1
from pauli_defect2 import LinearPauliRotations_defect2
from pauli_defect3 import LinearPauliRotations_defect3
from pauli_defect4 import LinearPauliRotations_defect4
from pauli_defect5 import LinearPauliRotations_defect5
from pauli_defect6 import LinearPauliRotations_defect6

import math

def execute_function(program_name, program_version):
    function_name = program_name + program_version
    if function_name in globals():
        func = globals()[function_name]
        return func
    else:
        return f"Function '{function_name}' not found."

# thoroughly decompose a qc until only basis gates
def fully_decompose(qc):
    while True:
        decomposed_qc = qc.decompose()
        if decomposed_qc == qc:
            break
        qc = decomposed_qc
    return qc


def info_collection(program_version, n_list, slop_list, offset_list):
    qubits_list = []
    gates_list = []
    depths_list = []
  
    program_name = 'LinearPauliRotations'
    basis = 'Y'          # Oracle is default for Y basis 
 
    for n in n_list:            
        for slop in slop_list:
            for offset in offset_list:
                qc = QuantumCircuit(n + 1, 1)
                # append the tested quantum subroutine (quantum program)
                func = execute_function(program_name + '_defect', program_version)
                qc_test = func(n, slop, offset, basis)
                qc.append(qc_test, qc.qubits)
                    
                # counts information of quantum circuits
                qubits_list.append(qc.num_qubits)
                decomposed_circ = fully_decompose(qc)
                depths = decomposed_circ.depth()
                gate_dict = decomposed_circ.count_ops()
                gates = sum(gate_dict.values())
                gates_list.append(gates)
                depths_list.append(depths)

    print('#qubits : [{}, {}]'.format(min(qubits_list), max(qubits_list)))
    print('#gates : [{}, {}]'.format(min(gates_list), max(gates_list)))
    print('#depth : [{}, {}]'.format(min(depths_list), max(depths_list)))
   
if __name__ == '__main__':
    # the setting to generate classical inputs
    n_list = range(1, 7)
    slop_list = np.arange(-math.pi, math.pi + 1e-9, math.pi/2)
    offset_list = np.arange(-math.pi/2, math.pi/2 + 1e-9, math.pi/4)
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        program_version = program_version[1:]
        info_collection(program_version, n_list, slop_list, offset_list)