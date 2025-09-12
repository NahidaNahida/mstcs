import numpy as np
import csv
import os
import math, time
from typing import Literal

from qiskit import QuantumCircuit

from ....utils import (
    generate_numbers, 
    loader_main, 
    circuit_execution, 
    OPO_UTest,
    csv_saving,
    RQ_saving_dir,
    pure_state_distribution,
    covered_pure_states
)
from ....config.csv_header import HEADER_DICT

from . import PSTC_specification, MSTC_specification
from . import default_shots, program_name, candidate_initial_states

current_dir = os.path.dirname(__file__)
version_dir = os.path.join(os.path.dirname(current_dir), "programs")

_RQ_NAME = "RQ1"
header = HEADER_DICT[_RQ_NAME]

def testing_process_PSTCs(
    program_version: str, 
    n_list: list[int], 
    weights_dict: dict[int, list[list]], 
    repeats: int = 20
):
    recorded_result = [] 
    for n in n_list:            
        initial_states_list = generate_numbers(
            n, 
            len(candidate_initial_states)
        )
        weights_list = weights_dict[n]
        num_classical_inputs = len(weights_list)
        start_time = time.time()
        pre_time = 0                                # Record time for state preparation
        for _ in range(repeats):                    # Independent repeats
            test_cases = 0
            for weight in weights_list:             # Calculate the number of output qubits s
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # Append the tested quantum subroutine (quantum program) 
                func = loader_main(program_name, version_dir, program_version)
                qc_test = func(n, weight)

                for initial_states in initial_states_list:
                    test_cases += 1
                    number = int(''.join(map(str, initial_states)), 2)

                    pre_start_time = time.time()
                    initial_states = initial_states[::-1]
                    qc = QuantumCircuit(qc_test.num_qubits, s)
                    # State preparation
                    for index, val in enumerate(initial_states):
                        if candidate_initial_states[val] == 1:
                            qc.x(index)
                    pre_end_time = time.time()
                    pre_time += pre_end_time - pre_start_time

                    qc.append(qc_test, qc.qubits)
                    qc.measure(qc.qubits[n: n + s],qc.clbits)

                    # Execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, default_shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        test_samps += [key] * value
                    
                    # Generate the samples that follow the expected probability distribution
                    exp_probs = PSTC_specification(s, initial_states, weight)
                    exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                    # derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)

        dura_time = time.time() - start_time
        recorded_result.append([
            n, 
            test_cases, 
            dura_time / num_classical_inputs / repeats, 
            pre_time / num_classical_inputs / repeats
        ])

    # Save the data
    save_dir = RQ_saving_dir(_RQ_NAME, program_name)
    csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, "PSTC", recorded_result)

def testing_process_MSTCs(
    program_version: str, 
    n_list: list[int],
    weights_dict: dict, 
    pre_mode: Literal["bits", "qubits"], 
    repeats: int = 20
):
    recorded_result = [] 
    for n in n_list:  
        # define the uniform distribution for the ensemble
        pure_states_distribution = pure_state_distribution(n, "uniform")
        
        # cover all the classical states            
        covered_numbers = covered_pure_states(n, "all_basis")
        weights_list = weights_dict[n]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        # determine m = n for this experiment
        pre_time = 0                        # record time for state preparation
        m = n
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
                
                test_cases += 1
                qc = QuantumCircuit(m + qc_test.num_qubits, s)

                pre_start_time = time.time() 
                # prepare the control state
                qc.h(qc.qubits[:m])
                # mixed state preparation
                if pre_mode == 'bits':
                    qc = bit_controlled_preparation_1MS(n, m, qc)
                elif pre_mode == 'qubits':
                    qc = qubit_controlled_preparation_1MS(n, m, qc)
                pre_end_time = time.time()
                pre_time += pre_end_time - pre_start_time

                qc.append(qc_test, qc.qubits[m:])
                qc.measure(qc.qubits[n + m: n + m + s],qc.clbits[:])
                    
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
                    
        dura_time = time.time() - start_time
        recorded_result.append([n, 
                                test_cases, 
                                dura_time / num_classical_inputs / repeats, 
                                pre_time / num_classical_inputs / repeats])
 
    # save the data
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    saving_path = os.path.join(root_dir, 
                               "data", 
                               "raw_data_for_empirical_results",
                               "RQ1",
                               program_name)
    file_name = "RQ1_" + program_name + '_' + program_version + '_' + pre_mode + "_MSTC" + ".csv"
    with open(os.path.join(saving_path, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['n', '# test_cases', 'ave_time(entire)', 'ave_time(prepare)']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs ' + pre_mode + ' done!')

if __name__ == '__main__':
    # the setting to generate classical inputs
    n_list = range(1, 7)
    weights_dict = {
        1: [[0], [1], [2], [3], [4]],
        2: [[0, 0], [0, 1], [1, 2], [1, 1], [2, 2]],
        3: [[0, 0, 0], [2, 0, 2], [1, 1, 0], [0, 2, 1], [1, 0, 2]],
        4: [[0, 1, 1, 1], [0, 0, 0, 0], [2, 2, 0, 0], [1, 1, 0, 0], [1, 2, 0, 1]],
        5: [[1, 0, 2, 1, 2], [0, 0, 1, 0, 0], [0, 2, 0, 1, 0], [2, 0, 1, 1, 0], [0, 0, 2, 1, 0]],
        6: [[1, 2, 2, 2, 2, 1], [0, 0, 0, 0, 0, 0], [2, 1, 0, 1, 1, 1], [1, 3, 1, 0, 2, 0], [1, 1, 0, 0, 0, 20]]
    }
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        testing_process_PSTCs(program_version, n_list, weights_dict)
        testing_process_MSTCs(program_version, n_list, weights_dict, 'bits')
        testing_process_MSTCs(program_version, n_list, weights_dict, 'qubits')    