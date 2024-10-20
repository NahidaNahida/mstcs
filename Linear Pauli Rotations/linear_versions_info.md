# LPR - v1
    line 177: replace ry with rx
    - circuit.ry(self.offset, qr_target)      
    + circuit.rx(self.offset, qr_target)      # defects 1

# LPR - v2
    line 185: replace cry with crz
    - circuit.cry(self.slope * pow(2, i), q_i, qr_target) 
    + circuit.crz(self.slope * pow(2, i), q_i, qr_target)      # defect 

# LPR - v3
    line 177: replace ry with rx
    - circuit.ry(self.offset, qr_target)      
    + circuit.rx(self.offset, qr_target)      # defects 1

    line 185: replace cry with crz
    - circuit.cry(self.slope * pow(2, i), q_i, qr_target) 
    + circuit.crz(self.slope * pow(2, i), q_i, qr_target)      # defect 2

# LPR - v4
    line 185: switch qubits of cry gate, replace cry with crz 
    - circuit.cry(self.slope * pow(2, i), q_i, qr_target) 
    + circuit.crz(self.slope * pow(2, i), qr_target, q_i)    # def
  
# LPR - v5
    line 185: switch qubits of cry gate
    - circuit.cry(self.slope * pow(2, i), q_i, qr_target)   
    + circuit.cry(self.slope * pow(2, i), qr_target, q_i)      # defect