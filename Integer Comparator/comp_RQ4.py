from qiskit.circuit import QuantumCircuit
import math
import numpy as np
import csv
import time 

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from comp_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution
from preparation_circuits import *
from repeat_until_success import *

from comp import IntegerComparator
from comp_defect1 import IntegerComparator_defect1
from comp_defect2 import IntegerComparator_defect2
from comp_defect3 import IntegerComparator_defect3
from comp_defect4 import IntegerComparator_defect4
from comp_defect5 import IntegerComparator_defect5

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
        
def testing_process_MSTCs_1MS(program_version, L_list, sign_list, inputs_list, 
                              mixed_pre_mode, repeats=20):
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

    program_name = 'IntegerComparator'
    default_shots = 1024
    recorded_result = []      
    
    for inputs in inputs_list:
        n, m, angle_list, pure_states_distribution, input_name = inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for L in L_list:
                for sign in sign_list:
                    test_cases += 1
                    qc = QuantumCircuit(2 * n + m, n)

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
                    qc_test = func(n, L, geq=sign)
                    qc.append(qc_test, qc.qubits[m:])
                    qc.measure(qc.qubits[m + n:],qc.clbits[:])
                    
                    # execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, default_shots)

                    # obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        test_samps += [key] * value
                    
                    # generate the samples that follow the expected probability distribution
                    exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, L, sign)
                    exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                    # derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                            
                    if test_result == 'fail':
                        total_failures += 1
                            
        recorded_result.append([input_name, test_cases, total_failures / test_cases / repeats])
    return recorded_result

def testing_process_MSTCs_2MS(program_version, L_list, sign_list, inputs_list, 
                              mixed_pre_mode, repeats=20):
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

    program_name = 'IntegerComparator'
    default_shots = 1024
    recorded_result = []      
    MSB_val_list = [0, 1]
    for inputs in inputs_list:
        n, m, angle_lists, pure_states_distributions, input_name = inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for L in L_list:
                for sign in sign_list:
                    for MSB_val in MSB_val_list:
                        test_cases += 1
                        angle_list = angle_lists[MSB_val]
                        pure_states_distribution = pure_states_distributions[MSB_val]

                        qc = QuantumCircuit(2 * n + m, n)
                        
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
                        qc_test = func(n, L, geq=sign)
                        qc.append(qc_test, qc.qubits[m:])
                        qc.measure(qc.qubits[m + n:],qc.clbits[:])
                        
                        # execute the program and derive the outputs
                        dict_counts = circuit_execution(qc, default_shots)

                        # obtain the samples (measurement results) of the tested program
                        test_samps = []
                        for (key, value) in dict_counts.items():
                            test_samps += [key] * value
                        
                        # generate the samples that follow the expected probability distribution
                        exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, L, sign)
                        exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                        # derive the test result by nonparametric hypothesis test
                        test_result = OPO_UTest(exp_samps, test_samps)

                        if test_result == 'fail':
                            total_failures += 1
                            
        recorded_result.append([input_name, test_cases, total_failures / test_cases / repeats])
    return recorded_result

 
if __name__ == '__main__':
    # the setting to generate classical inputs
    L_list = np.arange(-5, 5.1, 1)
    sign_list =  [True, False]

    # remember the length of pure_state_distribution should be 2 ** n
    inputs_2MS = [
        [2, 1, 
         [[math.pi/8], [math.pi/8]], 
         [[0.9619397662556434, 0.03806023374435662, 0, 0], 
          [0, 0, 0.9619397662556434, 0.03806023374435662]], "T0"],
        [2, 1, 
         [[math.pi/4], [math.pi/4]], 
         [[0.8535533905932737, 0.14644660940672624, 0, 0], 
          [0, 0, 0.8535533905932737, 0.14644660940672624]], "T1"],
        [2, 1, 
         [[3 * math.pi/8], [3 * math.pi/8]], 
         [[0.6913417161825449, 0.3086582838174551, 0, 0], 
          [0, 0, 0.6913417161825449, 0.3086582838174551]], "T2"],
        [2, 1, 
         [[math.pi/2], [math.pi/2]], 
         [[0.5, 0.5, 0, 0], 
          [0, 0, 0.5, 0.5]], "T3"],
    ]

    inputs_1MS = [
        [2, 2, 
         [math.pi/8, math.pi/2], 
         [0.48096988312782174, 0.01903011687217831, 0.48096988312782174, 0.01903011687217831], "T4"],
        [2, 2, 
         [2*math.pi/8, math.pi/2], 
         [0.4267766952966369, 0.07322330470336312, 0.4267766952966369, 0.07322330470336312], "T5"],
        [2, 2, 
         [3*math.pi/8, math.pi/2], 
         [0.3456708580912725, 0.15432914190872754, 0.3456708580912725, 0.15432914190872754], "T6"],
        [2, 2, 
         [4*math.pi/8, math.pi/2], 
         [0.25, 0.25, 0.25, 0.25], "T7"]
    ]

    # the test processes
    for program_version in ["v1", "v2", "v3", "v4", "v5"]:
        print(program_version)
        recorded_result = []
        recorded_result = recorded_result + testing_process_MSTCs_2MS(program_version, L_list, sign_list, inputs_2MS, 'qubits')
        recorded_result = recorded_result + testing_process_MSTCs_1MS(program_version, L_list, sign_list, inputs_1MS, 'qubits')

        # save the data
        program_name = 'IntegerComparator'
        file_name = "RQ4_" + program_name + "_" + program_version + ".csv"
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ['test_suite', 'mixed_pre_mode', '# test_cases', '# faults']
            writer.writerow(header)
            for data in recorded_result:
                writer.writerow(data)
    print('done!')