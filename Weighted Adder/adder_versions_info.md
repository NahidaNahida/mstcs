# WA - v1
    line 257: delete a cx
    - circuit.cx(q_state, qr_sum[j])

# WA - v2
    line 303: delete an x
    - circuit.x(qr_sum[j])

# WA - v3
    line 303: replace an x with an h
    - circuit.x(qr_sum[j])
    + circuit.h(qr_sum[j])

    line 305: replace an x with an h
    - circuit.x(qr_sum[j])
    + circuit.h(qr_sum[j])

# WA - v4
    line 304: switch qubits of an ccx
    - circuit.ccx(q_state, qr_sum[j], qr_carry[j])
    + circuit.ccx(q_state, qr_carry[j], qr_sum[j]) # bug
  
# WA - v5
    line 252: replace a cx with a ch
    - circuit.cx(q_state, qr_sum[j])
    + circuit.ch(q_state, qr_sum[j])  # def
  
    line 257: replace a cx with a ch
    - circuit.cx(q_state, qr_sum[j])
    + circuit.ch(q_state, qr_sum[j])  # def