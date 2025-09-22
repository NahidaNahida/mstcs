import numpy as np
import os
import time
from typing import Literal

from qiskit import QuantumCircuit

from ....utils import (
    generate_numbers,
    outputdict2samps, 
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

from ....config import (
    pure_state_distribution, 
    control_qubit_numbers
)

from . import PSTC_specification, MSTC_specification
from ..config import candidate_initial_states 

# =================================================================
# Get the file directory
current_dir = os.path.dirname(__file__)
config_dir = os.path.join(os.path.dirname(current_dir), "config")

def testing_process_PSTCs(
    n_list: list[int],
    shots: int,  
    repeats: int
) -> list[dict]:

    recorded_result = [] 
    for n in n_list:
        # Generate all possible initial classical states for testing    
        initial_states_list = generate_numbers(
            n, 
            len(candidate_initial_states)
        )
        
        start_time = time.time()
        pre_time = 0                        # Record cumulative time spent on state preparation
        total_failures = 0                  # Count total number of failed tests
        for _ in range(repeats):
            test_cases = 0
            for initial_states in initial_states_list:
                test_cases += 1
                # Convert list of binary digits to decimal number
                number = int(''.join(map(str, initial_states)), 2)
                # Reverse the bit order for Qiskit convention
                initial_states = initial_states[::-1]
                qc = QuantumCircuit(n, n)

                # State preparation
                pre_start_time = time.time()
                for index, val in enumerate(initial_states):
                    if candidate_initial_states[val] == 1:
                        qc.x(index)      
                pre_end_time = time.time()
                pre_time += pre_end_time - pre_start_time

                qc.measure(qc.qubits[:],qc.clbits[:])

                # Execute the program and derive the outputs
                dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = outputdict2samps(dict_counts)
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = PSTC_specification(n, number)
                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

                # derive the test result by nonparametric hypothesis test
                test_result = OPO_UTest(exp_samps, test_samps) 

                if test_result == 'fail':
                    total_failures += 1

        dura_time = time.time() - start_time
        recorded_result.append({
            "num_qubits": n,
            "num_shots": shots,
            "num_test_cases": test_cases,
            "ave_faults": total_failures / test_cases / repeats,
            "ave_exe_time": dura_time / repeats, 
            "ave_pre_time": pre_time / repeats
        })
    
    return recorded_result

def testing_process_MSTCs(
    n_list: list[int], 
    pre_mode: Literal["bits", "qubits"],
    shots: int, 
    repeats: int,
    pure_state_dist: Literal["uniform"] = "uniform",
    num_controls: Literal["equal"] = "equal"
) -> list[dict]:

    recorded_result = [] 
    for n in n_list:  
        # Define the uniform distribution for the ensemble
        pure_states_distribution = pure_state_distribution(n, pure_state_dist)

        start_time = time.time()
        pre_time = 0                                  # Record time for state preparation
        total_failures = 0

        m = control_qubit_numbers(n, num_controls)    # Determine m = n for this experiment
        for _ in range(repeats):
            qc = QuantumCircuit(n + m, n)
            
            # Prepare the control state
            pre_start_time = time.time() 
            qc.h(qc.qubits[:m])
            
            # Mixed state preparation
            if pre_mode == 'bits':
                qc = bit_controlled_preparation_1MS(n, m, qc)
            elif pre_mode == 'qubits':
                qc = qubit_controlled_preparation_1MS(n, m, qc)
            pre_end_time = time.time()
            pre_time += pre_end_time - pre_start_time                              
            qc.measure(qc.qubits[m:],qc.clbits[:])

            # Execute the program and derive the outputs
            dict_counts = circuit_execution(qc, shots)

            # Obtain the samples (measurement results) of the tested program
            test_samps = outputdict2samps(dict_counts)
            
            # Generate the samples that follow the expected probability distribution
            exp_probs = MSTC_specification(pure_states_distribution)
            exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=shots, p=exp_probs))

            # Derive the test result by nonparametric hypothesis test
            test_result = OPO_UTest(exp_samps, test_samps)

            if test_result == 'fail':
                total_failures += 1

        dura_time = time.time() - start_time
        recorded_result.append({
            "num_qubits": n,
            "num_shots": shots,
            "num_test_cases": 1,
            "ave_faults": total_failures / repeats,
            "ave_exe_time": dura_time / repeats, 
            "ave_pre_time": pre_time / repeats
        })

    return recorded_result

def testing_process_MSTCs_1MS(
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    shots: int, 
    repeats: int
) -> list[dict]:

    recorded_result = []      
    
    for inputs in inputs_list:
        n, m = inputs["num_target"], inputs["num_control"]
        angle_list = list(inputs["angles"].values())[0]
        pure_states_distribution = list(inputs["probs"].values())[0]
        input_name = inputs["saving_name"]
 
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 1
            qc = QuantumCircuit(n + m, n)

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
            qc.measure(qc.qubits[m:], qc.clbits[:])
            
            # Execute the program and derive the outputs
            dict_counts = circuit_execution(qc, shots)

            # Obtain the samples (measurement results) of the tested program
            test_samps = []
            for (key, value) in dict_counts.items():
                test_samps += [key] * value
            
            # Generate the samples that follow the expected probability distribution
            exp_probs = MSTC_specification(pure_states_distribution)
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
            "ave_exe_time": dura_time / repeats,
            "ave_faults": total_failures / test_cases / repeats
        })
    return recorded_result

def testing_process_MSTCs_2MS(    
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"], 
    shots: int,
    repeats: int
) -> list[dict]:

    recorded_result = []      
    for inputs in inputs_list:
        # Assign values to variables
        n, m = inputs["num_target"], inputs["num_control"]
        angle_lists = list(inputs["angles"].values())
        pure_states_distributions = list(inputs["probs"].values())
        input_name = inputs["saving_name"]
    
        # Return the indices from zero to num_test_cases - 1
        MSB_val_list = list(range(len(angle_lists)))

        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for MSB_val in MSB_val_list:
                test_cases += 1
                angle_list = angle_lists[MSB_val]
                pure_states_distribution = pure_states_distributions[MSB_val]

                qc = QuantumCircuit(n + m, n)
                
                # Prepare the most significant qubit
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
                qc.measure(qc.qubits[m:],qc.clbits[:])
                
                # Execute the program and derive the outputs
                dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = []
                for (key, value) in dict_counts.items():
                    test_samps += [key] * value
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(pure_states_distribution)
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
            "ave_exe_time": dura_time / repeats,
            "ave_faults": total_failures / test_cases / repeats
        })
    return recorded_result

def testing_process_MSTCs_MPS(
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    shots: int,
    repeats: int
) -> list[dict]:
    
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
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for temp_state in state_list:
                test_cases += 1
                if temp_state == 'mixed':
                    qc = QuantumCircuit(n + m, n + m)     
                    
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
                    qc = QuantumCircuit(n, n)            # for PSTCs
                    qc = pure_state_preparation(n, qc)

                # Execute the program and derive the outputs
                if temp_state == 'mixed':
                    qc.measure(qc.qubits[m:], qc.clbits[-n:])
                    # Remove the unexpected value until the valid values meets
                    # the required number of samples  
                    invalid_con_list = [int('1' * m, 2)]
                    invalid_num_list = generate_invalid_numbers(qc.num_qubits, m, invalid_con_list)
                    dict_counts = repeat_until_success(qc, shots, invalid_num_list)
                elif temp_state == 'pure':
                    qc.measure(qc.qubits[:], qc.clbits[:])
                    dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = []
                for (key, value) in dict_counts.items():
                    if temp_state == 'mixed':   # remove the output of control qubits (low m bits)
                        test_samps += [key >> m] * value
                    else:
                        test_samps += [key] * value
                
                # Generate the samples that follow the expected probability distribution
                if temp_state == "mixed":
                    exp_probs = MSTC_specification(pure_states_distribution)
                    # Discard the results from the control qubits
                    exp_samps = list(
                        np.random.choice(
                            range(2 ** (qc.num_clbits - m)), 
                            size=shots, 
                            p=exp_probs
                        )
                    )
                elif temp_state == "pure":
                    exp_probs = PSTC_specification(n, 2 ** n - 1)
                    exp_samps = list(
                        np.random.choice(
                            range(2 ** (qc.num_clbits)), 
                            size=shots, 
                            p=exp_probs
                        )
                    )               
                                    
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
            "ave_exe_time": dura_time / repeats,
            "ave_faults": total_failures / test_cases / repeats
        })
    return recorded_result