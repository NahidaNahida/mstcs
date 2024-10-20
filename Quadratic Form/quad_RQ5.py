from qiskit.circuit import QuantumRegister, QuantumCircuit, ParameterVector
 
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
 
import numpy as np
import csv
import math
import time

import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_convertion import generate_numbers
from quad_specification import PSTC_specification, MSTC_specification
from test_oracle import OPO_UTest
from circuit_execution import circuit_execution
from preparation_circuits import *
from repeat_until_success import *

from quad import QuadraticForm
from quad_defect1 import QuadraticForm_defect1
from quad_defect2 import QuadraticForm_defect2
from quad_defect3 import QuadraticForm_defect3
from quad_defect4 import QuadraticForm_defect4
from quad_defect5 import QuadraticForm_defect5

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
        
def testing_process_MSTCs_1MS(program_version, matA_dict, vecB_dict, c_list, 
                              inputs_list, mixed_pre_mode, shots_list, num_out=2, repeats=20):
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

    program_name = 'QuadraticForm'
    recorded_result = []      
    
    for shots in shots_list:
        n, m, angle_list, pure_states_distribution = inputs_list[0], inputs_list[1], inputs_list[2], inputs_list[3] 
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        A_list, b_list = matA_dict[n], vecB_dict[n]
        total_failures = 0
        start_time = time.time()
        num_classical_inputs = len(c_list) * len(A_list) * len(b_list)
        for _ in range(repeats):
            test_cases = 0
            for c in c_list:
                for A in A_list:
                    for b in b_list:
                        test_cases += 1
                        qc = QuantumCircuit(m + n + num_out, num_out)

                        # prepare the control state
                        con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                        if con_pre_mode == 'sep':
                            qc_con = separable_control_state_preparation(angle_list)
                        elif con_pre_mode == 'ent':
                            qc_con = entangled_control_state_preparation(angle_list)
                        
                        qc.append(qc_con, qc.qubits[:m])

                        # process control and target states
                        if mixed_pre_mode == 'bits':
                            qc = bit_controlled_preparation_1MS(n, m, qc)
                        elif mixed_pre_mode == 'qubits':
                            qc = qubit_controlled_preparation_1MS(n, m, qc) 
                            
                        # append the tested quantum subroutine (quantum program) 
                        func = version_selection(program_name, program_version)
                        qc_test = func(num_result_qubits=num_out, quadratic=A, linear=b, offset=c)
                        qc.append(qc_test, qc.qubits[m:])
                        qc.measure(qc.qubits[m + n:],qc.clbits[:])
                        
                        # execute the program and derive the outputs
                        dict_counts = circuit_execution(qc, shots)

                        # obtain the samples (measurement results) of the tested program
                        test_samps = []
                        for (key, value) in dict_counts.items():
                            test_samps += [key] * value
                        
                        # generate the samples that follow the expected probability distribution
                        exp_probs = MSTC_specification(covered_numbers, n, A, b, c, num_out, pure_states_distribution)
                        exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                        # derive the test result by nonparametric hypothesis test
                        test_result = OPO_UTest(exp_samps, test_samps)
                            
                        if test_result == 'fail':
                            total_failures += 1
                                
        dura_time = time.time() - start_time                           
        recorded_result.append([shots,
                                dura_time / num_classical_inputs / repeats, 
                                total_failures / test_cases / repeats])
        
    file_name = "RQ5_" + program_name + '_' + program_version + '_' + "MSTC(1MS)" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['shots', 'ave_time', 'faults']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs(1MS) done!')


def testing_process_MSTCs_2MS(program_version, matA_dict, vecB_dict, c_list, 
                              inputs_list, mixed_pre_mode, shots_list, num_out=2, repeats=20):
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

    program_name = 'QuadraticForm'
    recorded_result = []      
    MSB_val_list = [0, 1]

    for shots in shots_list:
        n, m, angle_lists, pure_states_distributions = inputs_list[0], inputs_list[1], inputs_list[2], inputs_list[3]
        # cover all the classical states            
        covered_numbers = list(range(2 ** n))
        A_list, b_list = matA_dict[n], vecB_dict[n]
        total_failures = 0
        start_time = time.time()
        num_classical_inputs = len(c_list) * len(A_list) * len(b_list)
        for _ in range(repeats):
            test_cases = 0
            for c in c_list:
                for A in A_list:
                    for b in b_list:
                        for MSB_val in MSB_val_list:
                            test_cases += 1
                            angle_list = angle_lists[MSB_val]
                            pure_states_distribution = pure_states_distributions[MSB_val]

                            qc = QuantumCircuit(m + n +  num_out, num_out)
                            
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
                            qc_test = func(num_result_qubits=num_out, quadratic=A, linear=b, offset=c)
                            qc.append(qc_test, qc.qubits[m:])
                            qc.measure(qc.qubits[m + n:],qc.clbits[:])
                            
                            # execute the program and derive the outputs
                            dict_counts = circuit_execution(qc, shots)

                            # obtain the samples (measurement results) of the tested program
                            test_samps = []
                            for (key, value) in dict_counts.items():
                                test_samps += [key] * value
                            
                            # generate the samples that follow the expected probability distribution
                            exp_probs = MSTC_specification(covered_numbers, n, A, b, c, num_out, pure_states_distribution)
                            exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                            # derive the test result by nonparametric hypothesis test
                            test_result = OPO_UTest(exp_samps, test_samps)
                                
                            if test_result == 'fail':
                                total_failures += 1

        dura_time = time.time() - start_time                            
        recorded_result.append([shots,
                                dura_time / num_classical_inputs / repeats, 
                                total_failures / test_cases / repeats])                            
    file_name = "RQ5_" + program_name + '_' + program_version + '_' + "MSTC(2MS)" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['shots', 'ave_time', 'faults']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('MSTCs(2MS) done!')

def testing_process_PSTCs(program_version, n, matA_dict, vecB_dict, c_list, shots_list, num_out=2, repeats=20):
    program_name = 'QuadraticForm'
    candidate_initial_states = [0, 1]
    
    recorded_result = []      
    for shots in shots_list:            
        total_failures = 0
        initial_states = generate_numbers(n, len(candidate_initial_states))
        A_list, b_list = matA_dict[n], vecB_dict[n]
        start_time = time.time()
        num_classical_inputs = len(c_list) * len(A_list) * len(b_list)
        for _ in range(repeats):
            test_cases = 0
            for c in c_list:
                for A in A_list:
                    for b in b_list:
                        for initial_state in initial_states:
                            test_cases += 1
                            number = int(''.join(map(str, initial_state)), 2)
                            qc = QuantumCircuit(n + num_out, num_out)
                            initial_state = initial_state[::-1]
                            
                            for index, val in enumerate(initial_state):
                                if candidate_initial_states[val] == 1:
                                    qc.x(index)
                                        
                            # append the tested quantum subroutine (quantum program)
                            func = version_selection(program_name, program_version)
                            qc_test = func(num_result_qubits=num_out, quadratic=A, linear=b, offset=c)
                            qc.append(qc_test, qc.qubits)
                            qc.measure(qc.qubits[n:],qc.clbits[:])


                            # execute the program and derive the outputs
                            dict_counts = circuit_execution(qc, shots)
                        
                            # obtain the samples (measurement results) of the tested program
                            test_samps = []
                            for (key, value) in dict_counts.items():
                                test_samps += [key] * value
                        
                            # generate the samples that follow the expected probability distribution
                            exp_probs = PSTC_specification(initial_state, A, b, c, num_out)
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
    file_name = "RQ5_" + program_name + '_' + program_version + "_PSTC" + ".csv"
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        header = ['shots', 'ave_time', '# faults']
        writer.writerow(header)
        for data in recorded_result:
            writer.writerow(data)
    print('PSTCs done!')
 
if __name__ == '__main__':
    # the setting to generate classical inputs
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
            [[0, 0, 0, 1, 0], [0, -1, -1, 0, 2], [2, 1, 0, 1, -1], [1, 1, -1, -1, 0], [0, 0, 0, 1, 0]]]
    }
    vecB_dict = {
        2: [[0, 0], [0, 1], [-1, 2], [1, 1], [2, 2]],
        3: [[0, 0, 1], [0, 1, -1], [1, -1, 2], [1, -1, 2], [1, 1, 0]], 
        4: [[1, -2, 0, 1], [0, 1, 1, 0], [1, 0, 0, 1], [1, 1, 2, 0], [-1, 1, 2, 1]],  
        5: [[1, 1, 1, 1, 1], [-1, 2, 0, 1, 0],  [0, 0, 1, 2, 1], [1, 1, -1, -1, 0], [0, 0, 0, 1, 0]],
    }
    C_list = np.arange(-2, 3, 1)

    # remember the length of pure_state_distribution should be 2 ** n
    inputs_2MS = [5, 4, 
                  [[math.pi/2] * 4, [math.pi/2] * 4], 
                  [[1 / (2 ** 4)] * (2 ** 4) + [0] * (2 ** 4), 
                   [0] * (2 ** 4) + [1 / (2 ** 4)] * (2 ** 4)]]
    inputs_1MS = [5, 5, 
                  [math.pi/2] * 5, 
                  [1 / (2 ** 5)] * (2 ** 5)]

    # the test processes
    shots_list = range(8, 1025, 8)
    for program_version in ["v1"]:
        print(program_version)
        testing_process_MSTCs_2MS(program_version, matA_dict, vecB_dict, C_list, inputs_2MS, 'qubits', shots_list)
        testing_process_MSTCs_1MS(program_version, matA_dict, vecB_dict, C_list, inputs_1MS, 'qubits', shots_list)
        testing_process_PSTCs(program_version, 5, matA_dict, vecB_dict, C_list, shots_list)
    print('done!')