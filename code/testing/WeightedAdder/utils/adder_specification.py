import numpy as np

def _PSTC_specification(s, qList, lambdaList):
    # qList is a binary list: q_{0} -> q_{n-1}
    # lambdaList is a weight list: lambda_{0} -> lambda_{n-1} 
    expProbs = (np.zeros(2 ** s)).tolist()
    expRes = 0
    for i in range(len(lambdaList)):
        expRes += lambdaList[i] * qList[i]      
    expProbs[expRes] = 1
    return expProbs

def _MSTC_specification(inputNums, inputProbs, n, s, lambdaList):    
    expProbs = (np.zeros(2 ** s)).tolist()
    for decimal_number in inputNums:
        binary_string = bin(decimal_number)[2:].zfill(n)
        qList = [int(bit) for bit in binary_string]
        qList = qList[::-1]
        expRes = 0
        for i in range(len(lambdaList)):
            expRes += lambdaList[i] * qList[i]      
        expProbs[expRes] += inputProbs[decimal_number]
    return expProbs