from qiskit import QuantumCircuit
import numpy as np
 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from adder_defect1 import WeightedAdder_defect1
from adder_defect2 import WeightedAdder_defect2
from adder_defect3 import WeightedAdder_defect3
from adder_defect4 import WeightedAdder_defect4
from adder_defect5 import WeightedAdder_defect5
from adder_defect6 import WeightedAdder_defect6

from data_convertion import generate_numbers
import math

def version_selection(program_name, program_version):
    '''
        select the program version to be tested

        Input variable:
            + program_name       [str] e.g. "IntegerComparator"
            + program_version    [str] e.g. "v1", "v2", "v3"
    
    '''
    if program_version[0] == "v":
        function_name = program_name + '_defect' + program_version[1:]
    elif program_version == 'raw':
        function_name = program_name
    else:
        return f"Invalid program version."

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


def info_collection(program_version, n_list, weights_dict):
    program_name = 'WeightedAdder'
    qubits_list = []
    gates_list = []
    depths_list = []
  
    for n in n_list:            
        weights_list = weights_dict[n]
        for weight in weights_list:              # calculate the number of output qubits s
            if np.sum(weight) == 0:
                s = 1
            else:
                s = 1 + math.floor(math.log2(np.sum(weight)))
            # append the tested quantum subroutine (quantum program) 
            func = version_selection(program_name, program_version)
            qc_test = func(n, weight)
            qc = QuantumCircuit(qc_test.num_qubits, s)
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
    weights_dict = {
        1: [[0], [1], [2], [3], [4]],
        2: [[0, 0], [0, 1], [1, 2], [1, 1], [2, 2]],
        3: [[0, 0, 0], [2, 0, 2], [1, 1, 0], [0, 2, 1], [1, 0, 2]],
        4: [[0, 1, 1, 1], [0, 0, 0, 0], [2, 2, 0, 0], [1, 1, 0, 0], [1, 2, 0, 1]],
        5: [[1, 0, 2, 1, 2], [0, 0, 1, 0, 0], [0, 2, 0, 1, 0], [2, 0, 1, 1, 0], [0, 0, 2, 1, 0]],
        6: [[1, 2, 2, 2, 2, 1], [0, 0, 0, 0, 0, 0], [2, 1, 0, 1, 1, 1], [1, 3, 1, 0, 2, 0], [1, 1, 0, 0, 0, 2]]
    }
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        info_collection(program_version, n_list, weights_dict)