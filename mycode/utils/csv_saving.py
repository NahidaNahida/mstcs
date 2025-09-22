import csv, os

def RQ_saving_dir(
    rq_name: str | int,
    program_name: str,
    rep_mode: str,
) -> str:
    """
    Generate the directory path for saving raw empirical data.

    This function constructs a standardized saving path based on the 
    research question (RQ) identifier, program name, and repetition mode.
    If ``rq_name`` is an integer, it is automatically converted to the 
    format ``RQ{number}``.

    Parameters
    ----------
    rq_name : str or int
        Research question identifier (e.g., "RQ1" or integer ``1``).
    program_name : str
        Name of the target program.
    rep_mode : str
        Repetition mode, used to select the saving folder. If ``"toy"``, 
        data will be saved under ``data(toy)/``. Otherwise, data will be 
        saved under ``data/``.

    Returns
    -------
    str
        Absolute directory path where raw data will be stored.
    """
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
    """
    Construct a standardized CSV filename for saving results.
    """
    task_str = f"_{task_name}" if task_name != "" else ""
    ver_str = f"_{program_ver}" if program_ver != "" else ""
    return f"{rq_name}_{program_name}{ver_str}{task_str}.csv"

def csv_saving(
    rq_name: str,
    program_name: str,
    program_ver: str,
    save_dir: str,
    header: list[str],
    task_name: str,
    data_list: list[list[float]],
) -> None:
    """
    Save experimental results into a CSV file.

    This function ensures the save directory exists, constructs a 
    standardized filename using ``RQ_saving_name``, and writes the given 
    header and data into the CSV file.

    Parameters
    ----------
    rq_name : str
        Research question identifier (e.g., "RQ1").
    program_name : str
        Name of the target program.
    program_ver : str
        Version identifier of the program.
    save_dir : str
        Directory where the CSV file will be saved.
    header : list of str
        Column headers for the CSV file.
    task_name : str
        Task identifier. Used both in the filename and log message.
    data_list : list of list of float
        Data rows to be written into the CSV file.

    Returns
    -------
    None
    """
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
    # Run ``python mycode/utils/csv_saving.py``
    expected_rq = "RQ3"
    expected_program = "QuantumFourierTransform"
    rep_mode = "toy"
    expected_dir = "data(toy)\\raw_data_for_empirical_results\\RQ3\\QuantumFourierTransform"

    res_dir = RQ_saving_dir(expected_rq, expected_program, rep_mode)
    assert expected_dir in res_dir, "Wrong directory!"