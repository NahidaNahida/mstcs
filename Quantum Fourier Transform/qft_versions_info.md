# QFT - v1
    bug:
        line 286: add a cx gate   
        + circuit.cx(i, num_qubits - i - 1)   # def

    complexity:
        #qubits : [1, 6]
        #gates : [1, 93]
        #depth : [1, 43]

# QFT - v2
    bug:
        line 277: modify an arithmetical operation  
        - lam = np.pi * (2.0 ** (k - j))   
        + lam = np.pi * (2.0 ** (k + j))      # defect 

    complexity:
        #qubits : [1, 6]
        #gates : [1, 90]
        #depth : [1, 42]

# QFT - v3
    bug:
        line 278: switch qubits within a cp gate
        - circuit.cp(lam, j, k)       
        + circuit.cp(lam, k, j)     # def

    complexity:
        #qubits : [1, 6]
        #gates : [1, 90]
        #depth : [1, 42]

# QFT - v4
    bug:
        line 285: replace a swap gate with a ch gate
        - circuit.swap(i, num_qubits - i - 1)
        + circuit.ch(i, num_qubits - i - 1)        # def

    complexity:
        #qubits : [1, 6]
        #gates : [1, 102]
        #depth : [1, 43]

# QFT - v5
    bug:
        line 283 - 285: delete if conditional
        - if self._do_swaps:
        -     for i in range(num_qubits // 2):
        -         circuit.swap(i, num_qubits - i - 1)
        + for i in range(num_qubits // 2):
        +     circuit.swap(i, num_qubits - i - 1)

    complexity:
        #qubits : [1, 6]
        #gates : [1, 90]
        #depth : [1, 42]

# QFT - v6
    bug:
        line 283 - 285: delete an if branch
        - if self._do_swaps:
        -     for i in range(num_qubits // 2):
        -         circuit.swap(i, num_qubits - i - 1)

    complexity:
        #qubits : [1, 6]
        #gates : [1, 81]
        #depth : [1, 39]