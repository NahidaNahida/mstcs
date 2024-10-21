from qiskit.circuit import QuantumRegister, QuantumCircuit, ParameterVector
 
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
 
import numpy as np
import csv

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from adder_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution

from adder import WeightedAdder
from adder_defect1 import WeightedAdder_defect1
from adder_defect2 import WeightedAdder_defect2
from adder_defect3 import WeightedAdder_defect3
from adder_defect4 import WeightedAdder_defect4
from adder_defect5 import WeightedAdder_defect5

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
    

def testing_process_PSTCs(program_version, n_list, weights_dict, repeats=20):
    program_name = 'WeightedAdder'
    default_shots = 1024
    candidate_initial_states = [0, 1]

    recorded_result = [] 
    for n in n_list:            
        initial_states_list = generate_numbers(n, len(candidate_initial_states))
        total_failures = 0
        weights_list = weights_dict[n]
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:              # calculate the number of output qubits s
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))
                # append the tested quantum subroutine (quantum program) 
                func = version_selection(program_name, program_version)
                qc_test = func(n, weight)

                for initial_states in initial_states_list:
                    test_cases += 1
                    number = int(''.join(map(str, initial_states)), 2)
                    initial_states = initial_states[::-1]
                    qc = QuantumCircuit(qc_test.num_qubits, s)

                    # state preparation
                    for index, val in enumerate(initial_states):
                        if candidate_initial_states[val] == 1:
                            qc.x(index)
                                    
                    qc.append(qc_test, qc.qubits)
                    qc.measure(qc.qubits[n: n + s],qc.clbits)

                    # execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, default_shots)

                    # obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        test_samps += [key] * value
                    
                    # generate the samples that follow the expected probability distribution
                    exp_probs = PSTC_specification(s, initial_states, weight)
                    exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                    # derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)

                    if test_result == 'fail':
                        total_failures += 1    

        recorded_result.append([n, test_cases, total_failures / test_cases / repeats])
    
    # save the data
    file_name = "RQ3_" + program_name + '_' + program_version + "_PSTC" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['n','# test_cases', 'ave_fault']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('PSTCs done!')

 
def testing_process_MSTCs(program_version, n_list, weights_dict, repeats=20):
    program_name = 'WeightedAdder'
    default_shots = 1024

    recorded_result = [] 
    for n in n_list:  
        # define the uniform distribution for the ensemble
        pure_states_distribution = list(np.ones(2 ** n) / (2 ** n))
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        total_failures = 0
        weights_list = weights_dict[n]
        for _ in range(repeats):
            test_cases= 0 
            for weight in weights_list:
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))
                # append the tested quantum subroutine (quantum program) 
                func = version_selection(program_name, program_version)
                qc_test = func(n, weight)
                    
                qc = QuantumCircuit(n + qc_test.num_qubits, s)
                qc.h(qc.qubits[:n])
                
                for index in range(n, 2 * n):
                    qc.cx(qc.qubits[index - n], qc.qubits[index])
                for i in range(n):
                    qc.measure(qc.qubits[i], qc.clbits[-1])
                
                qc.append(qc_test, qc.qubits[n:])
                qc.measure(qc.qubits[2 * n: 2 * n + s],qc.clbits)
                    
                # execute the program and derive the outputs
                dict_counts = circuit_execution(qc, default_shots)

                # obtain the samples (measurement results) of the tested program
                test_samps = []
                for (key, value) in dict_counts.items():
                    test_samps += [key] * value
                
                # generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, n, s, weight)
                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                # derive the test result by nonparametric hypothesis test
                test_result = OPO_UTest(exp_samps, test_samps)
                    
                if test_result == 'fail':
                    total_failures += 1
                        
                test_cases += 1
        recorded_result.append([n, test_cases, total_failures / test_cases / repeats])

    # save the data
    file_name = "RQ3_" + program_name + '_' + program_version + "_MSTC" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['n','# test_cases', 'ave_fault']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs done!')

if __name__ == '__main__':
    # the setting to generate classical inputs
    n_list = range(1, 6)
    weights_dict = {
        1: [[0], [1], [2]],
        2: [[0, 0], [0, 1], [1, 2], [1, 1], [2, 2]],
        3: [[0, 0, 0], [2, 0, 2], [1, 1, 0], [0, 2, 1], [1, 0, 2]],
        4: [[0, 1, 1, 1], [0, 0, 0, 0], [2, 2, 0, 0], [1, 1, 0, 0], [1, 2, 0, 1]],
        5: [[1, 0, 2, 1, 2], [0, 0, 1, 0, 0], [0, 2, 0, 1, 0], [2, 0, 1, 1, 0], [0, 0, 2, 1, 0]]
    }
    # the test processes
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5']:
        print(program_version)
        testing_process_PSTCs(program_version, n_list, weights_dict)
        testing_process_MSTCs(program_version, n_list, weights_dict)