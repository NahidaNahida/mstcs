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
    testing_process_MSTCs_MPS,
    rep_mode_selection,
    RQ_saving_dir,
    csv_saving
)

# =================================================================
# Configurations varying with RQs
_RQ_NAME = "RQ2"
header = HEADER_DICT[_RQ_NAME]

def _RQ_running_MSTC_core(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    repeats: int,
    process_func: Callable,
    verbose: bool=False
) -> list:
    recorded_list = process_func(
        program_version,
        weights_dict,
        inputs_list,
        mixed_pre_mode,
        default_shots,
        repeats,
        verbose
    )
    return required_data(_RQ_NAME, recorded_list)

# === Concrete instantiation, using functools.partial to bind process_func ===
_RQ_running_MSTCs_1MS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_1MS)
_RQ_running_MSTCs_2MS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_2MS)
_RQ_running_MSTCs_MPS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_MPS)

if __name__ == '__main__':
    import argparse
    from ..config.RQ2_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument(
        '--mode',
        type=str,
        help="Replication mode, either `toy` for a small subset of test suites or `all` for all the test cases.",
        choices=["toy", "all"],
        default=None
    )
    parser.add_argument(
        "--verbose", 
        action="store_true",
        help="Print detailed progress information."
    )
    args = parser.parse_args()

    input_data = rep_mode_selection(config_dict, args.mode)

    exe_dict = {
        "inputs_2MS": {
            "function": _RQ_running_MSTCs_2MS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_0"],
                input_data["mixed_state_suites"]["test_suite_3"]
            ]
        },
        "inputs_1MS": {
            "function": _RQ_running_MSTCs_1MS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_1"],
                input_data["mixed_state_suites"]["test_suite_2"],
                input_data["mixed_state_suites"]["test_suite_4"],
                input_data["mixed_state_suites"]["test_suite_5"]
            ]
        },
        "inputs_MPS_sep": {
            "function": _RQ_running_MSTCs_MPS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_6_separable"]
            ]
        },
        "inputs_MPS_ent": {
            "function": _RQ_running_MSTCs_MPS,
            "mixed_states": [
                input_data["mixed_state_suites"]["test_suite_6_entangled"]                
            ]
        }
    }

    save_dir = RQ_saving_dir(_RQ_NAME, program_name, args.mode)
    
    # Execute the test process
    for program_version in input_data["versions"]:
        print(program_version)
        recorded_result = []
        for current_exe in exe_dict.values():
            for mode in ["bits", "qubits"]:
                exe_function = current_exe["function"]
                input_states = current_exe["mixed_states"]
                weight_dict = input_data["weight_dict"]
                recorded_result = recorded_result + exe_function(
                    program_version, 
                    weight_dict, 
                    input_states,
                    mode,
                    exe_repeats,
                    verbose=args.verbose
                )

        # Save the data
        csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, "", recorded_result)
    
    print(f"{program_name}-{_RQ_NAME} done!")