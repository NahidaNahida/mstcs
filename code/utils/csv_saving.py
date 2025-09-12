import csv, os

def RQ_saving_dir(
    rq_name: str | int,
    program_name: str
) -> str:
    if isinstance(rq_name, int):
        rq_name = f"RQ{rq_name}"
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    saving_path = os.path.join(
        root_dir,
        "data",
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
    file_name = RQ_saving_name(rq_name, program_name, program_ver, task_name)
    with open(os.path.join(save_dir, file_name), mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header)
        for data in data_list:
            writer.writerow(data)
    print(f"{task_name} is done!")


if __name__ == "__main__":
    # Unit testing of ``RQ_saving_path``
    expected_rq = "RQ3"
    expected_program = "QuantumFourierTransform"
    expected_dir = "data\\raw_data_for_empirical_results\\RQ3\\QuantumFourierTransform"
    
    res_dir = RQ_saving_dir(expected_rq, expected_program)
    assert expected_dir in res_dir, "Wrong directory!"