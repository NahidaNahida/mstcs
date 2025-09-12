# QF - v1
    bug:
        line 156: modify an arithmetical operation
        - circuit.mcp(scaling * 2**i * value, [qr_input[j], qr_input[k]], q_i)     
        + circuit.mcp(scaling * 2 * i * value, [qr_input[j], qr_input[k]], q_i) # defect

    complexity:
        #qubits : [4, 8]
        #gates : [9, 581]
        #depth : [6, 317]

# QF - v2
    bug:
        line 146: switch qubits within a cp gate
        - circuit.cp(scaling * 2**i * value, qr_input[j], q_i) 
        + circuit.cp(scaling * 2**i * value, q_i, qr_input[j])      # defect switch 

    complexity:
        #qubits : [4, 8]
        #gates : [9, 581]
        #depth : [6, 317]

# QF - v3
    bug:
        line 144: modify an arithmetical operation
        - value += quadratic[j][j] if quadratic is not None else 0      
        + value -= quadratic[j][j] if quadratic is not None else 0    # def + -> -

    complexity:
        #qubits : [4, 8]
        #gates : [9, 581]
        #depth : [6, 317]

# QF - v4
    bug:
        line 157: add an h gate
        + circuit.h(q_i)      # def
  
    complexity:
        #qubits : [4, 8]
        #gates : [9, 611]
        #depth : [6, 321]

# QF - v5
    bug:
        line 132 - 133: delete an if condition
        - if little_endian:
        -    qr_result = qr_result[::-1]

    complexity:
        #qubits : [4, 8]
        #gates : [9, 581]
        #depth : [6, 317]

# QF - v6
    bug:
        line 157: add an x gate
        + circuit.x(q_i)      # def

    complexity:
        #qubits : [4, 8]
        #gates : [9, 611]
        #depth : [6, 321]