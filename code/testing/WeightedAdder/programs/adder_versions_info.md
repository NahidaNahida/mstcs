# WA - v1
    bug:
        line 257: delete a cx gate
        - circuit.cx(q_state, qr_sum[j])

    complexity:
        #qubits : [2, 14]
        #gates : [0, 1180]
        #depth : [0, 801]

# WA - v2
    bug:
        line 303: delete an x gate
        - circuit.x(qr_sum[j])

    complexity:
        #qubits : [2, 14]
        #gates : [0, 1178]
        #depth : [0, 812]

# WA - v3
    bugs:
        line 303: replace an x gate with an h gate
        - circuit.x(qr_sum[j])
        + circuit.h(qr_sum[j])

        line 305: replace an x gate with an h gate
        - circuit.x(qr_sum[j])
        + circuit.h(qr_sum[j])

    complexity:
        #qubits : [2, 14]
        #gates : [0, 1180]
        #depth : [0, 801]

# WA - v4
    bug:
        line 304: switch qubits within a ccx gate
        - circuit.ccx(q_state, qr_sum[j], qr_carry[j])
        + circuit.ccx(q_state, qr_carry[j], qr_sum[j]) # bug
    
    complexity:
        #qubits : [2, 14]
        #gates : [0, 1180]
        #depth : [0, 800]

# WA - v5
    bugs:
        line 252: replace a cx gate with a ch gate
        - circuit.cx(q_state, qr_sum[j])
        + circuit.ch(q_state, qr_sum[j])  # def
    
        line 257: replace a cx gate with a ch gate
        - circuit.cx(q_state, qr_sum[j])
        + circuit.ch(q_state, qr_sum[j])  # def

    complexity:
        #qubits : [2, 14]
        #gates : [0, 1192]
        #depth : [0, 807]

# WA - v6
    bugs:
        line 297: reverse a process
        - for j in reversed(range(len(weight_binary))):
        + for j in (range(len(weight_binary))):   # bug

        line 303: delete an \texttt{x} gate
        - circuit.x(qr_sum[j])  

    complexity:
        #qubits : [2, 14]
        #gates : [0, 1178]
        #depth : [0, 812]