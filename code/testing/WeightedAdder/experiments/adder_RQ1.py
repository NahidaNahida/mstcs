import numpy as np
import os
import math, time
from typing import Literal

from qiskit import QuantumCircuit

from ....utils import (
    generate_numbers, 
    import_versions,
    get_target_version, 
    circuit_execution, 
    OPO_UTest,
    csv_saving,
    RQ_saving_dir,
    bit_controlled_preparation_1MS,
    qubit_controlled_preparation_1MS,
    rep_mode_selection
)

from ....config import (
    HEADER_DICT, 
    pure_state_distribution, 
    control_qubit_numbers, 
    covered_pure_states
)

from . import PSTC_specification, MSTC_specification
from . import default_shots, program_name, candidate_initial_states

# =================================================================
# Configurations varying with RQs
_RQ_NAME = "RQ1"
header = HEADER_DICT[_RQ_NAME]

# Get the file directory
current_dir = os.path.dirname(__file__)
version_dir = os.path.join(os.path.dirname(current_dir), "programs")
config_dir = os.path.join(os.path.dirname(current_dir), "config")

# Import the program versions under the same directory
version_dict = import_versions(program_name, version_dir)

def testing_process_PSTCs(
    program_version: str, 
    n_list: list[int], 
    weights_dict: dict[int, list[list]], 
    repeats: int = 20
) -> None:
    recorded_result = [] 
    for n in n_list:            
        initial_states_list = generate_numbers(
            n, 
            len(candidate_initial_states)
        )
        weights_list = weights_dict[f"qubit_num={n}"] # pyright: ignore[reportArgumentType]
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
                func = get_target_version(version_dict, program_version)
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
) -> None:
    recorded_result = [] 
    for n in n_list:  
        # Define the uniform distribution for the ensemble
        pure_states_distribution = pure_state_distribution(n, "uniform")
        
        # Cover all the classical states            
        covered_numbers = covered_pure_states(n, "all_basis")
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
        
        # Determine m = n for this experiment
        pre_time = 0                            # Record time for state preparation
        m = control_qubit_numbers(n, "equal")   # Determine the number of the control qubits.
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
                dict_counts = circuit_execution(qc, default_shots)

                # Obtain the samples (measurement results) of the tested program
                test_samps = []
                for (key, value) in dict_counts.items():
                    test_samps += [key] * value
                
                # Generate the samples that follow the expected probability distribution
                exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, n, s, weight)
                exp_samps = list(np.random.choice(range(2 ** qc.num_clbits), size=default_shots, p=exp_probs))

                # Derive the test result by nonparametric hypothesis test
                test_result = OPO_UTest(exp_samps, test_samps)
                    
        dura_time = time.time() - start_time
        recorded_result.append([
            n, 
            test_cases, 
            dura_time / num_classical_inputs / repeats, 
            pre_time / num_classical_inputs / repeats
        ])
 
    # save the data
    save_dir = RQ_saving_dir(_RQ_NAME, program_name)
    csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, f"{pre_mode}_MSTC", recorded_result)

if __name__ == '__main__':
    import argparse
    from ..config.RQ1_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument("--mode", type=str, help="replication mode:'toy' or 'all'", default=None)
    args = parser.parse_args()

    input_data = rep_mode_selection(config_dict, args.mode)
        
    for program_version in input_data["versions"]:
        print(program_version)
        testing_process_PSTCs(program_version, input_data["qubit_list"], input_data["weight_dict"])
        testing_process_MSTCs(program_version, input_data["qubit_list"], input_data["weight_dict"], 'bits')
        testing_process_MSTCs(program_version, input_data["qubit_list"], input_data["weight_dict"], 'qubits')
    
    print(f"{program_name}-{_RQ_NAME} done!")