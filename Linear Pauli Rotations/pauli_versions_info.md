# LPR - v1
    bug:
        line 177: replace a ry gate with a rx gate
        - circuit.ry(self.offset, qr_target)      
        + circuit.rx(self.offset, qr_target)      # defects 1

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [5, 25]

# LPR - v2
    bug:
        line 185: replace a cry gate with a crz gate
        - circuit.cry(self.slope * pow(2, i), q_i, qr_target) 
        + circuit.crz(self.slope * pow(2, i), q_i, qr_target)      # defect 

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [5, 25]

# LPR - v3
    bugs:
        line 177: replace a ry gate with a rx gate
        - circuit.ry(self.offset, qr_target)      
        + circuit.rx(self.offset, qr_target)      # defects 1

        line 185: replace a cry gate with a crz gate
        - circuit.cry(self.slope * pow(2, i), q_i, qr_target) 
        + circuit.crz(self.slope * pow(2, i), q_i, qr_target)      # defect 2

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [4, 19]    

# LPR - v4
    bug:
        line 185: switch qubits within a cry gate, replace a cry gate with a crz gate 
        - circuit.cry(self.slope * pow(2, i), q_i, qr_target) 
        + circuit.crz(self.slope * pow(2, i), qr_target, q_i)    # def

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [4, 19]

# LPR - v5
    bug:
        line 185: switch qubits within a cry gate
        - circuit.cry(self.slope * pow(2, i), q_i, qr_target)   
        + circuit.cry(self.slope * pow(2, i), qr_target, q_i)      # defect

    complexity:
        #qubits : [2, 7]
        #gates : [5, 25]
        #depth : [4, 19]   

# LPR - v6
    bug:
        line 189: add a ry gate
        + circuit.ry(self.offset, 0)        # bug

    complexity:
        #qubits : [2, 7]
        #gates : [6, 26]
        #depth : [6, 25]