import numpy as np
import os
import math, time
from typing import Literal

from qiskit import QuantumCircuit

from ....utils import (
    generate_numbers,
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
    weights_dict: dict[str, list[list]],
    shots: int, 
    repeats: int
) -> list[dict]:

    recorded_result = [] 
    for n in n_list:            
        initial_states_list = generate_numbers(
            n, 
            len(candidate_initial_states)
        )
        weights_list = weights_dict[f"qubit_num={n}"]   

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        pre_time = 0                                # Record time for state preparation
        total_failures = 0
        for _ in range(repeats):                    # Independent repeats
            test_cases = 0
            for weight in weights_list:             # Calculate the number of output qubits s
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # Append the tested quantum subroutine (quantum program) 
                func = get_target_version(version_dict, program_version)
                qc_test = func(n, weight)

                for initial_states in initial_states_list:
                    test_cases += 1

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
                    dict_counts = circuit_execution(qc, shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = outputdict2samps(dict_counts)
                    
                    # Generate the samples that follow the expected probability distribution
                    exp_probs = PSTC_specification(s, initial_states, weight)
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
    weights_dict: dict[str, list[list]], 
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
        
        # Cover all the classical states            
        scope_of_numbers = list(range(2 ** n))
        
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        
        # Determine m = n for this experiment
        total_failures = 0
        pre_time = 0                                 # Record time for state preparation
        m = control_qubit_numbers(n, num_controls)   # Determine the number of the control qubits.
        for _ in range(repeats):
            test_cases= 0 
            for weight in weights_list:
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # Append the tested quantum subroutine (quantum program) 
                func = get_target_version(version_dict, program_version)
                qc_test = func(n, weight)
                
                test_cases += 1
                qc = QuantumCircuit(m + qc_test.num_qubits, s)

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

                qc.append(qc_test, qc.qubits[m:])
                qc.measure(qc.qubits[n + m: n + m + s],qc.clbits[:])
                    
                # Execute the program and derive the outputs
                dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = outputdict2samps(dict_counts)
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(scope_of_numbers, pure_states_distribution, n, s, weight)
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
    weights_dict: dict[str, list[list]], 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    shots: int, 
    repeats: int
) -> list[dict]:

    recorded_result = []      
    
    for inputs in inputs_list:
        # Assign values to variables
        n, m = inputs["num_target"], inputs["num_control"]
        angle_list = list(inputs["angles"].values())[0]
        pure_states_distribution = list(inputs["probs"].values())[0]
        input_name = inputs["saving_name"]

        # Cover all the classical states            
        scope_of_numbers = list(range(2 ** n))
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:              # Calculate the number of output qubits s
                test_cases += 1
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # Append the tested quantum subroutine (quantum program) 
                func = get_target_version(version_dict, program_version)
                qc_test = func(n, weight)

                qc = QuantumCircuit(m + qc_test.num_qubits, s)
                
                # Prepare the control state    
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
                qc.append(qc_test, qc.qubits[m:])
                qc.measure(qc.qubits[m + n: m + n + s],qc.clbits[:])
                
                # Execute the program and derive the outputs
                dict_counts = circuit_execution(qc, shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = outputdict2samps(dict_counts)
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(scope_of_numbers, pure_states_distribution, n, s, weight)
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
    weights_dict: dict[str, list[list]], 
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

        # Cover all the classical states            
        scope_of_numbers = list(range(2 ** n))
        
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # Append the tested quantum subroutine (quantum program) 
                for MSB_val in MSB_val_list:
                    test_cases += 1
                    angle_list = angle_lists[MSB_val]
                    pure_states_distribution = pure_states_distributions[MSB_val]

                    func = get_target_version(version_dict, program_version)
                    qc_test = func(n, weight)

                    qc = QuantumCircuit(m + qc_test.num_qubits, s)

                    # Prepare the control qubits
                    con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                    if con_pre_mode == 'sep':
                        qc_con = separable_control_state_preparation(angle_list)
                    elif con_pre_mode == 'ent':
                        qc_con = entangled_control_state_preparation(angle_list)
                    
                    qc.append(qc_con, qc.qubits[:m])  # type: ignore

                    # Prepare the most significant qubit
                    if MSB_val == 1:
                        qc.x(m + n - 1)

                    if mixed_pre_mode == 'bits':
                        qc = bit_controlled_preparation_2MS(n, m, qc)
                    elif mixed_pre_mode == 'qubits':
                        qc = qubit_controlled_preparation_2MS(n, m, qc) 
                        
                    # Append the tested quantum subroutine (quantum program) 
                    qc.append(qc_test, qc.qubits[m:])
                    qc.measure(qc.qubits[m + n:m + n + s],qc.clbits[:])
                    
                    # Execute the program and derive the outputs
                    dict_counts = circuit_execution(qc, shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = outputdict2samps(dict_counts)
                    
                    # Generate the samples that follow the expected probability distribution
                    exp_probs = MSTC_specification(scope_of_numbers, pure_states_distribution, n, s, weight)
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
    weights_dict: dict[str, list[list]], 
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
        scope_of_numbers = list(range(2 ** n))

        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        total_failures = 0
        for _ in range(repeats):
            test_cases = 0
            for weight in weights_list:
                if np.sum(weight) == 0:
                    s = 1
                else:
                    s = 1 + math.floor(math.log2(np.sum(weight)))

                # Append the tested quantum subroutine (quantum program) 
                    func = get_target_version(version_dict, program_version)
                    qc_test = func(n, weight)
                for temp_state in state_list:
                    test_cases += 1
                    if temp_state == 'mixed':
                        qc = QuantumCircuit(m + qc_test.num_qubits, m + s)
                        
                        # Prepare the control state
                        con_pre_mode = 'sep' if n == len(angle_list) else 'ent'
                        if con_pre_mode == 'sep':
                            qc_con = separable_control_state_preparation(angle_list)
                        elif con_pre_mode == 'ent':
                            qc_con = entangled_control_state_preparation(angle_list)
                        qc.append(qc_con, qc.qubits[:m])  # type: ignore
                        
                        # Connect the control and target qubits
                        if mixed_pre_mode == 'bits':
                            qc = bit_controlled_preparation_MPS(n, m, qc)
                        elif mixed_pre_mode == 'qubits':
                            qc = qubit_controlled_preparation_MPS(n, m, qc)
                    
                    elif temp_state == 'pure':
                        qc = QuantumCircuit(qc_test.num_qubits, s)
                        qc = pure_state_preparation(n, qc)

                    # Measurement and execute the program and derive the outputs
                    if temp_state == 'mixed':
                        qc.append(qc_test, qc.qubits[m:])
                        qc.measure(qc.qubits[n + m : n + m + s], qc.clbits[-s:])
                        # Remove the unexpected value until the valid values meets
                        # the required number of samples  
                        invalid_con_list = [int('1' * m, 2)]
                        invalid_num_list = generate_invalid_numbers(qc.num_qubits, m, invalid_con_list)
                        dict_counts = repeat_until_success(qc, shots, invalid_num_list)
                    elif temp_state == 'pure':
                        qc.append(qc_test, qc.qubits[:])
                        qc.measure(qc.qubits[-s:], qc.clbits[:])
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
                        exp_probs = MSTC_specification(scope_of_numbers, pure_states_distribution, n, s, weight)
                        exp_samps = list(np.random.choice(
                            range(2 ** (qc.num_clbits - m)), 
                            size=shots, 
                            p=exp_probs
                        ))
                    elif temp_state == "pure":
                        exp_probs = PSTC_specification(s, [1] * n, weight)
                        exp_samps = list(np.random.choice(
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