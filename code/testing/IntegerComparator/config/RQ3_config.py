import numpy as np

config_dict = {
   "all": {
      "versions": ["v1", "v2", "v3", "v4", "v5", "v6"],
      "qubit_list": [1, 2, 3, 4, 5, 6],
      "L_list": np.arange(-5, 5.1, 1),
      "sign_list": [True, False]
   },
   "toy": {
      "versions": ["v2"],
      "qubit_list": [2],
      "L_list": [-2, 0, 2],
      "sign_list": [True, False]   
   }
}   
    
 