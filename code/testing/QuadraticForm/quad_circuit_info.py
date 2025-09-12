from qiskit import QuantumCircuit 
import numpy as np
 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from quad_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution

from quad_defect1 import QuadraticForm_defect1
from quad_defect2 import QuadraticForm_defect2
from quad_defect3 import QuadraticForm_defect3
from quad_defect4 import QuadraticForm_defect4
from quad_defect5 import QuadraticForm_defect5
from quad_defect6 import QuadraticForm_defect6

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


def info_collection(program_version, n_list, matA_dict, vecB_dict, c_list, num_out=2):
    qubits_list = []
    gates_list = []
    depths_list = []
  
    program_name = 'QuadraticForm'
 
    for n in n_list:            
        A_list, b_list = matA_dict[n], vecB_dict[n]
        for c in c_list:
            for A in A_list:
                for b in b_list:
                    qc = QuantumCircuit(n + num_out, num_out)            
                    # append the tested quantum subroutine (quantum program)
                    func = version_selection(program_name, program_version)
                    qc_test = func(num_result_qubits=num_out, quadratic=A, linear=b, offset=c)
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
    n_list = range(2, 7)
    matA_dict = {
        2: [[[0, 0], [0, 1]], 
            [[-1, 2], [1, 1]], 
            [[2, 2], [0, -1]], 
            [[-1, 0], [1, -1]], 
            [[0, 0], [0, -1]]],
        3: [[[0, 0, 1], [0, 1, -1], [1, -1, 2]], 
            [[1, -1, 2], [1, 1, 0], [0, 0, 0]], 
            [[2, 2, 0], [0, -1, -2], [0, 1, -1]], 
            [[0, -1, 0], [1, 1, -1], [1, 2, 1]], 
            [[0, 0, 0], [0, -1, -1], [1, 1, 1]]],
        4: [[[0, 0, 0, 0], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 0, 0]], 
            [[-1, 1, 2, 1], [1, 1, 0, 1], [1, 1, 1, 1], [0, 0, 1, 0]], 
            [[2, 2, 2, 2], [0, -1, 0, 0], [1, 1, -2, 1], [0, 0, 0, 0]], 
            [[-1, 0, -1, 0], [1, -1, 1, -1], [0, 1, 0, 1], [1, 2, 1, 2]], 
            [[0, 0, 1, 1], [0, -1, 0, -2], [1, 0, 2, 1], [0, 0, 0, 2]]],
        5: [[[1, 0, 0, 0, 0], [0, 1, 0, 0, 0], [0, 0, 1, 0, 0], [0, 0, 0, 1, 0], [0, 0, 0, 0, 1]], 
            [[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]], 
            [[-1, 2, 0, 1, 0], [0, -1, 1, -2, 0], [1, -2, 0, 1, 2], [0, 0, 1, 2, 1], [0, 1, 0, 1, 0]], 
            [[-1, 0, -1, 0, -1], [1, -1, 1, -1, 1], [2, -2, 2, -2, 2], [0, 1, 2, 0, 1], [0, 1, 2, 1, 0]], 
            [[0, 0, 0, 1, 0], [0, -1, -1, 0, 2], [2, 1, 0, 1, -1], [1, 1, -1, -1, 0], [0, 0, 0, 1, 0]]],
        6: [[[1, 0, 0, 0, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 1, 0, 0], [0, 0, 0, 0, 1, 0], [0, 0, 0, 0, 0, 1]], 
            [[1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1]], 
            [[-1, 2, 1, 0, 1, 0], [0, -1, 1, -2, 0, -1], [1, -2, 0, 1, 2, 1], [0, 0, 1, 2, 0, 1], [0, 1, 0, 1, 0, 1], [-1, 0, 1, 2, 0, 1]], 
            [[-1, 0, -1, 0, -1, 0], [1, -1, 1, -1, 1, -1], [2, -2, 2, -2, 2, -2], [0, 1, 2, 0, 1, 2], [0, 1, 2, 1, 0, 1], [2, 1, 1, 2, 1, 0]], 
            [[0, 0, 0, 1, 0, 0], [0, -1, -1, 0, 2, 2], [2, 1, 0, 1, -1, 0], [1, 1, -1, -1, 0, 0], [0, 1, 0, 0, 1, 0], [1, 2, 1, 2, 0, 1]]]
    }
    vecB_dict = {
        2: [[0, 0], [0, 1], [-1, 2], [1, 1], [2, 2]],
        3: [[0, 0, 1], [0, 1, -1], [1, -1, 2], [1, -1, 2], [1, 1, 0]], 
        4: [[1, -2, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 2, 0], [-1, 1, 2, 1]],  
        5: [[1, 1, 1, 1, 1], [-1, 2, 0, 1, 0],  [0, 0, 1, 2, 1], [1, 1, -1, -1, 0], [0, 0, 0, 1, 0]],
        6: [[-2, 1, 0, -1, 2, 1], [0, 0, 0, 1, 0, 0], [1, 1, 1, 1, 1, 1], [0, 1, 0, 1, 0, 1], [-1, -1, -1, -1, -1, -1]]
    }
    C_list = np.arange(-2, 3, 1)
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        info_collection(program_version, n_list, matA_dict, vecB_dict, C_list)
