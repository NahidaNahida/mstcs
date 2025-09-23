import math

config_dict = {
    "all": {
        "versions": ["v1", "v2", "v3", "v4", "v5", "v6"],
        "if_swap_list": [True, False],
        "mixed_state_suites": {
            "test_suite_0": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T0-1": [math.pi/8], 
                    "T0-2": [math.pi/8]
                },
                "probs": {
                    "T0-1": [0.9619397662556434, 0.03806023374435662, 0, 0],
                    "T0-2": [0, 0, 0.9619397662556434, 0.03806023374435662]
                },
                "saving_name": "T0"
            },
            "test_suite_1": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T1-1": [math.pi/4],
                    "T1-2": [math.pi/4]
                },
                "probs": {
                    "T1-1": [0.8535533905932737, 0.14644660940672624, 0, 0],
                    "T1-2": [0, 0, 0.8535533905932737, 0.14644660940672624]
                },
                "saving_name": "T1"
            },
            "test_suite_2": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T2-1": [3 * math.pi/8],
                    "T2-2": [3 * math.pi/8]
                },
                "probs": {
                    "T2-1": [0.6913417161825449, 0.3086582838174551, 0, 0],
                    "T2-2": [0, 0, 0.6913417161825449, 0.3086582838174551]
                },
                "saving_name": "T2"
            }, 
            "test_suite_3": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T3-1": [math.pi/2],
                    "T3-2": [math.pi/2]
                },
                "probs": {
                    "T3-1": [0.5, 0.5, 0, 0],
                    "T3-2": [0, 0, 0.5, 0.5]
                },
                "saving_name": "T3"
            }, 
            "test_suite_4": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T4-1": [math.pi/8, math.pi/2]
                },
                "probs": {
                    "T4-1": [0.48096988312782174, 0.01903011687217831, 0.48096988312782174, 0.01903011687217831]
                },
                "saving_name": "T4"                
            },
            "test_suite_5": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T5-1": [2*math.pi/8, math.pi/2]
                },
                "probs": {
                    "T5-1": [0.4267766952966369, 0.07322330470336312, 0.4267766952966369, 0.07322330470336312]
                },
                "saving_name": "T5"                
            },            
            "test_suite_6": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T6-1": [3*math.pi/8, math.pi/2]
                },
                "probs": {
                    "T6-1": [0.3456708580912725, 0.15432914190872754, 0.3456708580912725, 0.15432914190872754]
                },
                "saving_name": "T6"                
            },
            "test_suite_7": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T7-1": [math.pi/2, math.pi/2]
                },
                "probs": {
                    "T7-1": [0.25, 0.25, 0.25, 0.25]
                },
                "saving_name": "T7"                
            }            
        }
   },
    "toy": {
        "versions": ["v2"],
        "if_swap_list": [True, False],
        "mixed_state_suites": {
            "test_suite_0": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T0-1": [math.pi/8], 
                    "T0-2": [math.pi/8]
                },
                "probs": {
                    "T0-1": [0.9619397662556434, 0.03806023374435662, 0, 0],
                    "T0-2": [0, 0, 0.9619397662556434, 0.03806023374435662]
                },
                "saving_name": "T0"
            },
            "test_suite_1": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T1-1": [math.pi/4],
                    "T1-2": [math.pi/4]
                },
                "probs": {
                    "T1-1": [0.8535533905932737, 0.14644660940672624, 0, 0],
                    "T1-2": [0, 0, 0.8535533905932737, 0.14644660940672624]
                },
                "saving_name": "T1"
            },
            "test_suite_2": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T2-1": [3 * math.pi/8],
                    "T2-2": [3 * math.pi/8]
                },
                "probs": {
                    "T2-1": [0.6913417161825449, 0.3086582838174551, 0, 0],
                    "T2-2": [0, 0, 0.6913417161825449, 0.3086582838174551]
                },
                "saving_name": "T2"
            }, 
            "test_suite_3": {
                "num_target": 2,
                "num_control": 1,
                "angles": {
                    "T3-1": [math.pi/2],
                    "T3-2": [math.pi/2]
                },
                "probs": {
                    "T3-1": [0.5, 0.5, 0, 0],
                    "T3-2": [0, 0, 0.5, 0.5]
                },
                "saving_name": "T3"
            }, 
            "test_suite_4": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T4-1": [math.pi/8, math.pi/2]
                },
                "probs": {
                    "T4-1": [0.48096988312782174, 0.01903011687217831, 0.48096988312782174, 0.01903011687217831]
                },
                "saving_name": "T4"                
            },
            "test_suite_5": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T5-1": [2*math.pi/8, math.pi/2]
                },
                "probs": {
                    "T5-1": [0.4267766952966369, 0.07322330470336312, 0.4267766952966369, 0.07322330470336312]
                },
                "saving_name": "T5"                
            },            
            "test_suite_6": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T6-1": [3*math.pi/8, math.pi/2]
                },
                "probs": {
                    "T6-1": [0.3456708580912725, 0.15432914190872754, 0.3456708580912725, 0.15432914190872754]
                },
                "saving_name": "T6"                
            },
            "test_suite_7": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T7-1": [math.pi/2, math.pi/2]
                },
                "probs": {
                    "T7-1": [0.25, 0.25, 0.25, 0.25]
                },
                "saving_name": "T7"                
            }            
        }
    }
} 