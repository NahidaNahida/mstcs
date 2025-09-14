import csv, os

def RQ_saving_dir(
    rq_name: str | int,
    program_name: str,
    rep_mode: str,
) -> str:
    if isinstance(rq_name, int):
        rq_name = f"RQ{rq_name}"
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    
    if rep_mode == "toy":
        folder_name = f"data({rep_mode})"
    else:
        folder_name = "data"

    saving_path = os.path.join(
        root_dir,
        folder_name,
        "raw_data_for_empirical_results",
        rq_name,
        program_name
    )
    return saving_path

def RQ_saving_name(
    rq_name: str,
    program_name: str,
    program_ver: str,
    task_name: str,
) -> str:
    if task_name == "":
        return f"{rq_name}_{program_name}_{program_ver}.csv"
    else:
        return f"{rq_name}_{program_name}_{program_ver}_{task_name}.csv"

def csv_saving(
    rq_name: str,
    program_name: str,
    program_ver: str,
    save_dir: str,
    header: list[str],
    task_name: str,
    data_list: list[list[float]],
) -> None:
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)

    # Generate the CSV file name
    file_name = RQ_saving_name(rq_name, program_name, program_ver, task_name)
    file_path = os.path.join(save_dir, file_name)

    # Write CSV
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        writer.writerows(data_list)  # more concise than looping

    print(f"{task_name} is done! Saved at {file_path}")


if __name__ == "__main__":
    # Unit testing of ``RQ_saving_path``
    # Run ``python code/utils/csv_saving.py``
    expected_rq = "RQ3"
    expected_program = "QuantumFourierTransform"
    rep_mode = "toy"
    expected_dir = "data(toy)\\raw_data_for_empirical_results\\RQ3\\QuantumFourierTransform"

    res_dir = RQ_saving_dir(expected_rq, expected_program, rep_mode)
    assert expected_dir in res_dir, "Wrong directory!"