import pandas as pd
import sys, os
import numpy as np
import math

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
current_file_path = os.path.abspath(__file__)
parent_dir = os.path.dirname(current_file_path)   

from circuit_execution import *

from amplitude_defect1 import LinearAmplitudeFunction_defect1
from amplitude_defect2 import LinearAmplitudeFunction_defect2
from amplitude_defect3 import LinearAmplitudeFunction_defect3
from amplitude_defect4 import LinearAmplitudeFunction_defect4
from amplitude_defect5 import LinearAmplitudeFunction_defect5
from amplitude_defect6 import LinearAmplitudeFunction_defect6

def execute_function(program_name, program_version):
    function_name = program_name + program_version
    if function_name in globals():
        func = globals()[function_name]
        return func
    else:
        return f"Function '{function_name}' not found."
    
def fully_decompose(qc):
    '''
        thoroughly decompose a qc until only basis gates
    '''
    while True:
        decomposed_qc = qc.decompose()
        if decomposed_qc == qc:
            break
        qc = decomposed_qc
    return qc

def info_collection(program_version, n_list, slop_list, offset_list, domain_list, image_list ):
    program_name = 'LinearAmplitudeFunction'
    qubits_list = []
    gates_list = []
    depth_list = []
 
    for n in n_list:            
        for slop in slop_list:
            for offset in offset_list:
                for domain in domain_list:
                    for image in image_list:
                        # running the quantum programs
                        func = execute_function(program_name + '_defect', program_version)
                        qc = func(n, slop, offset, domain=domain, image=image)

                        # counts information of quantum circuits
                        qubits_list.append(qc.num_qubits)
                        decomposed_circ = fully_decompose(qc)
                        depths = decomposed_circ.depth()
                        gate_dict = decomposed_circ.count_ops()
                        gates = sum(gate_dict.values())
                        gates_list.append(gates)
                        depth_list.append(depths)

    print('#qubits : [{}, {}]'.format(min(qubits_list), max(qubits_list)))
    print('#gates : [{}, {}]'.format(min(gates_list), max(gates_list)))
    print('#depth : [{}, {}]'.format(min(depth_list), max(depth_list)))

if __name__ == "__main__":
    # the setting to generate classical inputs
    n_list = range(1, 7)
    slop_list = [0, math.pi / 4, math.pi / 2]
    offset_list = [0, math.pi / 4, math.pi / 2]
    domain_list = [[-1, 1], [-1, 0], [0, 1]]
    image_list = [[-1, 1], [-1, 0], [0, 1]]
    
    for program_version in ['v1', 'v2', 'v3', 'v4', 'v5', 'v6']:
        print(program_version)
        program_version = program_version[1:]
        info_collection(program_version, n_list, slop_list, offset_list, domain_list, image_list)