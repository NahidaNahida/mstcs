from qiskit import QuantumCircuit 
from qiskit import Aer, execute
from qiskit.quantum_info import Statevector

import numpy as np
import csv

import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from adder_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution
from preparation_circuits import bit_controlled_preparation_1MS, qubit_controlled_preparation_1MS

from code.WeightedAdder.programs.adder import WeightedAdder
from adder_defect1 import WeightedAdder_defect1
from adder_defect2 import WeightedAdder_defect2
from adder_defect3 import WeightedAdder_defect3
from adder_defect4 import WeightedAdder_defect4
from adder_defect5 import WeightedAdder_defect5
from adder_defect6 import WeightedAdder_defect6

import math
import time

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

def testing_process_PSTCs(program_version, n_list, weights_dict, repeats=20):
    program_name = 'WeightedAdder'
    default_shots = 1024
    candidate_initial_states = [0, 1]

    recorded_result = [] 
    for n in n_list:            
        initial_states_list = generate_numbers(n, len(candidate_initial_states))
        weights_list = weights_dict[n]
        num_classical_inputs = len(weights_list)
        start_time = time.time()
        pre_time = 0                        # record time for state preparation
 
        for weight in weights_list:              # calculate the number of output qubits s
            print(weight)
            if np.sum(weight) == 0:
                s = 1
            else:
                s = 1 + math.floor(math.log2(np.sum(weight)))

            # append the tested quantum subroutine (quantum program) 
            func = version_selection(program_name, program_version)
            qc_test = func(n, weight)

            for initial_states in initial_states_list:
                number = int(''.join(map(str, initial_states)), 2)

                pre_start_time = time.time()
                initial_states = initial_states[::-1]
                qc = QuantumCircuit(qc_test.num_qubits, s)
                # state preparation
                for index, val in enumerate(initial_states):
                    if candidate_initial_states[val] == 1:
                        qc.x(index)
                pre_end_time = time.time()
                pre_time += pre_end_time - pre_start_time

                qc.append(qc_test, qc.qubits)
                qc.measure(qc.qubits[n: n + s],qc.clbits)

                # execute the program and derive the outputs
                backend = Aer.get_backend('statevector_simulator')
                # 运行线路并获取结果
                job = execute(qc, backend)
                result = job.result()
                # 提取态矢量
                full_statevector = result.get_statevector()
                stat_full = Statevector(full_statevector)
                test_probs = stat_full.probabilities(qargs=list(range(n, n + s)))
           
                
                # generate the samples that follow the expected probability distribution
                exp_probs = PSTC_specification(s, initial_states, weight)

                test_result = (list(test_probs) == list(exp_probs))
                print("quantum_input={}, test_probs={}, exp_probs={}, test_result={}".format(number, test_probs, exp_probs, test_result))

if __name__ == '__main__':
    # the setting to generate classical inputs
    n_list = [3]
    weights_dict = {
        3: [[0, 0, 0], [2, 0, 2], [1, 1, 0], [0, 2, 1], [1, 0, 2]]
    }
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        testing_process_PSTCs(program_version, n_list, weights_dict)