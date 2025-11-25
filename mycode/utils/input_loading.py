def rep_mode_selection(config_data: dict, arg: str) -> dict:
    """
    Read the configuration for each experiment, and return the corresponding
    dictionary with the purposed data.

    We propose two mode for replication and reproduction, i.e., "toy" and "all". 
    The mode "all" indicates running all the test cases executed in our paper. Instead,
    the mode "toy" is designed to verify the functionality of our artifact, including a
    small subset of test cases. 

    Args:
        config_data (dict): The configuration dictionary.
        arg (str): Specifies the dataset type. If `"toy"`, returns the simplified dataset; 
                    otherwise returns the full dataset `"all"`.

    Returns:
        dict: A dictionary containing the input data for the experiment, returning 
              either the `"toy"` or `"all"` dataset according to `arg`.

    """
 
    if arg == "toy":
        input_data = config_data["toy"]
    else:
        input_data = config_data["all"]
    return input_data

if __name__ == "__main__":
    """
    Unit testing for rep_mode_selection.
    Run:
        python mycode/utils/input_loading.py
    """

    # ----------------------------
    # Test inputs
    # ----------------------------
    def test_input_rep_mode():
        return {
            "toy": {"a": 1, "b": 2},
            "all": {"x": 10, "y": 20, "z": 30},
        }

    # ----------------------------
    # Unit tests
    # ----------------------------

    def unit_test_rep_mode_toy(config_data):
        res = rep_mode_selection(config_data, "toy")
        assert res == config_data["toy"]

    def unit_test_rep_mode_all(config_data):
        res = rep_mode_selection(config_data, "all")
        assert res == config_data["all"]

    # ----------------------------
    # Test execution table
    # ----------------------------
    executed_test = {
        "0": {
            "input": test_input_rep_mode,
            "function": unit_test_rep_mode_toy,
        },
        "1": {
            "input": test_input_rep_mode,
            "function": unit_test_rep_mode_all,
        }
    }

    for id, exec_dict in executed_test.items():
        print(f"test_id={id}: ", end="")
        test_input = exec_dict["input"]()
        try:
            exec_dict["function"](test_input)
            if "manual" not in exec_dict["function"].__name__:
                print("pass")
        except AssertionError:
            print("fail")
            raise