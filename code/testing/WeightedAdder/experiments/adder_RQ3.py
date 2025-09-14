from typing import Literal

from . import (
    program_name,
    default_shots,
    exe_repeats,
    HEADER_DICT,
    testing_process_PSTCs,
    testing_process_MSTCs,
    rep_mode_selection,
    RQ_saving_dir,
    csv_saving
)

# =================================================================
# Configurations varying with RQs
_RQ_NAME = "RQ3"
header = HEADER_DICT[_RQ_NAME]

def _required_data(recorded_list: list[dict]) -> list[list]:
    recorded_result = [[
            metadata_dict["num_qubits"],
            metadata_dict["num_test_cases"],
            metadata_dict["ave_faults"]
        ] 
        for metadata_dict in recorded_list
    ]
    return recorded_result
 
def _RQ_running_PSTCs(
    program_version: str, 
    n_list: list[int], 
    weights_dict: dict[str, list[list]], 
    repeats: int
) -> list[list]:
    
    recorded_list = testing_process_PSTCs(
        program_version,
        n_list,
        weights_dict,
        default_shots,
        repeats
    )
    return _required_data(recorded_list)

def _RQ_running_MSTCs(
    program_version: str, 
    n_list: list[int],
    weights_dict: dict[str, list[list]], 
    pre_mode: Literal["bits", "qubits"], 
    repeats: int
) -> list[list]:

    recorded_list = testing_process_MSTCs(
        program_version,
        n_list,
        weights_dict,
        pre_mode,
        default_shots,
        repeats
    )
    return _required_data(recorded_list)

if __name__ == '__main__':
    import argparse
    from ..config.RQ3_config import config_dict

    parser = argparse.ArgumentParser(description=f"adder_{_RQ_NAME}_experiment")
    parser.add_argument("--mode", type=str, help="replication mode:'toy' or 'all'", default=None)
    args = parser.parse_args()

    input_data = rep_mode_selection(config_dict, args.mode)

    save_dir = RQ_saving_dir(_RQ_NAME, program_name, args.mode)
    exe_dict = {"PSTC": _RQ_running_PSTCs, "MSTC":_RQ_running_MSTCs}
    # the test processes
    for program_version in input_data["versions"]:
        print(program_version)
        for task_name, exe_function in exe_dict.items():
            if task_name == "PSTC":
                recorded_data = exe_function(
                    program_version, 
                    input_data["qubit_list"], 
                    input_data["weight_dict"],
                    exe_repeats 
                )            
            elif task_name == "MSTC":
                recorded_data = exe_function(
                    program_version, 
                    input_data["qubit_list"], 
                    input_data["weight_dict"],
                    "qubits",
                    exe_repeats 
                )

            csv_saving(
                _RQ_NAME, 
                program_name, 
                program_version, 
                save_dir, 
                header, 
                task_name, 
                recorded_data
            )
    
    print(f"{program_name}-{_RQ_NAME} done!")