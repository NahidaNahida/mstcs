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
from preparation_circuits import *
from repeat_until_success import *

from adder import WeightedAdder
from adder_defect1 import WeightedAdder_defect1
from adder_defect2 import WeightedAdder_defect2
from adder_defect3 import WeightedAdder_defect3
from adder_defect4 import WeightedAdder_defect4
from adder_defect5 import WeightedAdder_defect5

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
        
def testing_process_MSTCs_1MS(program_version, weights_dict, inputs_list, 
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

    program_name = 'WeightedAdder'
    default_shots = 1024
    recorded_result = []      
    
    for inputs in inputs_list:
        n, m, angle_list, pure_states_distribution, input_name = inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        weights_list = weights_dict[n]
        num_classical_inputs = len(weights_list)
        start_time = time.time()
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:              # calculate the number of output qubits s
                test_cases += 1
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # append the tested quantum subroutine (quantum program) 
                func = version_selection(program_name, program_version)
                qc_test = func(n, weight)

                qc = QuantumCircuit(m + qc_test.num_qubits, s)
                
                # prepare the control state    
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
                qc.append(qc_test, qc.qubits[m:])
                qc.measure(qc.qubits[m + n: m + n + s],qc.clbits[:])
                
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
        recorded_result.append([input_name, mixed_pre_mode ,test_cases, 
                                dura_time / num_classical_inputs / repeats])
    return recorded_result

def testing_process_MSTCs_2MS(program_version, weights_dict, inputs_list, 
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

    program_name = 'WeightedAdder'
    default_shots = 1024
    recorded_result = []      
    MSB_val_list = [0, 1]
    for inputs in inputs_list:
        n, m, angle_lists, pure_states_distributions, input_name = inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        weights_list = weights_dict[n]
        num_classical_inputs = len(weights_list)
        start_time = time.time()
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))
                # append the tested quantum subroutine (quantum program) 
                for MSB_val in MSB_val_list:
                    test_cases += 1
                    angle_list = angle_lists[MSB_val]
                    pure_states_distribution = pure_states_distributions[MSB_val]

                    # append the tested quantum subroutine (quantum program) 
                    func = version_selection(program_name, program_version)
                    qc_test = func(n, weight)

                    qc = QuantumCircuit(m + qc_test.num_qubits, s)

                    # prepare the control qubits
                    con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                    if con_pre_mode == 'sep':
                        qc_con = separable_control_state_preparation(angle_list)
                    elif con_pre_mode == 'ent':
                        qc_con = entangled_control_state_preparation(angle_list)
                    qc.append(qc_con, qc.qubits[:m])

                    # prepare the most significant qubit
                    if MSB_val == 1:
                        qc.x(m + n - 1)

                    if mixed_pre_mode == 'bits':
                        qc = bit_controlled_preparation_2MS(n, m, qc)
                    elif mixed_pre_mode == 'qubits':
                        qc = qubit_controlled_preparation_2MS(n, m, qc) 
                        
                    # append the tested quantum subroutine (quantum program) 
                    qc.append(qc_test, qc.qubits[m:])
                    qc.measure(qc.qubits[m + n:m + n + s],qc.clbits[:])
                    
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
        recorded_result.append([input_name, mixed_pre_mode ,test_cases, 
                                dura_time / num_classical_inputs / repeats])
    return recorded_result

def testing_process_MSTCs_MPS(program_version, weights_dict, inputs_list, 
                              mixed_pre_mode, repeats=20):
    """
        Cover a group of classical inputs with one mixed state and one pure state. 
        The mixed state includes |0><0| ~ |2^n-2><2^n-2| and the pure states is |2^n-1><2^n-1|.
        Especially, this aims to check the repeat-until-success structure when N is not a power of m
        For example, n = 2,
        rho1 = 1/3 * (|0><0| + |1><1| + |2><2|), rho2 = |3><3|
        
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

    def pure_state_preparation(n, qc):
        qc.x(qc.qubits[:n])
        return qc  

    program_name = 'WeightedAdder'
    default_shots = 1024
    recorded_result = []      
    state_list = ['mixed', 'pure']

    for inputs in inputs_list:
        n, m, angle_list, pure_states_distribution, input_name = inputs[0], inputs[1], inputs[2], inputs[3], inputs[4]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        weights_list = weights_dict[n]
        num_classical_inputs = len(weights_list)
        start_time = time.time()
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))
                # append the tested quantum subroutine (quantum program) 
                func = version_selection(program_name, program_version)
                qc_test = func(n, weight)
                for temp_state in state_list:
                    test_cases += 1
                    if temp_state == 'mixed':
                        qc = QuantumCircuit(m + qc_test.num_qubits, m + s)
                        # prepare the control state
                        con_pre_mode = 'sep' if n == len(angle_list) else 'ent'
                        if con_pre_mode == 'sep':
                            qc_con = separable_control_state_preparation(angle_list)
                        elif con_pre_mode == 'ent':
                            qc_con = entangled_control_state_preparation(angle_list)
                        qc.append(qc_con, qc.qubits[:m])
                        # connect the control and target qubits
                        if mixed_pre_mode == 'bits':
                            qc = bit_controlled_preparation_MPS(n, m, qc)
                        elif mixed_pre_mode == 'qubits':
                            qc = qubit_controlled_preparation_MPS(n, m, qc)
                    elif temp_state == 'pure':
                        qc = QuantumCircuit(qc_test.num_qubits, s)
                        qc = pure_state_preparation(n, qc)

                    # measurement and execute the program and derive the outputs
                    if temp_state == 'mixed':
                        qc.append(qc_test, qc.qubits[m:])
                        qc.measure(qc.qubits[n + m : n + m + s], qc.clbits[-s:])
                        # remove the unexpected value until the valid values meets
                        # the required number of samples  
                        invalid_con_list = [int('1' * m, 2)]
                        invalid_num_list = generate_invalid_numbers(qc.num_qubits, m, invalid_con_list)
                        dict_counts = repeat_until_success(qc, default_shots, invalid_num_list)
                    elif temp_state == 'pure':
                        qc.append(qc_test, qc.qubits[:])
                        qc.measure(qc.qubits[-s:], qc.clbits[:])
                        dict_counts = circuit_execution(qc, default_shots)

                    # obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        if temp_state == 'mixed':   # remove the output of control qubits (low m bits)
                            test_samps += [key >> m] * value
                        else:
                            test_samps += [key] * value
                    
                    # generate the samples that follow the expected probability distribution
                    if temp_state == "mixed":
                        exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, n, s, weight)
                        exp_samps = list(np.random.choice(range(2 ** (qc.num_clbits - m)), 
                                                        size=default_shots, 
                                                        p=exp_probs))
                    elif temp_state == "pure":
                        exp_probs = PSTC_specification(s, [1] * n, weight)
                        exp_samps = list(np.random.choice(range(2 ** (qc.num_clbits)), 
                                                        size=default_shots, 
                                                        p=exp_probs))               
                                        
                    # derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                            
        dura_time = time.time() - start_time
        recorded_result.append([input_name, mixed_pre_mode ,test_cases, 
                                dura_time / num_classical_inputs / repeats])
    return recorded_result

if __name__ == '__main__':
    # the setting to generate classical inputs
    weights_dict = {
        1: [[0], [1], [2]],
        2: [[0, 0], [0, 1], [1, 2], [1, 1], [2, 2]],
        3: [[0, 0, 0], [2, 0, 2], [1, 1, 0], [0, 2, 1], [1, 0, 2]],
        4: [[0, 1, 1, 1], [0, 0, 0, 0], [2, 2, 0, 0], [1, 1, 0, 0], [1, 2, 0, 1]],
        5: [[1, 0, 2, 1, 2], [0, 0, 1, 0, 0], [0, 2, 0, 1, 0], [2, 0, 1, 1, 0], [0, 0, 2, 1, 0]]
    }

    # remember the length of pure_state_distribution should be 2 ** n
    inputs_2MS = [
        [2, 1, [[math.pi/2], [math.pi/2]], [[1/2, 1/2, 0, 0], [0, 0, 1/2, 1/2]], "T0"],
        [2, 1, [[2*math.pi/3], [2*math.pi/3]], [[1/4, 3/4, 0, 0], [0, 0, 1/4, 3/4]], "T3"]
    ]

    inputs_MPS_sep = [[2, 2, [math.pi/2, math.pi/2], [1/3, 1/3, 1/3, 0], "T6 sep"]]
    inputs_MPS_ent = [[2, 2, [1.231, math.pi/2, 0], [1/3, 1/3, 1/3, 0], "T6 ent"]]

    inputs_1MS = [
        [2, 2, [math.pi/2, math.pi/2], [1/4, 1/4, 1/4, 1/4], "T1"],
        [2, 3, [math.pi/2, math.pi/2, math.pi/2], [1/4, 1/4, 1/4, 1/4], "T2"],
        [2, 2, [1.911, math.pi/2, math.pi/2], [1/6, 1/3, 1/6, 1/3], "T4"],
        [2, 3, [1.911, math.pi/2, math.pi/2, math.pi/2, math.pi/2, math.pi/2, math.pi/2], [1/6, 1/3, 1/6, 1/3], "T5"]
    ]

    # the test processes
    for program_version in ["v1", "v2", "v3", "v4", "v5"]:
        print(program_version)
        recorded_result = []
        recorded_result = recorded_result + testing_process_MSTCs_2MS(program_version, weights_dict, inputs_2MS, 'bits')
        recorded_result = recorded_result + testing_process_MSTCs_2MS(program_version, weights_dict, inputs_2MS, 'qubits')
        recorded_result = recorded_result + testing_process_MSTCs_1MS(program_version, weights_dict, inputs_1MS, 'bits')
        recorded_result = recorded_result + testing_process_MSTCs_1MS(program_version, weights_dict, inputs_1MS, 'qubits')
        recorded_result = recorded_result + testing_process_MSTCs_MPS(program_version, weights_dict, inputs_MPS_sep, 'bits')
        recorded_result = recorded_result + testing_process_MSTCs_MPS(program_version, weights_dict, inputs_MPS_sep, 'qubits')
        recorded_result = recorded_result + testing_process_MSTCs_MPS(program_version, weights_dict, inputs_MPS_ent, 'bits')
        recorded_result = recorded_result + testing_process_MSTCs_MPS(program_version, weights_dict, inputs_MPS_ent, 'qubits')
        # save the data
        program_name = 'WeightedAdder'
        file_name = "RQ2_" + program_name + "_" + program_version + ".csv"
        with open(file_name, mode='w', newline='') as file:
            writer = csv.writer(file)
            header = ['test_suite', 'mixed_pre_mode', '# test_cases', 'ave_time']
            writer.writerow(header)
            for data in recorded_result:
                writer.writerow(data)
    print('done!')