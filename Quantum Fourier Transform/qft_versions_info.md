# QFT - v1
    line 286: add a cx gate   
    + circuit.cx(i, num_qubits - i - 1)   # def

# QFT - v2
    line 277: modify arithmetical operation  
    - lam = np.pi * (2.0 ** (k - j))   
    + lam = np.pi * (2.0 ** (k + j))      # defect 

# QFT - v3
    line 278: switch qubits of cp
    - circuit.cp(lam, j, k)       
    + circuit.cp(lam, k, j)     # def

# QFT - v4
    line 285: replace swap with ch
    - circuit.swap(i, num_qubits - i - 1)
    + circuit.ch(i, num_qubits - i - 1)        # def
  
# QFT - v5
    line 283 - 285: delete if conditional
    - if self._do_swaps:
    -     for i in range(num_qubits // 2):
    -         circuit.swap(i, num_qubits - i - 1)
    + for i in range(num_qubits // 2):
    +     circuit.swap(i, num_qubits - i - 1)