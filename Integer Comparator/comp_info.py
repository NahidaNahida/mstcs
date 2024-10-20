from qiskit.circuit import QuantumRegister, QuantumCircuit, ParameterVector
from qiskit.quantum_info import Statevector
from qiskit.circuit.library import RYGate
from qiskit import QuantumCircuit, transpile, assemble, execute
 
import numpy as np
 
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comp import IntegerComparator
from comp_defect1 import IntegerComparator_defect1
from comp_defect2 import IntegerComparator_defect2
from comp_defect3 import IntegerComparator_defect3
from comp_defect4 import IntegerComparator_defect4
from comp_defect5 import IntegerComparator_defect5


def version_selection(program_name, program_version):
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


def info_collection(program_version, n_list, L_list, sign_list):
    program_name = 'IntegerComparator'
    qubits_list = []
    gates_list = []
    depths_list = []
  
    for n in n_list:            
        for L in L_list:
            for sign in sign_list:
                qc = QuantumCircuit(2 * n, n)            
                # append the tested quantum subroutine (quantum program) 
                func = version_selection(program_name + '_defect', program_version)
                qc_test = func(n, L, geq=sign)
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
    n_list = range(1, 6)
    L_list = np.arange(-5, 5.1, 1)
    sign_list =  [True, False]
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5']:
        print(program_version)
        program_version = program_version[1:]
        info_collection(program_version, n_list, L_list, sign_list)