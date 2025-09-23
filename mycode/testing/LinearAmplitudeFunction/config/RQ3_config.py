import math

config_dict = {
    "all": {
        "versions": ["v1", "v2", "v3", "v4", "v5", "v6"],
        "qubit_list": [1, 2, 3, 4, 5, 6],
        "slop_list": [0, math.pi / 4, math.pi / 2],
        "offset_list": [0, math.pi / 4, math.pi / 2],
        "domain_list": [[-1, 1], [-1, 0], [0, 1]],
        "image_list": [[-1, 1], [-1, 0], [0, 1]]
   },
    "toy": {
        "versions": ["v2"],
        "qubit_list": [2],
        "slop_list": [math.pi / 2],
        "offset_list": [math.pi / 2],
        "domain_list": [[-1, 1]],
        "image_list": [[-1, 1]]
    }
}   