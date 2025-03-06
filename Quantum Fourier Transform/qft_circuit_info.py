from qiskit import QuantumCircuit
 
import numpy as np
import csv
 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from qft_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest

from qft_defect1 import QFT_defect1
from qft_defect2 import QFT_defect2
from qft_defect3 import QFT_defect3
from qft_defect4 import QFT_defect4
from qft_defect5 import QFT_defect5
from qft_defect6 import QFT_defect6

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


def info_collection(program_version, n_list, if_swap_list):
    program_name = 'QFT'
    qubits_list = []
    gates_list = []
    depths_list = []
  
    for n in n_list: 
        for if_swap in if_swap_list:
                qc = QuantumCircuit(n, n)
                # append the tested quantum subroutine (quantum program) 
                func = version_selection(program_name, program_version)
                qc_test = func(num_qubits=n, do_swaps=if_swap)
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
    if_swap_list = [True, False]
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        info_collection(program_version, n_list, if_swap_list)