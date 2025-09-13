import numpy as np
import os
import math, time
from typing import Literal

from qiskit import QuantumCircuit

from ....utils import (
    import_versions,
    get_target_version, 
    circuit_execution, 
    OPO_UTest,
    csv_saving,
    RQ_saving_dir,
    bit_controlled_preparation_1MS,
    qubit_controlled_preparation_1MS,
    bit_controlled_preparation_2MS,
    qubit_controlled_preparation_2MS,
    bit_controlled_preparation_MPS,
    qubit_controlled_preparation_MPS,
    separable_control_state_preparation,
    entangled_control_state_preparation,
    repeat_until_success,
    generate_invalid_numbers,
    rep_mode_selection
)

from ....config import (
    HEADER_DICT, 
    covered_pure_states
)

from . import PSTC_specification, MSTC_specification
from . import default_shots, program_name 

# =================================================================
# Configurations varying with RQs
_RQ_NAME = "RQ2"
header = HEADER_DICT[_RQ_NAME]

# Get the file directory
current_dir = os.path.dirname(__file__)
version_dir = os.path.join(os.path.dirname(current_dir), "programs")
config_dir = os.path.join(os.path.dirname(current_dir), "config")

# Import the program versions under the same directory
version_dict = import_versions(program_name, version_dir)

        
def testing_process_MSTCs_1MS(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    repeats: int = 20,
) -> list:
    """
    Test a quantum program by covering multiple classical inputs with 
    a single mixed state (MSTCs with one mixed state).

    The function prepares mixed quantum states, executes the given quantum
    program under different control configurations, and evaluates the test 
    results using nonparametric hypothesis testing.

    Example (n = 2):
        rho = 1/4 * (|0><0| + |1><1| + |2><2| + |3><3|)

    Args:
        program_version (str): 
            Identifier for the target program version to be tested.
        weights_dict (dict): 
            Dictionary mapping qubit numbers to weight vectors. 
            Keys are of the form "qubit_num={n}".
        inputs_list (list): 
            A list of input configurations. Each element is a dict containing:
                - "num_target" (int): Number of target qubits.
                - "num_control" (int): Number of control qubits.
                - "angles" (list[float]): Angle parameters for control state preparation.
                - "probs" (list[float]): Probability distribution over pure states.
                - "saving_name" (str): Identifier for the test input.
        mixed_pre_mode (Literal["bits", "qubits"]): 
            Mode for preparing the mixed state:
                - "bits": classical-bit controlled preparation.
                - "qubits": quantum-qubit controlled preparation.
        repeats (int, optional): 
            Number of repetitions per input configuration. Defaults to 20.

    Returns:
        list: A list of test results. Each element is a list:
            [input_name, mixed_pre_mode, test_cases, avg_time_per_case],
            where:
                - input_name (str): Identifier of the input configuration.
                - mixed_pre_mode (str): Mixed state preparation mode used.
                - test_cases (int): Number of test cases executed.
                - avg_time_per_case (float): Average runtime per test case.
    """
    recorded_result = []      
    
    for inputs in inputs_list:
        # Assign values to variables
        n, m = inputs["num_target"], inputs["num_control"]
        angle_list = list(inputs["angles"].values())[0]
        pure_states_distribution = list(inputs["probs"].values())[0]
        input_name = inputs["saving_name"]

        # Cover all the classical states            
        covered_numbers = covered_pure_states(n, "all_basis")
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
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
        recorded_result.append([
            input_name, 
            mixed_pre_mode,
            test_cases, 
            dura_time / num_classical_inputs / repeats
        ])
    return recorded_result

def testing_process_MSTCs_2MS(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"], 
    repeats: int = 20
) -> list:
    """
    Test a quantum program by covering classical inputs with 
    two mixed states (MSTCs with 2MS).

    Given n target qubits, the two mixed states are defined as:
        rho1 = 1/(2^(n-1)) * (|0><0| + ... + |2^(n-1)-1><2^(n-1)-1|)
        rho2 = 1/(2^(n-1)) * (|2^(n-1)><2^(n-1)| + ... + |2^n-1><2^n-1|)

    Example (n = 2):
        rho1 = 1/2 * (|0><0| + |1><1|)
        rho2 = 1/2 * (|2><2| + |3><3|)

    Args:
        program_version (str): 
            Identifier for the target quantum program version to be tested.
        weights_dict (dict): 
            Dictionary mapping qubit numbers to weight vectors. 
            Keys are of the form "qubit_num={n}".
        inputs_list (list): 
            A list of input configurations. Each element is a dict containing:
                - "num_target" (int): Number of target qubits.
                - "num_control" (int): Number of control qubits.
                - "angles" (list[list[float]]): 
                      Two lists of angle parameters for preparing control states.
                - "probs" (list[list[float]]): 
                      Two probability distributions for input pure states.
                - "saving_name" (str): Identifier for the test input.
        mixed_pre_mode (Literal["bits", "qubits"]): 
            Mode for preparing the mixed state:
                - "bits": classical-bit controlled preparation.
                - "qubits": quantum-qubit controlled preparation.
        repeats (int, optional): 
            Number of repetitions per input configuration. Defaults to 20.

    Returns:
        list: A list of test results. Each element is a list:
            [input_name, mixed_pre_mode, test_cases, avg_time_per_case],
            where:
                - input_name (str): Identifier of the input configuration.
                - mixed_pre_mode (str): Mixed state preparation mode used.
                - test_cases (int): Number of test cases executed.
                - avg_time_per_case (float): Average runtime per test case.
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
        covered_numbers = covered_pure_states(n, "all_basis")
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
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

                    # prepare the control qubits
                    con_pre_mode = 'sep' if m == len(angle_list) else 'ent'
                    if con_pre_mode == 'sep':
                        qc_con = separable_control_state_preparation(angle_list)
                    elif con_pre_mode == 'ent':
                        qc_con = entangled_control_state_preparation(angle_list)
                    qc.append(qc_con, qc.qubits[:m])  # type: ignore

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
        recorded_result.append([
            input_name, 
            mixed_pre_mode,
            test_cases, 
            dura_time / num_classical_inputs / repeats
        ])
    return recorded_result

def testing_process_MSTCs_MPS(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"], 
    repeats: int = 20
):
    """
    Test a quantum program by covering classical inputs with 
    one mixed state and one pure state (MSTCs with MPS).

    The mixed state includes all basis states except the highest one,
    and the pure state is the highest basis state.

    Definition for n target qubits:
        rho_mixed = 1/(2^n - 1) * (|0><0| + ... + |2^n-2><2^n-2|)
        rho_pure  = |2^n-1><2^n-1|

    Example (n = 2):
        rho_mixed = 1/3 * (|0><0| + |1><1| + |2><2|)
        rho_pure  = |3><3|

    This test is particularly useful for verifying 
    repeat-until-success structures when N is not a power of m.

    Args:
        program_version (str): 
            Identifier for the target quantum program version to be tested.
        weights_dict (dict): 
            Dictionary mapping qubit numbers to weight vectors. 
            Keys are of the form "qubit_num={n}".
        inputs_list (list): 
            A list of input configurations. Each element is a dict containing:
                - "num_target" (int): Number of target qubits.
                - "num_control" (int): Number of control qubits.
                - "angles" (list[float]): 
                      Angle parameters for preparing the control state.
                - "probs" (list[float]): 
                      Probability distribution over input pure states.
                - "saving_name" (str): Identifier for the test input.
        mixed_pre_mode (Literal["bits", "qubits"]): 
            Mode for preparing the mixed state:
                - "bits": classical-bit controlled preparation.
                - "qubits": quantum-qubit controlled preparation.
        repeats (int, optional): 
            Number of repetitions per input configuration. Defaults to 20.

    Returns:
        list: A list of test results. Each element is a list:
            [input_name, mixed_pre_mode, test_cases, avg_time_per_case],
            where:
                - input_name (str): Identifier of the input configuration.
                - mixed_pre_mode (str): Mixed state preparation mode used.
                - test_cases (int): Number of test cases executed.
                - avg_time_per_case (float): Average runtime per test case.
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
        covered_numbers = covered_pure_states(n, "all_basis")
        weights_list = weights_dict[f"qubit_num={n}"]

        num_classical_inputs = len(weights_list)
        start_time = time.time()
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
                        dict_counts = repeat_until_success(qc, default_shots, invalid_num_list)
                    elif temp_state == 'pure':
                        qc.append(qc_test, qc.qubits[:])
                        qc.measure(qc.qubits[-s:], qc.clbits[:])
                        dict_counts = circuit_execution(qc, default_shots)

                    # Obtain the samples (measurement results) of the tested program
                    test_samps = []
                    for (key, value) in dict_counts.items():
                        if temp_state == 'mixed':   # Remove the output of control qubits (low m bits)
                            test_samps += [key >> m] * value
                        else:
                            test_samps += [key] * value
                    
                    # Generate the samples that follow the expected probability distribution
                    if temp_state == "mixed":
                        exp_probs = MSTC_specification(covered_numbers, pure_states_distribution, n, s, weight)
                        exp_samps = list(np.random.choice(
                            range(2 ** (qc.num_clbits - m)), 
                            size=default_shots, 
                            p=exp_probs
                        ))
                    elif temp_state == "pure":
                        exp_probs = PSTC_specification(s, [1] * n, weight)
                        exp_samps = list(np.random.choice(
                            range(2 ** (qc.num_clbits)), 
                            size=default_shots, 
                            p=exp_probs
                        ))               
                                        
                    # derive the test result by nonparametric hypothesis test
                    test_result = OPO_UTest(exp_samps, test_samps)
                            
        dura_time = time.time() - start_time
        recorded_result.append([
            input_name, 
            mixed_pre_mode, 
            test_cases, 
            dura_time / num_classical_inputs / repeats
        ])
    return recorded_result

if __name__ == '__main__':
    import argparse
    from ..config.RQ2_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument("--mode", type=str, help="replication mode:'toy' or 'all'", default=None)
    args = parser.parse_args()

    input_data = rep_mode_selection(config_dict, args.mode)

    exe_dict = {
        "inputs_2MS": {
            "function": testing_process_MSTCs_2MS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_0"],
                input_data["mixed_state_suites"]["test_suite_3"]
            ]
        },
        "inputs_1MS": {
            "function": testing_process_MSTCs_1MS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_1"],
                input_data["mixed_state_suites"]["test_suite_2"],
                input_data["mixed_state_suites"]["test_suite_4"],
                input_data["mixed_state_suites"]["test_suite_5"]
            ]
        },
        "inputs_MPS_sep": {
            "function": testing_process_MSTCs_MPS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_6_separable"]
            ]
        },
        "inputs_MPS_ent": {
            "function": testing_process_MSTCs_MPS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_6_entangled"]                
            ]
        }
    }

    # Execute the test process
    for program_version in input_data["versions"]:
        print(program_version)
        recorded_result = []
        for current_exe in exe_dict.values():
            for mode in ["bits", "qubits"]:
                exe_function = current_exe["function"]
                input_states = current_exe["mixed_states"]
                recorded_result = recorded_result + exe_function(
                    program_version, 
                    input_data["weight_dict"], 
                    input_states,
                    mode
                )

        # Save the data
        save_dir = RQ_saving_dir(_RQ_NAME, program_name)
        csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, "", recorded_result)
    print(f"{program_name}-{_RQ_NAME} done!")