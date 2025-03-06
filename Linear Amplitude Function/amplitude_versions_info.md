# LAF - v1
    bug:
        line 150: add a cx gate 
        + pwl_pauli_rotation.cx(0, -1) 

    complexity:
        #qubits : [2, 7]
        #gates : [6, 26]
        #depth : [6, 26]

# LAF - v2
    bug:
        line 144: modify an arithmetical operator
        - offset_angles[i] += np.pi * rescaling_factor * (mapped_offset[i] - c) / 2 / (d - c)
        + offset_angles[i] -= np.pi * rescaling_factor * (mapped_offset[i] - c) / 2 / (d - c)
  
    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [5, 25]


# LAF - v3
    bug:
        line 143: replace an arithmetical operation
        - slope_angles[i] = np.pi * rescaling_factor * mapped_slope[i] / 2 / (d - c)
        + slope_angles[i] = np.pi * rescaling_factor * mapped_slope[i] / 2 / (c - d) # d-c -> c-d
    
    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [5, 25]

# LAF - v4
    bug:
        line 144: delete an operational component, replace an arithmetical operation
        - offset_angles[i] += np.pi * rescaling_factor * (mapped_offset[i] - c) / 2 / (d - c)
        + offset_angles[i] += np.pi * rescaling_factor * (mapped_offset[i]) / 2 / (c - d)   # delete -c , change d-c -> c-d

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [5, 25]

# LAF - v5
    bug:
        line 136: replace an arithmetical operation
        - mapped_slope += [slope[i] * (b - a) / (2**num_state_qubits - 1)]
        + mapped_slope += [slope[i] * (b - a) / (2**(num_state_qubits - 1))]        # def 

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [5, 25]

# LAF - v6
    bug:
        line 150: add a ch gate
        + pwl_pauli_rotation.ch(0, -1)        # bug

    complexity:
        #qubits : [2, 7]
        #gates : [12, 32]
        #depth : [12, 32]