from qiskit import QuantumCircuit

import numpy as np
import csv
import math
import time
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from amplitude_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution
from preparation_circuits import *
from repeat_until_success import *

from amplitude_defect1 import LinearAmplitudeFunction_defect1
from amplitude_defect2 import LinearAmplitudeFunction_defect2
from amplitude_defect3 import LinearAmplitudeFunction_defect3
from amplitude_defect4 import LinearAmplitudeFunction_defect4
from amplitude_defect5 import LinearAmplitudeFunction_defect5
from amplitude_defect6 import LinearAmplitudeFunction_defect6

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
        
def testing_process_MSTCs_1MS(program_version, 
                              slop_list, 
                              offset_list,
                              domain_list,
                              image_list, 
                              inputs_list, 
                              mixed_pre_mode, 
                              shots_list, 
                              repeats=20):
    """
        Cover a group of classical inputs with only one mixed state. For example, n = 2,
        rho = 1/4 * (|0><0| + |1><1| + |2><2| + |3><3|)
        
        Input variables:
            + inputs_list  [list]: each element stores the following data, 
                                   inputs = [n, m, angle_list, input_probs, input_name]
                                   n -- number of target qubits
                                   m -- number of control qubits
                                   angle_list -- the list of angle parameters for state preparation
                                   input_probs -- the probability distribution of input pure states
                                   input_name -- the name of the test suite
            + mixed_pre_mode [str]: the mode for preparing mixed states, which is either 'ent' or 'sep'

        Output variable:
            + recorded_result [list]: each element gives [input_name, test_cases, ave_time]  
    """

    program_name = 'LinearAmplitudeFunction'
    recorded_result = []      

    for shots in shots_list:
        n, m, angle_list, pure_states_distribution = inputs_list[0], inputs_list[1], inputs_list[2], inputs_list[3]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        num_classical_inputs = len(slop_list) * len(offset_list) * len(domain_list) * len(image_list)
        total_failures = 0
        start_time = time.time()
        for _ in range(repeats):
            test_cases = 0
            for slop in slop_list:
                for offset in offset_list:
                    for domain in domain_list:
                        for image in image_list:
                            test_cases += 1
                            qc = QuantumCircuit(n + m + 1, 1)

                            con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                            if con_pre_mode == 'sep':
                                qc_con = separable_control_state_preparation(angle_list)
                            elif con_pre_mode == 'ent':
                                qc_con = entangled_control_state_preparation(angle_list)
                            
                            qc.append(qc_con, qc.qubits[:m])

                            if mixed_pre_mode == 'bits':
                                qc = bit_controlled_preparation_1MS(n, m, qc)
                            elif mixed_pre_mode == 'qubits':
                                qc = qubit_controlled_preparation_1MS(n, m, qc) 
                                
                            # append the tested quantum subroutine (quantum program) 
                            func = version_selection(program_name, program_version)
                            qc_test = func(n, slop, offset, domain=domain, image=image)
                            qc.append(qc_test, qc.qubits[m:])
                            qc.measure(qc.qubits[-1],qc.clbits[-1])
                            
                            # execute the program and derive the outputs
                            dict_counts = circuit_execution(qc, shots)

                            # obtain the samples (measurement results) of the tested program
                            test_samps = []
                            for (key, value) in dict_counts.items():
                                test_samps += [key] * value
                            
                            # generate the samples that follow the expected probability distribution
                            exp_probs = MSTC_specification(n, covered_numbers, pure_states_distribution, slop, offset, domain, image)
                            exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                            # derive the test result by nonparametric hypothesis test
                            test_result = OPO_UTest(exp_samps, test_samps)
                            if test_result == 'fail':
                                total_failures += 1

        dura_time = time.time() - start_time                           
        recorded_result.append([shots,
                                dura_time / num_classical_inputs / repeats, 
                                total_failures / test_cases / repeats])

    # save the data
    current_dir = os.getcwd()
    saving_path = os.path.join(current_dir, 
                               "data", 
                               "raw_data_for_empirical_results",
                               "RQ5",
                               program_name)
    file_name = "RQ5_" + program_name + '_' + program_version + '_' + "MSTC(1MS)" + ".csv"
    with open(os.path.join(saving_path, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['shots', 'ave_time', 'faults']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs(1MS) done!')

def testing_process_MSTCs_2MS(program_version, 
                              slop_list, 
                              offset_list,
                              domain_list,
                              image_list, 
                              inputs_list, 
                              mixed_pre_mode, 
                              shots_list, 
                              repeats=20):
    """
        Cover a group of classical inputs with two mixed state. Given n,
        rho1 = 1/(2^(n-1)) * (|0><0| + ... + |2^{n-1}-1><2^{n-1}-1|) 
        rho2 = 1/(2^(n-1)) * (|2^{n-1}><2^{n-1}| + ... + |2^{n}-1><2^{n}-1|) 
        
        For example, n = 2,
        rho1 = 1/2 * (|0><0| + |1><1|) 
        rho2 = 1/2 * (|2><2| + |3><3|)
        
        Input variables:
            + inputs_list  [list]: each element stores the following data, 
                                   inputs = [n, m, angle_list, input_probs, input_name]
                                   n -- number of target qubits
                                   m -- number of control qubits
                                   angle_lists -- 2 lists of angle parameters for state preparation
                                   pure_states_distributionss -- 2 probability distributions of input pure states
                                   input_name -- the name of the test suite
            + mixed_pre_mode [str]: the mode for preparing mixed states, which is either 'ent' or 'sep'

        Output variable:
            + recorded_result [list]: each element gives [input_name, test_cases, ave_time]  
    """  

    program_name = 'LinearAmplitudeFunction'
    recorded_result = []
      
    MSB_val_list = [0, 1]
    for shots in shots_list:
        n, m, angle_lists, pure_states_distributions = inputs_list[0], inputs_list[1], inputs_list[2], inputs_list[3]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        total_failures = 0
        num_classical_inputs = len(slop_list) * len(offset_list) * len(domain_list) * len(image_list)
        start_time = time.time()
        for _ in range(repeats):
            test_cases = 0
            for slop in slop_list:
                for offset in offset_list:
                    for domain in domain_list:
                        for image in image_list:
                            for MSB_val in MSB_val_list:
                                test_cases += 1
                                angle_list = angle_lists[MSB_val]
                                pure_states_distribution = pure_states_distributions[MSB_val]

                                qc = QuantumCircuit(n + m + 1, 1)
                                
                                # prepare the most significant qubit
                                if MSB_val == 1:
                                    qc.x(m + n - 1)

                                con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                                if con_pre_mode == 'sep':
                                    qc_con = separable_control_state_preparation(angle_list)
                                elif con_pre_mode == 'ent':
                                    qc_con = entangled_control_state_preparation(angle_list)
                                
                                qc.append(qc_con, qc.qubits[:m])

                                if mixed_pre_mode == 'bits':
                                    qc = bit_controlled_preparation_2MS(n, m, qc)
                                elif mixed_pre_mode == 'qubits':
                                    qc = qubit_controlled_preparation_2MS(n, m, qc) 
                                    
                                # append the tested quantum subroutine (quantum program) 
                                func = version_selection(program_name, program_version)
                                qc_test = func(n, slop, offset, domain=domain, image=image)
                                qc.append(qc_test, qc.qubits[m:])
                                qc.measure(qc.qubits[-1],qc.clbits[-1])
                                
                                # execute the program and derive the outputs
                                dict_counts = circuit_execution(qc, shots)

                                # obtain the samples (measurement results) of the tested program
                                test_samps = []
                                for (key, value) in dict_counts.items():
                                    test_samps += [key] * value
                                
                                # generate the samples that follow the expected probability distribution
                                exp_probs = MSTC_specification(n, covered_numbers, pure_states_distribution, slop, offset, domain, image)
                                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                                # derive the test result by nonparametric hypothesis test
                                test_result = OPO_UTest(exp_samps, test_samps)

                                if test_result == 'fail':
                                    total_failures += 1

        dura_time = time.time() - start_time                           
        recorded_result.append([shots,
                                dura_time / num_classical_inputs / repeats, 
                                total_failures / test_cases / repeats])

    # save the data
    current_dir = os.getcwd()
    saving_path = os.path.join(current_dir, 
                               "data", 
                               "raw_data_for_empirical_results",
                               "RQ5",
                               program_name)    
    file_name = "RQ5_" + program_name + '_' + program_version + '_' + "MSTC(2MS)" + ".csv"
    with open(os.path.join(saving_path, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['shots', 'ave_time', 'faults']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs(2MS) done!')

def testing_process_PSTCs(program_version, 
                          n, 
                          slop_list, 
                          offset_list,  
                          domain_list,
                          image_list,
                          shots_list, 
                          repeats=20):
    program_name = 'LinearAmplitudeFunction'
    candidate_initial_states = [0, 1]
    num_classical_inputs = len(slop_list) * len(offset_list) * len(domain_list) * len(image_list)
    
    recorded_result = []  
    for shots in shots_list:  
        total_failures = 0
        initial_states = generate_numbers(n, len(candidate_initial_states))
        
        start_time = time.time()
        for _ in range(repeats):          
            test_cases = 0
            for slop in slop_list:
                for offset in offset_list:
                    for domain in domain_list:
                        for image in image_list:
                            for initial_state in initial_states:
                                test_cases += 1

                                number = int(''.join(map(str, initial_state)), 2)
                                qc = QuantumCircuit(n + 1, 1)
                                initial_state = initial_state[::-1]
                                for index, val in enumerate(initial_state):
                                    if candidate_initial_states[val] == 1:
                                        qc.x(index)
                                                
                                # append the tested quantum subroutine (quantum program)
                                func = version_selection(program_name, program_version)
                                qc_test = func(n, slop, offset, domain=domain, image=image)
                                qc.append(qc_test, qc.qubits)
                                qc.measure(qc.qubits[-1], qc.clbits[-1])
                                
                                # execute the program and derive the outputs
                                dict_counts = circuit_execution(qc, shots)
                            
                                # obtain the samples (measurement results) of the tested program
                                test_samps = []
                                for (key, value) in dict_counts.items():
                                    test_samps += [key] * value
                                
                                # generate the samples that follow the expected probability distribution
                                exp_probs = PSTC_specification(n, number, slop, offset, domain, image)
                                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))                    

                                # derive the test result by nonparametric hypothesis test
                                test_result = OPO_UTest(exp_samps, test_samps)

                                if test_result == 'fail':
                                    total_failures += 1   

        dura_time = time.time() - start_time                            
        recorded_result.append([shots,
                                dura_time / num_classical_inputs / repeats, 
                                total_failures / test_cases / repeats])
     
    # save the data
    current_dir = os.getcwd()
    saving_path = os.path.join(current_dir, 
                               "data", 
                               "raw_data_for_empirical_results",
                               "RQ5",
                               program_name)
    file_name = "RQ5_" + program_name + '_' + program_version + "_PSTC" + ".csv"
    with open(os.path.join(saving_path, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['shots', 'ave_time', 'faults']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('PSTCs done!')

if __name__ == '__main__':
    n = 5       # the number of input qubits
    program_versions = ['v1']
    # the setting to generate classical inputs
    slop_list = [0, math.pi / 4, math.pi / 2]
    offset_list = [0, math.pi / 4, math.pi / 2]
    domain_list = [[-1, 1], [-1, 0], [0, 1]]
    image_list = [[-1, 1], [-1, 0], [0, 1]]
    # remember the length of pure_state_distribution should be 2 ** n
    inputs_2MS = [n, n - 1, 
                  [[math.pi/2] * (n - 1), [math.pi/2] * (n - 1)], 
                  [[1 / (2 ** (n - 1))] * (2 ** (n - 1)) + [0] * (2 ** (n - 1)), 
                   [0] * (2 ** (n - 1)) + [1 / (2 ** (n - 1))] * (2 ** (n - 1))]]
    inputs_1MS = [n, n, 
                  [math.pi/2] * n, 
                  [1 / (2 ** n)] * (2 ** n)]
    
    # the test processes
    shots_list = range(8, 1025, 8)
    for program_version in program_versions:
        print(program_version)
        testing_process_MSTCs_2MS(program_version, 
                                  slop_list, 
                                  offset_list, 
                                  domain_list,
                                  image_list,
                                  inputs_2MS, 
                                  'qubits', 
                                  shots_list)
        testing_process_MSTCs_1MS(program_version, 
                                  slop_list, 
                                  offset_list, 
                                  domain_list,
                                  image_list,
                                  inputs_1MS, 
                                  'qubits', 
                                  shots_list)
        testing_process_PSTCs(program_version, 
                              n, 
                              slop_list, 
                              offset_list, 
                              domain_list,
                              image_list,
                              shots_list)
    print('done!')