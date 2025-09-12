import numpy as np
from typing import Literal

def pure_state_distribution(
    qubit_num: int, 
    mode: Literal["uniform"]
) -> list:
    distribution_dict = {
        "uniform": list(np.ones(2 ** qubit_num) / (2 ** qubit_num))
    }

    return distribution_dict[mode]

def covered_pure_states(
    qubit_num: int,
    mode: Literal["all_basis"]
) -> list:
    covered_state_dict = {
        "all_basis": list(range(2 ** qubit_num))
    }

    return covered_state_dict[mode]