import numpy as np

def PSTC_specification(x, A, b, c, outQubits):
    expProb = (np.zeros(2 ** outQubits)).tolist()
    # initial state = [1, 0] means (01)b = 1
    x = np.array(x)
    A = np.array(A)
    b = np.array(b)
    Q = np.dot(np.dot(x.T, A), x) + np.dot(x.T, b) + c
    expRes = (Q + (2 ** outQubits)) % (2 ** outQubits)
    expProb[expRes] = 1 
    return expProb

def MSTC_specification(inputNumbers,n, A, b, c, outQubits, inputProbs):
    expProbs = (np.zeros(2 ** outQubits)).tolist()
    for decimal_number in inputNumbers:
        binary_string = bin(decimal_number)[2:].zfill(n)
        binary_list = [int(bit) for bit in binary_string]
        x = binary_list[::-1]
        x = np.array(x)
        A = np.array(A)
        b = np.array(b)
        Q = np.dot(np.dot(x.T, A), x) + np.dot(x.T, b) + c
        expRes = int((Q + (2 ** outQubits)) % (2 ** outQubits))    
        expProbs[expRes] +=  inputProbs[decimal_number]
    return expProbs