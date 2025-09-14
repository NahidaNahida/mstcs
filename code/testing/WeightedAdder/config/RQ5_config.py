import math

config_dict = {
   "all": {
      "shots_list": list(range(8, 1025, 8)),
      "versions": ["v1"],
      "qubit_list": [5],
      "weight_dict": {
         "qubit_num=1": [
            [0], 
            [1], 
            [2], 
            [3], 
            [4]
         ],
         "qubit_num=2": [
            [0, 0], 
            [0, 1], 
            [1, 2], 
            [1, 1], 
            [2, 2]
         ],
         "qubit_num=3": [
            [0, 0, 0], 
            [2, 0, 2], 
            [1, 1, 0], 
            [0, 2, 1], 
            [1, 0, 2]
         ],
         "qubit_num=4": [
            [0, 1, 1, 1], 
            [0, 0, 0, 0], 
            [2, 2, 0, 0], 
            [1, 1, 0, 0], 
            [1, 2, 0, 1]
         ],
         "qubit_num=5": [
            [1, 0, 2, 1, 2], 
            [0, 0, 1, 0, 0], 
            [0, 2, 0, 1, 0], 
            [2, 0, 1, 1, 0], 
            [0, 0, 2, 1, 0]
         ],
         "qubit_num=6": [  
            [1, 2, 2, 2, 2, 1], 
            [0, 0, 0, 0, 0, 0], 
            [2, 1, 0, 1, 1, 1], 
            [1, 3, 1, 0, 2, 0], 
            [1, 1, 0, 0, 0, 2]
         ]
      }
   },
   "toy": {
      "versions": ["v2"],
      "qubit_list": [4],
      "weight_dict": {"qubit_num=4": [[1, 2, 0, 1]]}         
   }
}   

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