import math
import numpy as np

config_dict = {
    "all": {
        "versions": ["v1", "v2", "v3", "v4", "v5", "v6"],
        "qubit_list": [1, 2, 3, 4, 5, 6],
        "slop_list": np.arange(-math.pi, math.pi + 1e-9, math.pi/2),
        "offset_list": np.arange(-math.pi, math.pi + 1e-9, math.pi/2)
    },
    "toy": {
        "versions": ["v2"],
        "qubit_list": [2],
        "slop_list": [math.pi / 2],
        "offset_list": [math.pi / 2]
    }
}   