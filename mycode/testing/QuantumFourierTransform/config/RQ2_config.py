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
                    "T0-1": [math.pi/2], 
                    "T0-2": [math.pi/2]
                },
                "probs": {
                    "T0-1": [1/2, 1/2, 0, 0],
                    "T0-2": [0, 0, 1/2, 1/2]
                },
                "saving_name": "T0"
            },
            "test_suite_1": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T1-1": [math.pi/2, math.pi/2]
                },
                "probs": {
                    "T1-1": [1/4, 1/4, 1/4, 1/4]
                },
                "saving_name": "T1"
            },
            "test_suite_2": {
                "num_target": 2,
                "num_control": 3,
                "angles": {
                    "T2-1": [math.pi/2, math.pi/2, math.pi/2]
                },
                "probs": {
                    "T2-1": [1/4, 1/4, 1/4, 1/4]
                },
                "saving_name": "T2"
            },
            "test_suite_3": {
                "num_target": 2,
                "num_control": 1, 
                "angles": {
                    "T3-1": [2*math.pi/3],
                    "T3-2": [2*math.pi/3]
                },
                "probs": {
                    "T3-1": [1/4, 3/4, 0, 0],
                    "T3-2": [0, 0, 1/4, 3/4]
                },
                "saving_name": "T3"
            },
            "test_suite_4": {
                "num_target": 2, 
                "num_control": 2, 
                "angles": {
                    "T4-1": [1.911, math.pi/2, math.pi/2]
                }, 
                "probs": {
                    "T4-1": [1/6, 1/3, 1/6, 1/3]
                },
                "saving_name": "T4"
            },
            "test_suite_5": {
                "num_target": 2, 
                "num_control": 3,
                "angles": {
                    "T5-1": [1.911, math.pi/2, math.pi/2, math.pi/2, math.pi/2, math.pi/2, math.pi/2]
                },
                "probs": {
                    "T5-1": [1/6, 1/3, 1/6, 1/3] 
                },
                "saving_name": "T5"
            },
            "test_suite_6_separable": {
                "num_target": 2, 
                "num_control": 2, 
                "angles": {
                    "T6_sep-1": [math.pi/2, math.pi/2]
                },
                "probs": {
                    "T6_sep-1": [1/3, 1/3, 1/3, 0]
                },
                "saving_name": "T6_sep"
            },
            "test_suite_6_entangled": {
                "num_target": 2, 
                "num_control": 2, 
                "angles": {
                    "T6_ent-1": [1.231, math.pi/2, 0]
                },
                "probs": {
                    "T6_ent-1": [1/3, 1/3, 1/3, 0]
                },
                "saving_name": "T6_ent"
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
                    "T0-1": [math.pi/2], 
                    "T0-2": [math.pi/2]
                },
                "probs": {
                    "T0-1": [1/2, 1/2, 0, 0],
                    "T0-2": [0, 0, 1/2, 1/2]
                },
                "saving_name": "T0"
                },
            "test_suite_1": {
                "num_target": 2,
                "num_control": 2,
                "angles": {
                    "T1-1": [math.pi/2, math.pi/2]
                },
                "probs": {
                    "T1-1": [1/4, 1/4, 1/4, 1/4]
                },
                "saving_name": "T1"
            },
            "test_suite_2": {
                "num_target": 2,
                "num_control": 3,
                "angles": {
                    "T2-1": [math.pi/2, math.pi/2, math.pi/2]
                },
                "probs": {
                    "T2-1": [1/4, 1/4, 1/4, 1/4]
                },
                "saving_name": "T2"
            },
            "test_suite_3": {
                "num_target": 2,
                "num_control": 1, 
                "angles": {
                    "T3-1": [2*math.pi/3],
                    "T3-2": [2*math.pi/3]
                },
                "probs": {
                    "T3-1": [1/4, 3/4, 0, 0],
                    "T3-2": [0, 0, 1/4, 3/4]
                },
                "saving_name": "T3"
            },
            "test_suite_4": {
                "num_target": 2, 
                "num_control": 2, 
                "angles": {
                    "T4-1": [1.911, math.pi/2, math.pi/2]
                }, 
                "probs": {
                    "T4-1": [1/6, 1/3, 1/6, 1/3]
                },
                "saving_name": "T4"
            },
            "test_suite_5": {
                "num_target": 2, 
                "num_control": 3,
                "angles": {
                    "T5-1": [1.911, math.pi/2, math.pi/2, math.pi/2, math.pi/2, math.pi/2, math.pi/2]
                },
                "probs": {
                    "T5-1": [1/6, 1/3, 1/6, 1/3] 
                },
                "saving_name": "T5"
            },
            "test_suite_6_separable": {
                "num_target": 2, 
                "num_control": 2, 
                "angles": {
                    "T6_sep-1": [math.pi/2, math.pi/2]
                },
                "probs": {
                    "T6_sep-1": [1/3, 1/3, 1/3, 0]
                },
                "saving_name": "T6_sep"
            },
            "test_suite_6_entangled": {
                "num_target": 2, 
                "num_control": 2, 
                "angles": {
                    "T6_ent-1": [1.231, math.pi/2, 0]
                },
                "probs": {
                    "T6_ent-1": [1/3, 1/3, 1/3, 0]
                },
                "saving_name": "T6_ent"
            }
        }
    }
} 