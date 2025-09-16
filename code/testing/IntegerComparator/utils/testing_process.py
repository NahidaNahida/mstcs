import numpy as np
import os
import math, time
from typing import Literal
from itertools import product

from qiskit import QuantumCircuit

from ....utils import (
    generate_numbers,
    covered_pure_states,
    outputdict2samps, 
    import_versions,
    get_target_version, 
    circuit_execution, 
    OPO_UTest,
    repeat_until_success,
    generate_invalid_numbers,
    bit_controlled_preparation_1MS,
    qubit_controlled_preparation_1MS,
    bit_controlled_preparation_2MS,
    qubit_controlled_preparation_2MS,
    bit_controlled_preparation_MPS,
    qubit_controlled_preparation_MPS,
    separable_control_state_preparation,
    entangled_control_state_preparation,
)

from ....config import pure_state_distribution, control_qubit_numbers
 

from . import PSTC_specification, MSTC_specification
from ..config import program_name, candidate_initial_states 

# =================================================================
# Get the file directory
current_dir = os.path.dirname(__file__)
version_dir = os.path.join(os.path.dirname(current_dir), "programs")
config_dir = os.path.join(os.path.dirname(current_dir), "config")

# Import the program versions under the same directory
version_dict = import_versions(program_name, version_dir)

def testing_process_PSTCs(
    program_version: str, 
    n_list: list[int], 
    L_list: list[int], 
    sign_list: list[bool], 
    shots: int,
    repeats: int
) -> list[dict]:
    recorded_result = []      
    for n in n_list:            
        initial_states_list = generate_numbers(n, len(candidate_initial_states))
        num_classical_inputs = len(L_list) * len(sign_list)
        start_time = time.time()
        pre_time = 0                        # Record time for state preparation
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for L, sign in product(L_list, sign_list):
                for initial_states in initial_states_list:
                    test_cases += 1
                    number = int(''.join(map(str, initial_states)), 2)
                    qc = QuantumCircuit(2 * n, n)

                    pre_start_time = time.time()
                    initial_states = initial_states[::-1]
                    for index, val in enumerate(initial_states):
                        if candidate_initial_states[val] == 1:
                            qc.x(index)
                    pre_end_time = time.time()
                    pre_time += pre_end_time - pre_start_time

                    # Append the tested quantum subroutine (quantum program) 
                    func = get_target_version(version_dict, program_version)
                    qc_test = func(n, L, geq=sign)

                    qc.append(qc_test, qc.qubits)
                    qc.measure(qc.qubits[n:],qc.clbits[:])
                    
                    # Execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = outputdict2samps(dict_counts)
                    
                    # Generate the samples that follow the expected probability distribution
                    exp_probs = PSTC_specification(n, number, L, sign)
                    exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                    # Derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                    
                    if test_result == 'fail':
                        total_failures += 1

        dura_time = time.time() - start_time

        recorded_result.append({
            "num_qubits": n,
            "num_shots": shots,
            "num_test_cases": test_cases,
            "ave_faults": total_failures / test_cases / repeats,
            "ave_exe_time": dura_time / num_classical_inputs / repeats, 
            "ave_pre_time": pre_time / num_classical_inputs / repeats
        })
  
    return recorded_result

def testing_process_MSTCs(
    program_version: str, 
    n_list: list[int], 
    L_list: list[int], 
    sign_list: list[bool], 
    pre_mode: Literal["bits", "qubits"],
    shots: int,
    repeats: int,
    pure_state_dist: Literal["uniform"] = "uniform",
    num_controls: Literal["equal"] = "equal"
) -> list[dict]:
    
    recorded_result = []      
    for n in n_list:  
        # define the uniform distribution for the ensemble
        pure_states_distribution = pure_state_distribution(n, pure_state_dist)

        # Cover all the classical states            
        covered_numbers = covered_pure_states(pure_states_distribution)
        
        num_classical_inputs = len(L_list) * len(sign_list)
        start_time = time.time()
        total_failures = 0
        pre_time = 0                                 # Record time for state preparation
        m = control_qubit_numbers(n, num_controls)   # Determine the number of the control qubits.
        for _ in range(repeats):
            test_cases = 0
            for L, sign in product(L_list, sign_list):
                test_cases += 1
                qc = QuantumCircuit(2 * n + m, n)

                pre_start_time = time.time()
                
                # Prepare the control state
                qc.h(qc.qubits[:m])
                
                # Mixed state preparation
                if pre_mode == 'bits':
                    qc = bit_controlled_preparation_1MS(n, m, qc)
                elif pre_mode == 'qubits':
                    qc = qubit_controlled_preparation_1MS(n, m, qc)
                pre_end_time = time.time()
                pre_time += pre_end_time - pre_start_time                    

                # Append the tested quantum subroutine (quantum program) 
                func = get_target_version(version_dict, program_version)
                qc_test = func(n, L, geq=sign)

                qc.append(qc_test, qc.qubits[m:])
                qc.measure(qc.qubits[n + m:],qc.clbits[:])
                
                # Execute the program and derive the outputs
                dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = outputdict2samps(dict_counts)
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, L, sign)
                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                # Derive the test result by nonparametric hypothesis test
                test_result = OPO_UTest(exp_samps, test_samps)

                if test_result == 'fail':
                    total_failures += 1

        dura_time = time.time() - start_time
        recorded_result.append({
            "num_qubits": n,
            "num_shots": shots,
            "num_test_cases": test_cases,
            "ave_faults": total_failures / test_cases / repeats,
            "ave_exe_time": dura_time / num_classical_inputs / repeats, 
            "ave_pre_time": pre_time / num_classical_inputs / repeats
        })
 
    return recorded_result

def testing_process_MSTCs_1MS(
    program_version: str, 
    L_list: list[int], 
    sign_list: list[bool], 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    shots: int, 
    repeats: int
) -> list[dict]:
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

    recorded_result = []      
    for inputs in inputs_list:
        # Assign values to variables
        n, m = inputs["num_target"], inputs["num_control"]
        angle_list = list(inputs["angles"].values())[0]
        pure_states_distribution = list(inputs["probs"].values())[0]
        input_name = inputs["saving_name"]

        # Cover all the classical states            
        covered_numbers = covered_pure_states(pure_states_distribution)
        num_classical_inputs = len(L_list) * len(sign_list)
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for L, sign in product(L_list, sign_list):
                test_cases += 1
                qc = QuantumCircuit(2 * n + m, n)

                con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                if con_pre_mode == 'sep':
                    qc_con = separable_control_state_preparation(angle_list)
                elif con_pre_mode == 'ent':
                    qc_con = entangled_control_state_preparation(angle_list)
                
                qc.append(qc_con, qc.qubits[:m]) # type: ignore

                if mixed_pre_mode == 'bits':
                    qc = bit_controlled_preparation_1MS(n, m, qc)
                elif mixed_pre_mode == 'qubits':
                    qc = qubit_controlled_preparation_1MS(n, m, qc) 
                    
                # Append the tested quantum subroutine (quantum program) 
                func = get_target_version(version_dict, program_version)
                qc_test = func(n, L, geq=sign)
                qc.append(qc_test, qc.qubits[m:])
                qc.measure(qc.qubits[m + n:],qc.clbits[:])
                
                # Execute the program and derive the outputs
                dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = outputdict2samps(dict_counts)
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, L, sign)
                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                # Derive the test result by nonparametric hypothesis test
                test_result = OPO_UTest(exp_samps, test_samps)
                if test_result == 'fail':
                    total_failures += 1

        dura_time = time.time() - start_time
        recorded_result.append({            
            "input_name": input_name,
            "num_shots": shots,
            "controlling_unit": mixed_pre_mode,
            "num_test_cases": test_cases, 
            "ave_exe_time": dura_time / num_classical_inputs / repeats,
            "ave_faults": total_failures / test_cases / repeats
        })
    return recorded_result

def testing_process_MSTCs_2MS(
    program_version: str, 
    L_list: list[int], 
    sign_list: list[bool], 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"], 
    shots: int,
    repeats: int
) -> list[dict]:
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

    recorded_result = []      
    for inputs in inputs_list:
        # Assign values to variables
        n, m = inputs["num_target"], inputs["num_control"]
        angle_lists = list(inputs["angles"].values())
        pure_states_distributions = list(inputs["probs"].values())
        input_name = inputs["saving_name"]

        # Return the indices from zero to num_test_cases - 1
        MSB_val_list = list(range(len(angle_lists)))

        # Cover all the classical states            
        covered_numbers = covered_pure_states(pure_states_distribution)
        num_classical_inputs = len(L_list) * len(sign_list)
        start_time = time.time()
        total_failures = 0

        for _ in range(repeats):
            test_cases = 0
            for L, sign in product(L_list, sign_list):
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
                    
                    qc.append(qc_con, qc.qubits[:m]) # type: ignore

                    if mixed_pre_mode == 'bits':
                        qc = bit_controlled_preparation_2MS(n, m, qc)
                    elif mixed_pre_mode == 'qubits':
                        qc = qubit_controlled_preparation_2MS(n, m, qc) 
                        
                    # Append the tested quantum subroutine (quantum program) 
                    func = get_target_version(version_dict, program_version)
                    qc_test = func(n, L, geq=sign)

                    qc.append(qc_test, qc.qubits[m:])
                    qc.measure(qc.qubits[m + n:],qc.clbits[:])
                    
                    # Execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = outputdict2samps(dict_counts)
                    
                    # Generate the samples that follow the expected probability distribution
                    exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, L, sign)
                    exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                    # Derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                    if test_result == 'fail':
                        total_failures += 1

        dura_time = time.time() - start_time
        recorded_result.append({            
            "input_name": input_name,
            "num_shots": shots, 
            "controlling_unit": mixed_pre_mode,
            "num_test_cases": test_cases, 
            "ave_exe_time": dura_time / num_classical_inputs / repeats,
            "ave_faults": total_failures / test_cases / repeats
        })
    return recorded_result

def testing_process_MSTCs_MPS(    
    program_version: str, 
    L_list: list[int], 
    sign_list: list[bool], 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    shots: int, 
    repeats: int
) -> list[dict]:
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
 
    recorded_result = []      
    state_list = ['mixed', 'pure']

    for inputs in inputs_list:
        # Assign values to variables
        n, m = inputs["num_target"], inputs["num_control"]
        angle_list = list(inputs["angles"].values())[0]
        pure_states_distribution = list(inputs["probs"].values())[0]
        input_name = inputs["saving_name"]

        # Cover all the classical states            
        covered_numbers = covered_pure_states(pure_states_distribution)
        num_classical_inputs = len(L_list) * len(sign_list)
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for L, sign in product(L_list, sign_list):
                for temp_state in state_list:
                    test_cases += 1
                    if temp_state == 'mixed':
                        qc = QuantumCircuit(2 * n + m, n + m)
                        # Prepare the control state
                        con_pre_mode = 'sep' if n == len(angle_list) else 'ent'
                        if con_pre_mode == 'sep':
                            qc_con = separable_control_state_preparation(angle_list)
                        elif con_pre_mode == 'ent':
                            qc_con = entangled_control_state_preparation(angle_list)
                        qc.append(qc_con, qc.qubits[:m]) # type: ignore
                        # Connect the control and target qubits
                        if mixed_pre_mode == 'bits':
                            qc = bit_controlled_preparation_MPS(n, m, qc)
                        elif mixed_pre_mode == 'qubits':
                            qc = qubit_controlled_preparation_MPS(n, m, qc)
                    elif temp_state == 'pure':
                        qc = QuantumCircuit(2 * n, n)
                        qc = pure_state_preparation(n, qc)
                        
                    # Append the tested quantum subroutine (quantum program) 
                    func = get_target_version(version_dict, program_version)
                    qc_test = func(n, L, geq=sign)

                    # Execute the program and derive the outputs
                    if temp_state == 'mixed':
                        qc.append(qc_test, qc.qubits[m:])
                        qc.measure(qc.qubits[n + m:], qc.clbits[-n:])
                        # Remove the unexpected value until the valid values meets
                        # the required number of samples  
                        invalid_con_list = [int('1' * m, 2)]
                        invalid_num_list = generate_invalid_numbers(qc.num_qubits, m, invalid_con_list)
                        dict_counts = repeat_until_success(qc, shots, invalid_num_list)
                    elif temp_state == 'pure':
                        qc.append(qc_test, qc.qubits[:])
                        qc.measure(qc.qubits[n:], qc.clbits[:])
                        dict_counts = circuit_execution(qc, shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        if temp_state == 'mixed':   # Remove the output of control qubits (low m bits)
                            test_samps += [key >> m] * value
                        else:
                            test_samps += [key] * value
                    
                    # Generate the samples that follow the expected probability distribution
                    if temp_state == "mixed":
                        exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, L, sign)
                        exp_samps = list(
                            np.random.choice(
                                range(2 ** (qc.num_clbits - m)), 
                                size=shots, 
                                p=exp_probs
                        ))
                    elif temp_state == "pure":
                        exp_probs = PSTC_specification(n, 2 ** n - 1, L, sign)
                        exp_samps = list(
                            np.random.choice(
                                range(2 ** (qc.num_clbits)), 
                                size=shots, 
                                p=exp_probs
                        ))               
                                        
                    # Derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                    if test_result == 'fail':
                        total_failures += 1

        dura_time = time.time() - start_time
        recorded_result.append({            
            "input_name": input_name,
            "num_shots": shots, 
            "controlling_unit": mixed_pre_mode,
            "num_test_cases": test_cases, 
            "ave_exe_time": dura_time / num_classical_inputs / repeats,
            "ave_faults": total_failures / test_cases / repeats
        })
    return recorded_result