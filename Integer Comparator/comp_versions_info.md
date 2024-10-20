# IC - v1
    line 233: replace cx with ch
    - circuit.cx(qr_state[i], qr_ancilla[i])     
    + circuit.ch(qr_state[i], qr_ancilla[i]) # bug

# IC - v2
    line 227: replace x with h
    - circuit.x(q_compare) 
    + circuit.h(q_compare)

# IC - v3
    line 240: switch qubits of ccx
    - circuit.ccx(qr_state[i], qr_ancilla[i - 1], qr_ancilla[i])      
    + circuit.ccx(qr_ancilla[i], qr_ancilla[i - 1], qr_state[i])      # defect switch qubit

# IC - v4
    line 206: delete if conditional  
    - if twos[i] == 1
  
    line 207: replace cx with ry
    - circuit.cx(qr_state[i], qr_ancilla[i])
    + circuit.ry(3.141592/5, qr_state[i])   #  replace gate
  
# IC - v5
    line 241: add h gate
    + circuit.h(qr_state) # bug 