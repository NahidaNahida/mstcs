# QF - v1
    line 156: modify arithmetical operation
    - circuit.mcp(scaling * 2**i * value, [qr_input[j], qr_input[k]], q_i)     
    + circuit.mcp(scaling * 2 * i * value, [qr_input[j], qr_input[k]], q_i) # defect

# QF - v2
    line 146: switch qubits of cp
    - circuit.cp(scaling * 2**i * value, qr_input[j], q_i) 
    + circuit.cp(scaling * 2**i * value, q_i, qr_input[j])      # defect switch 

# QF - v3
    line 144: modify arithmetical operation
    - value += quadratic[j][j] if quadratic is not None else 0      
    + value -= quadratic[j][j] if quadratic is not None else 0    # def + -> -

# QF - v4
    line 157: add an h gate
    + circuit.h(q_i)      # def
  
# QF - v5
    line 132 - 133: delete an if condition
    - if little_endian:
    -    qr_result = qr_result[::-1]