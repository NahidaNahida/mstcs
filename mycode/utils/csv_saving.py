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

    if task_name == "":
        print(f"This task is done! Saved at {file_path}")
    else:
        print(f"Task {task_name} is done! Saved at {file_path}")

 

if __name__ == "__main__":
    """
    Unit & Integration Testing.
    Run:
        python mycode/utils/csv_saving.py
    """

    import tempfile
    import shutil
    import os

    # ----------------------------
    # Test input generators
    # ----------------------------

    def test_input_rq_saving_dir():
        return {
            "rq_name": 2,
            "program_name": "TestProgram",
            "rep_mode": "toy",
        }

    def test_input_rq_saving_name():
        return {
            "rq_name": "RQ5",
            "program_name": "MyProg",
            "program_ver": "v2",
            "task_name": "taskA",
        }

    def test_input_csv_saving():
        tmp_dir = tempfile.mkdtemp()
        return {
            "rq_name": "RQ7",
            "program_name": "Alpha",
            "program_ver": "v1",
            "save_dir": tmp_dir,
            "header": ["col1", "col2"],
            "task_name": "T",
            "data_list": [[1, 2], [3, 4]],
            "tmp_dir": tmp_dir,
        }

    # ----------------------------
    # Unit tests
    # ----------------------------

    def unit_test_rq_saving_dir(args):
        res = RQ_saving_dir(**args)
        # rq_name = 2 → converted to RQ2 automatically
        assert "RQ2" in res
        assert "TestProgram" in res
        assert "data(toy)" in res

    def unit_test_rq_saving_name(args):
        res = RQ_saving_name(**args)
        assert res == "RQ5_MyProg_v2_taskA.csv"

    # ----------------------------
    # Integration test 
    # ----------------------------

    def integration_test_csv_saving(args):
        csv_saving(
            args["rq_name"],
            args["program_name"],
            args["program_ver"],
            args["save_dir"],
            args["header"],
            args["task_name"],
            args["data_list"],
        )

        expected_name = RQ_saving_name(
            args["rq_name"],
            args["program_name"],
            args["program_ver"],
            args["task_name"],
        )
        file_path = os.path.join(args["save_dir"], expected_name)

        assert os.path.exists(file_path), "CSV file not generated!"

        # Read back to check content
        with open(file_path, "r") as f:
            lines = f.read().strip().split("\n")
            assert lines[0] == "col1,col2"
            assert lines[1] == "1,2"
            assert lines[2] == "3,4"

        # clean temp directory
        shutil.rmtree(args["tmp_dir"])

    # ----------------------------
    # Test execution table
    # ----------------------------

    executed_test = {
        "0": {
            "input": test_input_rq_saving_dir,
            "function": unit_test_rq_saving_dir,
        },
        "1": {
            "input": test_input_rq_saving_name,
            "function": unit_test_rq_saving_name,
        },
        "2": {
            "input": test_input_csv_saving,
            "function": integration_test_csv_saving,
        },
    }

    for id, exec_dict in executed_test.items():
        print(f"test_id={id}:")
        test_input = exec_dict["input"]()
        try:
            exec_dict["function"](test_input)
            print("pass")
        except AssertionError as e:
            print("fail")
            raise