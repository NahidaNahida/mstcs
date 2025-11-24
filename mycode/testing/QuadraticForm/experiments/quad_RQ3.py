from typing import Literal

from . import (
    program_name,
    default_shots,
    exe_repeats,
    HEADER_DICT,
    required_data,
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

def _RQ_running_PSTCs(
    program_version: str, 
    n_list: list[int], 
    matA_dict: dict[str, list],
    vecB_dict: dict[str, list],
    c_list: list[int],
    num_outs: list[int],
    repeats: int,
    verbose: bool=False
) -> list[list]:
    
    recorded_list = testing_process_PSTCs(
        program_version,
        n_list,
        matA_dict,
        vecB_dict,
        c_list,
        num_outs,
        default_shots,
        repeats,
        verbose
    )
    return required_data(_RQ_NAME, recorded_list)

def _RQ_running_MSTCs(
    program_version: str,
    n_list: list[int],
    matA_dict: dict[str, list],
    vecB_dict: dict[str, list],
    c_list: list[int],
    num_outs: list[int],  
    pre_mode: Literal["bits", "qubits"], 
    repeats: int,
    verbose: bool=False
) -> list[list]:

    recorded_list = testing_process_MSTCs(
        program_version,
        n_list,
        matA_dict,
        vecB_dict,
        c_list,
        num_outs,
        pre_mode,
        default_shots,
        repeats,
        verbose
    )
    return required_data(_RQ_NAME, recorded_list)


if __name__ == '__main__':
    import argparse
    from ..config.RQ3_config import config_dict

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

    save_dir = RQ_saving_dir(_RQ_NAME, program_name, args.mode)
    exe_dict = {"PSTC": _RQ_running_PSTCs, "MSTC":_RQ_running_MSTCs}
    # Execute the test processes
    for program_version in input_data["versions"]:
        print(program_version)
        for task_name, exe_function in exe_dict.items():
            if task_name == "PSTC":
                recorded_data = exe_function(
                    program_version, 
                    input_data["qubit_list"], 
                    input_data["matrix_A"],
                    input_data["vector_B"],
                    input_data["integer_C"],
                    input_data["num_outs"],
                    exe_repeats,
                    verbose=args.verbose
                )            
            elif task_name == "MSTC":
                recorded_data = exe_function(
                    program_version, 
                    input_data["qubit_list"], 
                    input_data["matrix_A"],
                    input_data["vector_B"],
                    input_data["integer_C"],
                    input_data["num_outs"], 
                    "qubits",
                    exe_repeats,
                    verbose=args.verbose
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
