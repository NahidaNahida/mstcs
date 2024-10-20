def PSTC_specification(n, number):
    expProbs = [0] * (2 ** n)
    expProbs[number] = 1
    return expProbs

def MSTC_specification(inputProbs):
    return inputProbs