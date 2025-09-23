import math

def RQ5_create_2MS_input(num_target: int) -> dict:
    return {
        "num_target": num_target,
        "num_control": num_target - 1,
        "angles": {
            "2MS-1": [math.pi/2] * (num_target - 1),
            "2MS-2": [math.pi/2] * (num_target - 1)
        },
        "probs": {
            "2MS-1": [1 / (2 ** (num_target - 1))] * (2 ** (num_target - 1)) + [0] * (2 ** (num_target - 1)),
            "2MS-2": [0] * (2 ** (num_target - 1)) + [1 / (2 ** (num_target - 1))] * (2 ** (num_target - 1))
        },
        "saving_name": "MSTC(2MS)"
    }

def RQ5_create_1MS_input(num_target: int) -> dict:
    return {
        "num_target": num_target,
        "num_control": num_target,
        "angles": {
            "1MS-1": [math.pi/2] * num_target
        },
        "probs": {
            "1MS-1": [1 / (2 ** num_target)] * (2 ** num_target)
        },
        "saving_name": "MSTC(1MS)"
    }

config_dict = {
    "all": {
        "versions": ["v1"],
        "shots_list": list(range(8, 1025, 8)),
        "qubit_list": [5],
        "if_swap_list": [True, False]
    },
    "toy": {
        "versions": ["v1"],
        "shots_list": [8, 1024],
        "qubit_list": [5],
        "if_swap_list": [True, False]
    }
} 


for mode in ["all", "toy"]:
   config_dict[mode]["mixed_state_suites"] = {
      "test_suite_1MS": RQ5_create_1MS_input(
         config_dict[mode]["qubit_list"][0]
      ),
      "test_suite_2MS": RQ5_create_2MS_input(
         config_dict[mode]["qubit_list"][0]
      )
   }
 