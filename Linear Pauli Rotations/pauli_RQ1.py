from qiskit import QuantumCircuit 
import numpy as np
import csv
import math
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from pauli_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution
from preparation_circuits import *

from pauli_defect1 import LinearPauliRotations_defect1
from pauli_defect2 import LinearPauliRotations_defect2
from pauli_defect3 import LinearPauliRotations_defect3
from pauli_defect4 import LinearPauliRotations_defect4
from pauli_defect5 import LinearPauliRotations_defect5
from pauli_defect6 import LinearPauliRotations_defect6

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

def testing_process_PSTCs(program_version, n_list, slop_list, offset_list, repeats=20):
    program_name = 'LinearPauliRotations'
    default_shots = 1024
    candidate_initial_states = [0, 1]
    basis = 'Y'          # Oracle is default for Y basis 
    
    recorded_result = []  
    for n in n_list:  
        initial_states = generate_numbers(n, len(candidate_initial_states))
        start_time = time.time()
        pre_time = 0                        # record time for state preparation
        num_classical_inputs = len(slop_list) * len(offset_list)
        for _ in range(repeats):          
            test_cases = 0
            for slop in slop_list:
                for offset in offset_list:
                    for initial_state in initial_states:
                        test_cases += 1
                        number = int(''.join(map(str, initial_state)), 2)
                        qc = QuantumCircuit(n + 1, 1)

                        pre_start_time = time.time()
                        initial_state = initial_state[::-1]
                        for index, val in enumerate(initial_state):
                            if candidate_initial_states[val] == 1:
                                qc.x(index)
                        pre_end_time = time.time()
                        pre_time += pre_end_time - pre_start_time
                                        
                        # append the tested quantum subroutine (quantum program)
                        func = version_selection(program_name, program_version)
                        qc_test = func(n, slop, offset, basis)
                        qc.append(qc_test, qc.qubits)
                        qc.measure(qc.qubits[-1], qc.clbits[-1])
                        
                        # execute the program and derive the outputs
                        dict_counts = circuit_execution(qc, default_shots)
                    
                        # obtain the samples (measurement results) of the tested program
                        test_samps = []
                        for (key, value) in dict_counts.items():
                            test_samps += [key] * value
                        
                        # generate the samples that follow the expected probability distribution
                        exp_probs = PSTC_specification(number, slop, offset)
                        exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))                    

                        # derive the test result by nonparametric hypothesis test
                        test_result = OPO_UTest(exp_samps, test_samps)

        dura_time = time.time() - start_time
        recorded_result.append([n, 
                                test_cases, 
                                dura_time / num_classical_inputs / repeats, 
                                pre_time / num_classical_inputs / repeats])
  
    # save the data
    file_name = "RQ1_" + program_name + '_' + program_version + "_PSTC" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['n', '# test_cases', 'ave_time(entire)', 'ave_time(prepare)']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('PSTCs done!')

def testing_process_MSTCs(program_version, n_list, slop_list, offset_list, mode, repeats=20):    
    program_name = 'LinearPauliRotations'
    default_shots = 1024
    basis = 'Y'          # Oracle is default for Y basis 
    
    recorded_result = []  

    for n in n_list:  
        # define the uniform distribution for the ensemble
        pure_states_distribution = list(np.ones(2 ** n) / (2 ** n))
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        # determine m = n for this experiment
        m = n
        num_classical_inputs = len(slop_list) * len(offset_list)
        start_time = time.time()
        pre_time = 0                        # record time for state preparation
        for _ in range(repeats):
            test_cases = 0
            for slop in slop_list:
                for offset in offset_list:
                    test_cases += 1
                    qc = QuantumCircuit(m + n + 1, 1)

                    pre_start_time = time.time()
                    # prepare the control state
                    qc.h(qc.qubits[:m])
                    # mixed state preparation
                    if mode == 'bits':
                        qc = bit_controlled_preparation_1MS(n, m, qc)
                    elif mode == 'qubits':
                        qc = qubit_controlled_preparation_1MS(n, m, qc)
                    pre_end_time = time.time()
                    pre_time += pre_end_time - pre_start_time    

                    # append the tested quantum subroutine (quantum program) 
                    func = version_selection(program_name, program_version)
                    qc_test = func(n, slop, offset, basis)
                    qc.append(qc_test, qc.qubits[m:])
                    qc.measure(qc.qubits[-1],qc.clbits[-1])
                    
                    # execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, default_shots)
                
                    # obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        test_samps += [key] * value
                    
                    # generate the samples that follow the expected probability distribution
                    exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, slop, offset)
                    exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                    # derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                        
        dura_time = time.time() - start_time
        recorded_result.append([n, 
                                test_cases, 
                                dura_time / num_classical_inputs / repeats, 
                                pre_time / num_classical_inputs / repeats])
 
    # save the data
    file_name = "RQ1_" + program_name + '_' + program_version + '_' + mode + "_MSTC" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['n', '# test_cases', 'ave_time(entire)', 'ave_time(prepare)']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs ' + mode + ' done!')


if __name__ == '__main__':
    # the setting to generate classical inputs
    n_list = range(1, 7)
    slop_list = np.arange(-math.pi, math.pi + 1e-9, math.pi/2)
    offset_list = np.arange(-math.pi, math.pi + 1e-9, math.pi/2)

    # the test processes
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        testing_process_PSTCs(program_version, n_list, slop_list, offset_list)
        testing_process_MSTCs(program_version, n_list, slop_list, offset_list, 'bits')
        testing_process_MSTCs(program_version, n_list, slop_list, offset_list, 'qubits')