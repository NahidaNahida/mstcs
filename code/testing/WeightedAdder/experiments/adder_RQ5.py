from typing import Literal, Callable
from functools import partial

from . import (
    program_name,
    exe_repeats,
    HEADER_DICT,
    required_data,
    testing_process_MSTCs_1MS,
    testing_process_MSTCs_2MS,
    testing_process_PSTCs,
    rep_mode_selection,
    RQ_saving_dir,
    csv_saving
)

# =================================================================
# Configurations varying with RQs
_RQ_NAME = "RQ5"
header = HEADER_DICT[_RQ_NAME]
 
def _RQ_running_PSTCs(
    program_version: str, 
    n_list: list[int], 
    weights_dict: dict[str, list[list]],
    shot_list: list[int], 
    repeats: int
) -> list[list]:
    recorded_list = []
    for shots in shot_list:
        temp_list = testing_process_PSTCs(
            program_version,
            n_list,
            weights_dict,
            shots,
            repeats
        )
        recorded_list = recorded_list + temp_list
    return required_data(_RQ_NAME, recorded_list)

def _RQ_running_MSTC_core(
    program_version: str,
    weights_dict: dict[str, list[list]],
    inputs_list: list, 
    mixed_pre_mode: Literal["bits", "qubits"],
    shot_list: list[int],
    repeats: int,
    process_func: Callable
) -> list[list]:
    recorded_list = []
    for shots in shot_list:
        temp_list = process_func(
            program_version,
            weights_dict,
            inputs_list,
            mixed_pre_mode,
            shots,
            repeats
        )
        recorded_list = recorded_list + temp_list
    return required_data(_RQ_NAME, recorded_list)

# === Concrete instantiation, using functools.partial to bind process_func ===
_RQ_running_MSTCs_1MS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_1MS)
_RQ_running_MSTCs_2MS = partial(_RQ_running_MSTC_core, process_func=testing_process_MSTCs_2MS)

if __name__ == '__main__':
    import argparse
    from ..config.RQ5_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument("--mode", type=str, help="replication mode:'toy' or 'all'", default=None)
    args = parser.parse_args()

    input_data = rep_mode_selection(config_dict, args.mode)

    exe_dict = {
        "PSTC": {"function": _RQ_running_PSTCs}, 
        "MSTC(1MS)": { 
            "function": _RQ_running_MSTCs_1MS,
            "mixed_states": [input_data["mixed_state_suites"]["test_suite_1MS"]]
        },
        "MSTC(2MS)": {
            "function": _RQ_running_MSTCs_2MS,
            "mixed_states": [input_data["mixed_state_suites"]["test_suite_2MS"]]
        }           
    }

    save_dir = RQ_saving_dir(_RQ_NAME, program_name, args.mode)
    # Execute the test processes
    for program_version in input_data["versions"]:
        print(program_version)
        for task_name, current_exe in exe_dict.items():
            n_list = input_data["qubit_list"]
            weight_dict = input_data["weight_dict"]
            shot_list = input_data["shots_list"]
            exe_function = current_exe["function"]
            if task_name == "PSTC":
                recorded_data = exe_function(
                    program_version,
                    n_list,
                    weight_dict,
                    shot_list,
                    exe_repeats
                )
            # else:
            #     input_states = current_exe["mixed_states"]
            #     recorded_data = exe_function(
            #         program_version,
            #         weight_dict,
            #         input_states,
            #         "qubits",
            #         shot_list,
            #         exe_repeats
            #     )

            # Save the data
            csv_saving(_RQ_NAME, program_name, program_version, save_dir, header, task_name, recorded_data)

    print(f"{program_name}-{_RQ_NAME} done!")