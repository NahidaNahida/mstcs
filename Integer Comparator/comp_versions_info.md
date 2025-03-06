# IC - v1
    bug:
        line 233: replace a cx gate with a ch gate
        - circuit.cx(qr_state[i], qr_ancilla[i])     
        + circuit.ch(qr_state[i], qr_ancilla[i]) # bug

    complexity:
        #qubits : [2, 12]
        #gates : [0, 189]
        #depth : [0, 112]

# IC - v2
    bug:
        line 227: replace an x gate with an h gate
        - circuit.x(q_compare) 
        + circuit.h(q_compare)

    complexity:
        #qubits : [2, 12]
        #gates : [0, 183]
        #depth : [0, 106]

# IC - v3
    bug:
        line 240: switch qubits within a ccx gate
        - circuit.ccx(qr_state[i], qr_ancilla[i - 1], qr_ancilla[i])      
        + circuit.ccx(qr_ancilla[i], qr_ancilla[i - 1], qr_state[i])      # defect switch qubit
    
    complexity:
        #qubits : [2, 12]
        #gates : [0, 183]
        #depth : [0, 106]

# IC - v4
    bug:
        line 206: delete an if conditional  
        - if twos[i] == 1
    
        line 207: replace a cx gate with a ry gate
        - circuit.cx(qr_state[i], qr_ancilla[i])
        + circuit.ry(3.141592/5, qr_state[i])   #  replace gate

    complexity:
        #qubits : [2, 12]
        #gates : [0, 183]
        #depth : [0, 106]
  
# IC - v5
    bug:
        line 241: add an h gate
        + circuit.h(qr_state) # bug

    complexity:
        #qubits : [2, 12]
        #gates : [0, 183]
        #depth : [0, 106]

# IC - 6
    bug:
        line 189: replace an x gate with an h gate
        - circuit.x(q_compare)    # bug
        + circuit.h(q_compare)    # bug

    complexity:
        #qubits : [2, 12]
        #gates : [0, 183]
        #depth : [0, 106]