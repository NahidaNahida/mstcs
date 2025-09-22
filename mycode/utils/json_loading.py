import os
import json

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