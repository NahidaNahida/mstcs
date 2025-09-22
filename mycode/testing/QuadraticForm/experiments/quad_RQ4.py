from typing import Literal, Callable
from functools import partial

from . import (
    program_name,
    default_shots,
    exe_repeats,
    HEADER_DICT,
    required_data,
    testing_process_MSTCs_1MS,
    testing_process_MSTCs_2MS,
    rep_mode_selection,
    RQ_saving_dir,
    csv_saving
)

# =================================================================
# Configurations varying with RQs
_RQ_NAME = "RQ4"
header = HEADER_DICT[_RQ_NAME]

def _RQ_running_MSTC_core(
    program_version: str, 
    matA_dict: dict[str, list],
    vecB_dict: dict[str, list],
    c_list: list[int],
    num_outs: list[int],
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    repeats: int,
    process_func: Callable
) -> list:
    recorded_list = process_func(
        program_version,
        matA_dict,
        vecB_dict,
        c_list,
        num_outs,
        inputs_list,
        mixed_pre_mode,
        default_shots,
        repeats
    )
    return required_data(_RQ_NAME, recorded_list)

# === Concrete instantiation, using functools.partial to bind process_func ===
_RQ_running_MSTCs_1MS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_1MS)
_RQ_running_MSTCs_2MS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_2MS)

if __name__ == '__main__':
    import argparse
    from ..config.RQ4_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument("--mode", type=str, help="replication mode:'toy' or 'all'", default=None)
    args = parser.parse_args()

    input_data = rep_mode_selection(config_dict, args.mode)

    exe_dict = {
        "inputs_2MS": {
            "function": _RQ_running_MSTCs_2MS,
            "mixed_states": [
                input_data["mixed_state_suites"][f"test_suite_{idx}"]
                for idx in [0, 1, 2, 3]
            ]
        },
        "inputs_1MS": {
            "function": _RQ_running_MSTCs_1MS,
            "mixed_states": [
                input_data["mixed_state_suites"][f"test_suite_{idx}"]
                for idx in [4, 5, 6, 7]
            ]
        }
    }

    save_dir = RQ_saving_dir(_RQ_NAME, program_name, args.mode)
    # Execute the test process
    for program_version in input_data["versions"]:
        print(program_version)
        recorded_result = []
        for current_exe in exe_dict.values():
            exe_function = current_exe["function"]
            input_states = current_exe["mixed_states"]
            matA_dict = input_data["matrix_A"]
            vecB_dict = input_data["vector_B"]
            C_list = input_data["integer_C"]
            num_outs = input_data["num_outs"]
            recorded_result = recorded_result + exe_function(
                program_version, 
                matA_dict, 
                vecB_dict, 
                C_list, 
                num_outs,
                input_states, 
                'qubits',
                exe_repeats
            )     
        # Save the data
        csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, "", recorded_result)
    
    print(f"{program_name}-{_RQ_NAME} done!")