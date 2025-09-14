from typing import Literal

from . import (
    program_name,
    default_shots,
    exe_repeats,
    HEADER_DICT,
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

def _required_data(recorded_list: list[dict]) -> list[list]:
    recorded_result = [[
            metadata_dict["input_name"],
            metadata_dict["controlling_unit"],
            metadata_dict["num_test_cases"],
            metadata_dict["ave_exe_time"]
        ] 
        for metadata_dict in recorded_list
    ]
    return recorded_result

def _RQ_running_MSTCs_1MS(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    repeats: int
) -> list:
    
    recorded_list = testing_process_MSTCs_1MS(
        program_version,
        weights_dict,
        inputs_list,
        mixed_pre_mode,
        default_shots,
        repeats
    )
    return _required_data(recorded_list)

def _RQ_running_MSTCs_2MS(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"], 
    repeats: int
) -> list:

    recorded_list = testing_process_MSTCs_2MS(
        program_version,
        weights_dict,
        inputs_list,
        mixed_pre_mode,
        default_shots,
        repeats
    )
    return _required_data(recorded_list)

def _RQ_running_MSTCs_MPS(
    program_version: str, 
    weights_dict: dict, 
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"], 
    repeats: int
):
 
    recorded_list = testing_process_MSTCs_MPS(
        program_version,
        weights_dict,
        inputs_list,
        mixed_pre_mode,
        default_shots,
        repeats
    )   
    return _required_data(recorded_list)

if __name__ == '__main__':
    import argparse
    from ..config.RQ2_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument("--mode", type=str, help="replication mode:'toy' or 'all'", default=None)
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
                    exe_repeats
                )

        # Save the data
        csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, "", recorded_result)
    
    print(f"{program_name}-{_RQ_NAME} done!")